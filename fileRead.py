import pdfplumber


    
with pdfplumber.open("C:/Users/soell_7pbpycu/Desktop/Synopsis 3 semester projekt.pdf") as f:
    text = pdf.extract_text()
    print(text)