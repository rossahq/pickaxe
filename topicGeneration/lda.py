from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import subprocess
import seaborn as sns
import re
sns.set_style('whitegrid')


def generate_topic_models(sentences):
    x = 0
    while x < len(sentences) - 1:
        #remove digits from text e.g 2006
        clean_sentence = re.sub(r'\d+', '', sentences[x])
        sentences[x] = clean_sentence
        x = x + 1
    print(sentences)
    count_vectorizer = CountVectorizer(stop_words='english')  # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(sentences)

    # Tweak the two parameters below (use int values below 15)
    number_topics = 3
    number_words = 5

    # Create and fit the LDA model
    lda = LDA(n_components=number_topics)
    lda.fit(count_data)
    print("Topics found via LDA:")

    topics = get_topics(lda, count_vectorizer, number_words)
    return topics


def get_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        #print("\nTopic #%d:" % topic_idx)
        topic = " ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])
        topics.append(topic)
    print(topics)
    return topics

def generate_lda_topic_model():
    subprocess.call(['java', '-jar', ''])