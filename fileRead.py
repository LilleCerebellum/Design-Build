import pdfplumber
import re


pattern = re.compile(r"Date: \d+-\d+-\d+", re.IGNORECASE)
    
    
UPLOAD_FOLDER = "/home/sugrp202/journals/"
    

with pdfplumber.open(UPLOAD_FOLDER + "falsk_tandlaegejournal.pdf") as f:
    for i in f. pages:
        Text = i. extract_text()
        if Text:
            print("it extracted")
            matches = pattern.search(Text)
            if matches:
                dateText = matches.group()
                print("grouping:" + str(dateText))
            else:
                print("No date found in text.")




#https://medium.com/@python-javascript-php-html-css/creating-patterns-to-exclude-specific-words-using-regular-expressions-0b6398c644b6
