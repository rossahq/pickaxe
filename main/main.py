import pdfParser.pdfparser


class Main:

    def main(self):
        parser = pdfParser.pdfparser.PdfParser()
        parsed_text = parser.parse_pdf()

        split_text = parser.split_text(parsed_text)

        print(parsed_text)
        print(split_text[2])


if __name__ == '__main__':
    main = Main()
    main.main()
