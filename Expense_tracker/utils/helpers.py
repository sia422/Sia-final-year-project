from datetime import datetime

def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")