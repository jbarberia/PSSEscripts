"""
Retira el uno en la parte inferior del PDF
Recorta el PDF quitando los bordes que queden por un mal paginado
"""
import sys
import fitz

def ajusta_pdf(pdf_path):
    # Remueve el unito al final del documento
    doc = fitz.open(pdf_path)
    for page_number, page in enumerate(doc, start=1):
        text_blocks = page.get_text("blocks")
        page_height = page.rect.height
        for block in text_blocks:
            x0, y0, x1, y1, text, _, _ = block
            if abs(y1 - page_height) < 10 and text.strip() == "1":
                print(text)
                page.add_redact_annot((x0, y0, x1, y1), "")
                page.apply_redactions()
    # Recorta todos los bordes sobrantes
    for page_number, page in enumerate(doc, start=1):
        content_rect = page.rect
        x0, y0, x1, y1 = page.cropbox
        paths = page.get_drawings()   
        x0 = None
        y0 = None
        x1 = None
        y1 = None
        for path in paths:
            u0, v0, u1, v1 = path["rect"]
            x0 = min(x0, u0) if x0 else u0
            y0 = min(y0, v0) if y0 else v0
            x1 = max(x1, u1) if x1 else u1
            y1 = max(y1, v1) if y1 else v1
        page.set_cropbox(fitz.Rect(x0, y0, x1, y1))
    doc.save(pdf_path.replace(".pdf", "_out.pdf"))


if __name__ == "__main__":
    pdfs = [x for x in sys.argv[1:] if x.endswith(".pdf")]
    for pdf in pdfs:
        ajusta_pdf(pdf)