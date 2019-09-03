import pdfParser.pdfparser
import topicGeneration.lda
import argumentMining.miningtools as arg_mining


class Main:

    def main(self):
        parser = pdfParser.pdfparser.PdfParser()
        parsed_text = parser.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.pdf')
        cleaned_text = parser.clean_pdf(parsed_text)
        split_text = parser.split_text(cleaned_text)

        topic_models = topicGeneration.lda.generate_topic_models(split_text)

        mining = arg_mining.MiningTools()
        args = mining.argument_word_match(split_text)
        topic_argument_relations = mining.calculate_cosine_similarity(topic_models, args)

        x = 0
        for relation in topic_argument_relations:
            x = x + 1
            print("Topic "+ str(x) + ": " + relation)
            print("Arguments associated with topic " + str(x) + ":" + topic_argument_relations.get(relation))


if __name__ == '__main__':
    main = Main()
    main.main()
