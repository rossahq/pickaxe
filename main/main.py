import pathlib

import pdfParser.pdfparser
import topicGeneration.lda
import argumentMining.miningtools as arg_mining


class Main:

    def main(self):
        parser = pdfParser.pdfparser.PdfParser()
        # parsed_text = parser.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.txt')
        parsed_text = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.txt')
        cleaned_text = parser.clean_pdf(parsed_text)
        split_text = parser.split_text(cleaned_text)

        topic_models = topicGeneration.lda.generate_topic_models(split_text)

        mining = arg_mining.MiningTools()
        args = mining.argument_word_match(split_text)
        topic_argument_relations = mining.calculate_soft_cosine_similarity(topic_models, args)
        print("Complete!")
        x = 0
        for relation in topic_argument_relations:
            x = x + 1
            print("Topic key words: " + relation)
            print("Number of claims related to this topic: %.0f" % len(topic_argument_relations.get(relation)))
            print("Arguments associated with topic :" + str(topic_argument_relations.get(relation)))

    def read_txt(self, path, filename):
        data = pathlib.Path(path, filename)
        fp = open(data, 'r', encoding="utf8")
        data = fp.read()
        return data


if __name__ == '__main__':
    main = Main()
    main.main()
