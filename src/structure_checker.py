def check_structure(report_text, required_sections):
    """
    Checks if sections extracted from guidelines exist in the report.
    """
    errors = []
    report_text_lower = report_text.lower()
    
    for section in required_sections:
        if section.lower() not in report_text_lower:
            errors.append(f"Missing mandatory section: {section}")
            
    return errors