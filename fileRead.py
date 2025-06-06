import pdfplumber


    
with pdfplumber.open("C:/Users/soell_7pbpycu/Desktop/Synopsis 3 semester projekt.pdf") as f:
    for i in f. pages:
        print(i. extract_text())
    