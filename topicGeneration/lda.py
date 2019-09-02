from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


def generate_topic_models(document):

    #data = pathlib.Path(path, filename)
    #document = open(data, 'rb')
    count_vectorizer = CountVectorizer(stop_words='english')  # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(document)  # Visualise the 10 most common words
    #plot_10_most_common_words(count_data, count_vectorizer)

    # Tweak the two parameters below (use int values below 15)
    number_topics = 5
    number_words = 8

    # Create and fit the LDA model
    lda = LDA(n_components=number_topics)
    lda.fit(count_data)
    print("Topics found via LDA:")

    topics = get_topics(lda, count_vectorizer, number_words)
    return topics

def plot_10_most_common_words(count_data, count_vectorizer):

    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts += t.toarray()[0]

    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x: x[1], reverse=True)[0:10]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    plt.subplot(title='10 most common words')
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90)
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.show()  # Initialise the count vectorizer with the English stop words


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