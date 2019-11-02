import pathlib
from ctypes import windll

from nltk import download
from nltk.corpus import stopwords

import pdfParser.pdfparser as parser
import topicGeneration.lda
import tkinter as tk
from tkinter import *
import argumentMining.miningtools as arg_mining
download('stopwords')  # Download stopwords list.


class Main:

    def main(self):

        pdf_parser = parser.PdfParser()
        parsed_text = pdf_parser.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'iraq_exec_summary.pdf')

        # parsed_text = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'iraq_test.txt')
        # text = parsed_text.lower().split()
        # filtered_words = [word for word in text if word not in stopwords.words('english')]
        # final = " ".join(filtered_words)
        # finalfinal = pdf_parser.clean_pdf(final)
        # f = open("output.dat", "a")
        # print(finalfinal, file=f)
        # f.close()

        topic_models = topicGeneration.lda.generate_topic_models(parsed_text)
        print(str(parsed_text))
        mining = arg_mining.MiningTools()
        args = mining.argument_word_match(parsed_text)
        claims = mining.claim_verb_match(args)
        topic_argument_relations = mining.calculate_soft_cosine_similarity(topic_models, claims)

        print("Complete!")

        claims = 0
        for relation in topic_argument_relations:
            claims += len(topic_argument_relations.get(relation))

        result_string = ""
        result_string += "Number of sentences in document: %d \n" % len(parsed_text)
        result_string += "Number of claims detected: %d \n" % claims
        f = open("results.txt", "a")

        x = 0
        for relation in topic_argument_relations:
            x = x + 1
            print("\nTopic %d " % x + "key words: " + relation, file=f)
            print("Number of claims related to this topic: %.d" % len(topic_argument_relations.get(relation)), file=f)
            print("Arguments associated with topic: " + str(topic_argument_relations.get(relation)),file=f)
            result_string += ("\nTOPIC %d " % x + "KEY WORDS: " + relation + "\n")
            result_string += ("Number of CLAIMS related to this TOPIC: %.d" % len(topic_argument_relations.get(relation))+ "\n")
            for claim in topic_argument_relations.get(relation):
                result_string += ("\nCLAIM sentence: " + str(claim) + "\n")

        self.start_gui(result_string)
        self.write_output_file(result_string)
        f.close()

    def read_txt(self, path, filename):
        data = pathlib.Path(path, filename)
        fp = open(data, 'r', encoding="utf8")
        data = fp.read()
        return data

    def write_output_file(self, output):
        text_file = open(r"C:\Users\ROSSA\PycharmProjects\pickaxe\output\output.txt", "w")
        text_file.write(output)
        text_file.close()

    def start_gui(self, result_string):
        root = tk.Tk()
        T = tk.Text(root, height=45, width=80)
        T.pack()
        T.insert(tk.END, result_string)
        tk.mainloop()


if __name__ == '__main__':
    if 'win' in sys.platform:
        windll.shcore.SetProcessDpiAwareness(1)
    main = Main()
    main.main()
