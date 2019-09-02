import pdfParser.pdfparser
import topicGeneration.lda
import argumentMining.miningtools as arg_mining


class Main:

    def main(self):
        parser = pdfParser.pdfparser.PdfParser()
        parsed_text = parser.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.pdf')
        split_text = parser.split_text(parsed_text)

        topic_models = topicGeneration.lda.generate_topic_models(split_text)

        mining = arg_mining.MiningTools()
        args = mining.argument_word_match(split_text)
        mining.calculate_cosine_similarity(topic_models, args)

if __name__ == '__main__':
    main = Main()
    main.main()
