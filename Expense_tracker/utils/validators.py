def validate_email(email):
    return "@" in email and "." in email

def validate_password(password):
    return len(password) >= 8