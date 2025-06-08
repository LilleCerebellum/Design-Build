import pdfplumber
import re

pattern = re.compile(r"børn \d+-\d+", re.IGNORECASE)
    
with pdfplumber.open("C:/Users/soell_7pbpycu/Desktop/Synopsis 3 semester projekt.pdf") as f:
    for i in f. pages:
        Text = i. extract_text()
        if Text:
            print("it extracted")
            matches = pattern.findall(Text)
            print(*matches, sep='\n')
    


"""
test_string = "Example text without the forbidden word."
result = pattern.match(test_string)
if result:
    print("No forbidden word found.")
else:
    print("Forbidden word detected.")
    
"""