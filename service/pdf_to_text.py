import pymupdf


def extract_text(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def save_text(text, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    name = "map"
    pdf_path = f"pdf/{name}.pdf"
    text = extract_text(pdf_path)
    save_text(text, f"txt/{name}.txt")
