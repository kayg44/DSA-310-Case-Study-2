import pdfplumber 
import re 

def extract_text_from_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text())
    return pages

def clean_page_text(text):
    if text is None:
        return ""
    # remove page numbers
    text = re.sub(r'^\s*Page\s+\d+.*$', '', text, flags=re.MULTILINE)
    # remove multiple spaces/newlines
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def extract_and_clean(path):
    raw_pages = extract_text_from_pdf(path)
    clean_pages = [clean_page_text(p) for p in raw_pages]
    return "\n".join(clean_pages)

