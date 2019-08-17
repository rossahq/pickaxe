from fuzzywuzzy import fuzz


class MiningTools:


    def argument_word_match(self, sentences):


        argumentative_words = ['argue', 'conclude', 'therefore']
        matches = []
        threshold = 0.8
        for sentence in sentences:
            for arg in argumentative_words:
                if arg in sentence:
                    matches.append(sentence)
        print(matches)

if __name__ == '__main__':
    main = MiningTools()
    main.argument_word_match(["it can be argued","i argue that x is true","we can then conclude", "whatever", "not an argument"])