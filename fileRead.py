
import pdfplumber
import re





def extract_date_from_pdf(pdf_path):
    date_pattern = re.compile(r"Date: \d+-\d+-\d+", re.IGNORECASE)
    behandler_pattern = re.compile(r"Behandler: [A-ZÆØÅ][a-zæøå]+(?: [A-ZÆØÅ][a-zæøå]+)+", re.IGNORECASE) #Behandler Pattern done by AI
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                print("it extracted")

                date_match = date_pattern.search(text)
                if date_match:
                    date_text = date_match.group()
                    print("search (date):", date_match)
                    print("grouping (date):", date_text)
                
                behandler_match = behandler_pattern.search(text)
                if behandler_match:
                    behandler_text = behandler_match.group()
                    print("search (behandler):", behandler_match)
                    print("grouping (behandler):", behandler_text)
                
                return date_text, behandler_text
"""
test_string = "Example text without the forbidden word."
result = pattern.match(test_string)
if result:
    print("No forbidden word found.")
else:
    print("Forbidden word detected.")
    
"""