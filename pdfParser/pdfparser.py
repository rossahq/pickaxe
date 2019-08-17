from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import pathlib


class PdfParser:

    def parse_pdf(self):
        data = pathlib.Path(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.pdf')
        fp = open(data, 'rb')
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.

        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data = retstr.getvalue()

        return data

    def clean_pdf(self, text):
        pass

    def split_text(self, text):
        split_text = text.split(".")
        return split_text

