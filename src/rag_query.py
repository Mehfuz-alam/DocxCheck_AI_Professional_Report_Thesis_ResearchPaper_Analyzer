import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=st.getenv("GEMINI_API_KEY"))
output_parser = StrOutputParser()

def extract_requirements(guideline_context):
    """Extracts font, size, and sections as structured data."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional academic formatting auditor."),
        ("user", "Extract rules from these guidelines: {context}\n\nReturn ONLY a JSON: {{\"font_name\": \"str\", \"font_size\": int, \"sections\": [\"list\"]}}")
    ])
    try:
        chain = prompt | llm | output_parser
        res = chain.invoke({"context": guideline_context})
        data = json.loads(re.search(r"\{.*\}", res, re.DOTALL).group())
        return data
    except:
        return {"font_name": "Times New Roman", "font_size": 12, "sections": ["Abstract", "Introduction", "Conclusion", "References"]}

def query_rag(report_text, relevant_guidelines):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional project reviewer."),
        ("user", "Report: {report_text}\nGuidelines: {relevant_guidelines}\n\nProvide deep feedback. AT THE END, add 'QUICK FIX SUMMARY' with 'Error -> Fix' points.")
    ])
    chain = prompt | llm | output_parser
    return chain.invoke({"report_text": report_text, "relevant_guidelines": "\n".join(relevant_guidelines)})