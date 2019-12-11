import pathlib
from ctypes import windll

from nltk import download
import json

import main.lda
from tkinter import *
import re
import argumentMining.miningtools as arg_mining
download('stopwords')  # Download stopwords list.


class Main:

    def main(self):

       # pdf_parser = parser.PdfParser()
       # parsed_text = pdf_parser.parse_pdf(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'iraq_exec_summary.pdf')
       i = 1
       total_claims = 0
       total_matches = 0
       total_premise_matches = 0
       total_annotated_claims = 0
       while i < 91:

           number = i
           if i < 10:
               number = "0" + str(i)
           essay_name = "essay" + str(number) + ".txt"

           parsed_text = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\essays', essay_name)
           parsed_text = parsed_text.split("\n")
           parsed_text.pop(0)
           parsed_text = "\n".join(parsed_text)
           parsed_text = parsed_text.split(".")
           topic_models = main.lda.generate_topic_models(parsed_text)

           mining = arg_mining.MiningTools()
           args = mining.argument_word_match(parsed_text)
           claims = mining.claim_verb_match(args)
           topic_argument_relations = mining.calculate_soft_cosine_similarity(topic_models, claims)

           print("Complete!")

           number_of_claims = 0
           claims = []
           for relation in topic_argument_relations:
               number_of_claims += len(topic_argument_relations.get(relation))
               for claim in topic_argument_relations.get(relation):
                   claims.append(claim)

           essay_claims = self.read_essay_annotation(number)
           essay_premises = self.get_premises(number)
           matches = []
           premise_matches = []
           for ec in essay_claims:
               for claim in claims:
                   if ec in claim and claim not in matches:
                       matches.append(claim)
                   if ec == claim and claim not in matches:
                       matches.append(claim)
           for premise in essay_premises:
               for claim in claims:
                   if premise in claim and claim not in premise_matches and claim not in matches:
                       premise_matches.append(claim)
                   if premise == claim and claim not in premise_matches and claim not in matches:
                       premise_matches.append(claim)

           print("My claims: " + str(number_of_claims))
           print("Annotated claims: " + str(len(essay_claims)))
           print("Matches: " + str(len(matches)))

           total_claims = total_claims + number_of_claims
           total_annotated_claims = total_annotated_claims + len(essay_claims)
           total_matches = total_matches + len(matches)
           total_premise_matches = total_premise_matches + len(premise_matches)

           result_string = ""
           result_string += "Number of sentences in document: %d \n" % len(parsed_text)
           result_string += "Number of claims detected: %d \n" % number_of_claims
           f = open("essay_corpus_results.txt", "a")

           # construct gui
           x = 0
           for relation in topic_argument_relations:
               x = x + 1
               result_string += ("\nTOPIC %d " % x + "KEY WORDS: " + relation + "\n")
               result_string += ("Number of CLAIMS related to this TOPIC: %.d" % len(topic_argument_relations.get(relation))+ "\n")
               for claim in topic_argument_relations.get(relation):
                   result_string += ("\nCLAIM sentence: " + str(claim) + "\n")
           result_string += "Matches: " + str(len(matches))
           result_string += "Pickaxe claims: " + str(number_of_claims)
           result_string += "Annotated claims: " + str(len(essay_claims))

           self.write_output_file(result_string, number)
           f.close()
           i += 1
       print("Total Annotated Claims: " + str(total_annotated_claims))
       print("Total Agreements: " + str(total_matches))
       print("Total Claims Detected: " + str(total_claims))
       print("Total premises detected as claims: " + str(total_premise_matches))


    def read_txt(self, path, filename):
        data = pathlib.Path(path, filename)
        fp = open(data, 'r', encoding="utf8")
        data = fp.read()
        return data

    def write_output_file(self, output, number):
        filename = "essay_corpus_results" + str(number) + ".txt"
        path = r"C:\Users\ROSSA\PycharmProjects\pickaxe\output\\"
        path = path + filename
        text_file = open(path, "w")
        text_file.write(output)
        text_file.close()

    def read_essay_annotation(self, number):
        essay_name = "essay" + str(number) + ".ann"
        annotated_data = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\essays', essay_name)
        annotated_data = annotated_data.split("\n")
        claims = []
        for line in annotated_data:
            if "Claim" in line or "MajorClaim" in line:
                line = line.replace("T", "", 1)
                line = line.replace("Claim", "", 1)
                line = line.replace("Major", "", 1)
                line = line.replace("\t", "", 1)
                line = re.sub(r'\d+', '', line)
                line = " ".join(line.split())
                claims.append(line)
        return claims

    def get_premises(self, number):
        essay_name = "essay" + str(number) + ".ann"
        annotated_data = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\essays', essay_name)
        annotated_data = annotated_data.split("\n")
        premises = []
        for line in annotated_data:
            if "Premise" in line:
                line = line.replace("T", "", 1)
                line = line.replace("\t", "", 1)
                line = line.replace("Premise", "", 1)
                line = re.sub(r'\d+', '', line)
                line = " ".join(line.split())
                premises.append(line)
        return premises

    def get_all_essays(self):
     i = 1
     essay = ""
     while i < 91:
         number = i
         if i < 10:
            number = "0" + str(i)
         essay_name = "essay" + str(number) + ".txt"
         essay += self.essay_hack(essay_name)
         i = i+1
     filename = "all_essays.txt"
     path = r"C:\Users\ROSSA\PycharmProjects\pickaxe\main\\"
     path = path + filename
     text_file = open(path, "w")
     text_file.write(essay)
     text_file.close()

    def essay_hack(self, essay_name):
        data = self.read_txt(r'C:\Users\ROSSA\PycharmProjects\pickaxe\essays', essay_name)
        parsed_text = data.split("\n")
        parsed_text.pop(0)
        parsed_text = "\n".join(parsed_text)

        return parsed_text

    def read_json(self):
        data = self.read_txt(r"C:\Users\ROSSA\PycharmProjects\pickaxe\results\\", "margot_results.json")
        results = json.loads(data)

        result_list = results['document']

        claims = []
        for item in result_list:
            if item['claim_score'] >= item['evidence_score']:
                if 'claim' in item:
                    claims.append(item['text'])
                elif 'claim_evidence' in item:
                    claims.append(item['text'])
                else:
                    claims.append(item['text'])
        return claims

    def get_acc(self):
     i = 1
     claims = []
     matches = []
     premises = []
     premise_matches = []
     while i < 91:
        number = i
        if i < 10:
            number = "0" + str(i)
        claims = claims + self.read_essay_annotation(number)
        premises = premises + self.get_premises(number)
        i = i + 1
     margot_claims = self.read_json()
     print(len(premises))
     print(len(claims))
     print(len(margot_claims))
     for margot_claim in margot_claims:
         for annotated in claims:
             if margot_claim in annotated and margot_claim not in matches:
                 matches.append(margot_claim)
             if margot_claim == annotated and margot_claim not in matches:
                 matches.append(margot_claim)
             if annotated in margot_claim and margot_claim not in matches:
                 matches.append(margot_claim)

     for margot_claim in margot_claims:
         for premise in premises:
             if margot_claim in premise and margot_claim not in premise_matches:
                 premise_matches.append(margot_claim)
             if margot_claim == premise and margot_claim not in premise_matches:
                 matches.append(margot_claim)
             if premise in margot_claim and margot_claim not in premise_matches:
                 premise_matches.append(margot_claim)
         if margot_claim not in matches and margot_claim not in premise_matches:
             print(margot_claim)

     print("Matches: " + str(len(matches)))
     print("Premise matches: " + str(len(premise_matches)))

if __name__ == '__main__':
    if 'win' in sys.platform:
        windll.shcore.SetProcessDpiAwareness(1)
    main = Main()
    main.get_acc()
