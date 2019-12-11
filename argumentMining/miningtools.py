from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import WordEmbeddingSimilarityIndex
from nltk.corpus import stopwords
from gensim import corpora
from nltk import download
from gensim.similarities import SparseTermSimilarityMatrix
import gensim.downloader as api
from nltk.corpus import wordnet
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
download('stopwords')  # Download stopwords list.
download('wordnet')  # Download WordNet lexical database
syns = wordnet.synsets('program')


class MiningTools:

    def argument_word_match(self, sentences):
        # source for argumentative words & phrases list is:
        # https://www.academia.edu/3296265/Using_linguistic_phenomena_to_motivate_a_set_of_coherence_relations
        # move to json
        argumentative_words = [
                               'by the same token', 'by the way', 'certainly', 'clearly', 'consequently', 'conversely',
                               'correspondingly', 'despite that',
                               'despite the fact that', 'earlier', 'either', 'else', 'equally', 'essentially then',
                               'even', 'even so', 'even then', 'eventually',
                               'every time', 'except', 'except', 'insofar as', 'finally', 'first', 'first of all',
                               'firstly', 'for', 'for a start', 'for example', 'for instance', 'for one thing',
                               'for the simple reason', 'for this reason', 'further', 'furthermore', 'given that',
                               'hence', 'however', 'if',
                               'if ever', 'if not', 'if only', 'if so', 'in a different vein', 'in actual fact',
                               'in addition', 'in any case', 'in case', 'in conclusion',
                               'in contrast', 'in fact', 'initially', 'in other words', 'in particular', 'in short',
                               'in spite of that', 'in sum',
                               'in that case', 'in the beginning', 'in the case of ', 'in the end', 'in the _rst place',
                               'in the meantime', 'in this way', 'in turn',
                               'inasmuch as', 'incidentally', 'indeed', 'instead', 'it follows that',
                               'it might appear that', 'it might seem that', 'just as',
                               'last', 'lastly', 'later', 'let us assume', 'likewise', 'meanwhile', 'merely',
                               'merely because', 'moreover', 'much later',
                               'much sooner', 'naturally', 'neither is it the case', 'nevertheless', 'no doubt',
                               'nonetheless', 'not', 'not because', 'not only',
                               'not that', 'notably', 'notwithstanding that', 'now', 'now that', 'obviously',
                               'of course', 'on condition that', 'on one hand', 'on one side', 'on the assumption that',
                               'on the contrary', 'on the grounds that', 'on the one hand', 'on the one side',
                               'on the other hand', 'on the other side', 'once', 'once again',
                               'once more', 'or', 'or else', 'otherwise', 'overall', 'plainly', 'presumably because',
                               'previously', 'provided that', 'providing that',
                               'put another way', 'rather', 'reciprocally', 'regardless of that', 'second', 'secondly',
                               'similarly', 'simply because', 'simultaneously', 'since', 'so', 'so that',
                               'specifically', 'still', 'subsequently', 'such that', 'summarising', 'summing up',
                               'suppose', 'suppose that', 'supposing that', 'sure enough', 'surely', 'that is',
                               'that is to say', 'the fact is that', 'the more often', 'then', 'then again',
                               'thereafter', 'thereby', 'therefore', 'third', 'thirdly', 'this time', 'though',
                               'thus', 'to be sure', 'to begin with', 'to conclude', 'to start with', 'to sum up',
                               'to summarise', 'to take an example', 'to the degree that', 'to the extent that', 'too',
                               'true', 'we might say', 'what is more',
                               'when', 'whenever', 'where', 'whereas', 'wherein', 'wherever', 'while ,yet']

        matches = []
        for sentence in sentences:
            for arg in argumentative_words:
                if arg in sentence and sentence not in matches:
                    matches.append(sentence)
        print("number of sentences: %d" % sentences.__len__())
        print("number of argument phrases & word matches: %d" % matches.__len__())

        return matches

    def claim_verb_match(self, sentences):
        verbs = ['required', 'identified', 'argued', 'needed', 'stated', 'failed', 'agreed', 'judged', 'suggested',
                 'felt', 'considered', 'should', "consider", "discussed", "reported", "believe", "believed", "thought",
                 "explained", "ensure", "demonstrates", "support", 'believe', 'conclude']

        matches = []
        for sentence in sentences:
            for verb in verbs:
                if verb in sentence and sentence not in matches:
                    matches.append(sentence)
                else:
                    for syn in wordnet.synsets(verb):
                        for lemma in syn.lemmas():
                            if lemma.name() in sentence and sentence not in matches:
                                matches.append(sentence)

        print("verb matches: %d" % len(matches))

        return matches

    def calculate_soft_cosine_similarity(self, topic_models, sentences, *args, **kwargs):

        topic_claim_relations = {}
        for topic in topic_models:
            topic_claim_relations[topic] = []

        documents = []
        for topic in topic_models:
            documents.append(topic.lower().split())
        for sentence in sentences:
            documents.append(sentence.lower().split())
        dictionary = corpora.Dictionary(documents)

        w2v_model = api.load("glove-wiki-gigaword-100")
        similarity_index = WordEmbeddingSimilarityIndex(w2v_model)
        similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary)

        for sentence in sentences:
            best_cosine_result = 0
            x = 0
            normal_sentence = sentence
            sentence = sentence.lower().split()

            stop_words = stopwords.words('english')
            sentence = [w for w in sentence if w not in stop_words]

            while x <= len(topic_models) - 1:

                topic_model = (topic_models[x]).lower().split()
                topic_model = [w for w in topic_model if w not in stop_words]

                topic_model_bow = dictionary.doc2bow(topic_model)
                sentence_bow = dictionary.doc2bow(sentence)

                similarity = similarity_matrix.inner_product(topic_model_bow, sentence_bow, normalized=True)
                print('similarity = %.4f' % similarity)

                if similarity > best_cosine_result:
                    best_cosine_result = similarity
                    matched_topic = topic_models[x]

                if x == len(topic_models) - 1:
                    if best_cosine_result > 0.3:
                        topic_claim_relations[matched_topic].append(normal_sentence)

                x = x + 1
        return topic_claim_relations


if __name__ == '__main__':
    tools = MiningTools()
    tools.calculate_expanded_cosine_similarity("identified")
