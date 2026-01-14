def check_formatting(styles, required_styles):
    """
    Checks document styles against dynamically extracted requirements.
    """
    errors = []
    # Defaults are used only if the AI fails to extract rules
    target_font = required_styles.get("font_name", "Times New Roman")
    target_size = required_styles.get("font_size", 12)

    for para in styles:
        # Check Font Name
        if para["font_name"] and para["font_name"].lower() != target_font.lower():
            errors.append(f"Font mismatch: Found '{para['font_name']}', expected '{target_font}' in '{para['text'][:30]}...'")
        
        # Check Font Size
        if para["font_size"] and para["font_size"] != target_size:
            errors.append(f"Size mismatch: Found {para['font_size']}pt, expected {target_size}pt in '{para['text'][:30]}...'")
            
    return errors