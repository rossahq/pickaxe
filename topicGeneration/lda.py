from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import subprocess
from nltk.corpus import stopwords
from nltk import download
import seaborn as sns
import re
download('stopwords')  # Download stopwords list.
sns.set_style('whitegrid')


def generate_topic_models(sentences):
    x = 0
    working_sents = sentences
    while x < len(working_sents) - 1:
        #remove digits from text e.g 2006
        clean_sentence = re.sub(r'\d+', '', working_sents[x])
        working_sents[x] = clean_sentence
        x = x + 1
    count_vectorizer = CountVectorizer(stop_words='english')  # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(working_sents)

    # Tweak the two parameters below (use int values below 15)
    number_topics = 5
    number_words = 7

    # Create and fit the LDA model
    lda = LDA(n_components=number_topics)
    lda.fit(count_data)
    print("Topics found via LDA:")

    topics = get_topics(lda, count_vectorizer, number_words)
    print(str(topics))
    return topics


def get_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topic = " ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])
        topics.append(topic)
    return topics


def generate_lda_topic_model(sentences):

    # create_dat_file(sentences)

    subprocess.call(['java', '-mx512M', '-cp', 'C:/Users/ROSSA/PycharmProjects/pickaxe/topicModellingResources/JGibbLDA-v.1.0/bin;C:/Users/ROSSA/PycharmProjects/pickaxe/topicModellingResources/JGibbLDA-v.1.0/lib/args4j-2.0.6.jar',
                     'jgibblda.LDA', '-est', '-ntopics', '5','-twords', '7',
                     '-dir', 'C:/Users/ROSSA/PycharmProjects/pickaxe/test', '-dfile',
                     'output.dat'])


def create_dat_file(sentences):
    x = 0
    working_sents = sentences
    while x < len(working_sents) - 1:
        #remove digits from text e.g 2006
        clean_sentence = re.sub(r'\d+', '', working_sents[x])
        working_sents[x] = clean_sentence
        x = x + 1
    for sentence in sentences:
        stop_words = stopwords.words('english')
        sentence = [w for w in sentence if w not in stop_words]




if __name__ == '__main__':
    generate_lda_topic_model()
