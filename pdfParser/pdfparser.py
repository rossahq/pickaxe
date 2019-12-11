from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import pathlib


class PdfParser:

    def parse_pdf(self, path, filename):
        parsed_text = self.read_pdf(path, filename)
        cleaned_text = self.clean_pdf(parsed_text)
        split_text = self.split_text(cleaned_text)

        self.write_processed_file(split_text)

        return split_text


    def read_pdf(self, path, filename):
        data = pathlib.Path(path, filename)
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

        split = text.split(" ")
        text = self.get_core_text(split)

        text = " ".join(text)
        text = " ".join(text.split())

        text = text.replace('\n', ' ')
        text = text.encode('ascii', 'ignore')
        text = str(text)

        return text

    def split_text(self, text):
        split_text = text.split(".")
        for sentence in split_text:
            if not sentence:
                split_text.remove(sentence)
            if "indd" in sentence:
                split_text.remove(sentence)
        return split_text

    #return main body of text i.e that occurring after table of contents, etc
    def get_core_text(self, split_text):
        x = 0
        y = True
        while x < len(split_text)-1 or y is False:
            if '1.' in split_text[x]:
                start_splice = 0
                end_splice = x
                del split_text[start_splice:end_splice]
                return split_text
            x = x + 1

        return split_text

    def write_processed_file(self, cleaned_text):
        text = ".".join(cleaned_text)

        with open(r"C:\Users\ROSSA\PycharmProjects\pickaxe\output\output.txt", "w") as file:
            file.write(text)
        file.close()


if __name__ == '__main__':
    p = PdfParser()
    result = p.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'iraq_exec_summary.pdf')
    print("parsed pdf: " + str(result))
