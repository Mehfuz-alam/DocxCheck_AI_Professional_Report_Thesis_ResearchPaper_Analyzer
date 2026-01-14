# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.document_parser import parse_document, highlight_errors_docx
from src.format_checker import check_formatting
from src.structure_checker import check_structure
from src.embeddings import create_embeddings, search_embeddings
from src.rag_query import query_rag, extract_requirements
from utils.file_utils import save_file
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Directories
USER_REPORTS_DIR = "data/user_reports"
GUIDELINES_DIR = "data/guidelines"
os.makedirs(USER_REPORTS_DIR, exist_ok=True)
os.makedirs(GUIDELINES_DIR, exist_ok=True)

@app.on_event("startup")
def startup_event():
    # Only try to create embeddings if the directory is NOT empty
    if os.path.exists(GUIDELINES_DIR) and os.listdir(GUIDELINES_DIR):
        print("Initializing guideline index...")
        create_embeddings(GUIDELINES_DIR)
        print("Startup index ready!")
    else:
        print("No guidelines found in directory. Waiting for upload.")

@app.post("/upload_report/")
async def upload_report(guidelines: UploadFile = File(...), report: UploadFile = File(...)):
    # FIX: Clear old local guideline files so they don't get re-indexed
    for filename in os.listdir(GUIDELINES_DIR):
        file_path = os.path.join(GUIDELINES_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    # 1. Save the NEW files
    g_path = save_file(guidelines, GUIDELINES_DIR)
    r_path = save_file(report, USER_REPORTS_DIR)
    
    # 2. Re-create embeddings (Now it only contains the one new file)
    create_embeddings(GUIDELINES_DIR)
    
    # 3. Parse report and get AI context
    text, styles = parse_document(r_path)
    context = search_embeddings(text)
    
    # 4. Extract requirements and audit
    rules = extract_requirements("\n".join(context))
    f_errors = check_formatting(styles, rules)
    s_errors = check_structure(text, rules["sections"])
    
    # 5. Get AI Suggestions
    ai_res = query_rag(text, context)
    
    # 6. Generate Highlighted Report
    h_path = os.path.join(USER_REPORTS_DIR, f"highlighted_{report.filename}")
    highlight_errors_docx(r_path, h_path, f_errors, s_errors)

    return {
        "detected_rules": rules,
        "format_errors": f_errors,
        "structure_errors": s_errors,
        "rag_suggestions": ai_res,
        "highlighted_report_path": h_path
    }