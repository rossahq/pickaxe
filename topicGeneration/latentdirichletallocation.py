import inline as inline
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import os
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

def create_topic_model():


    print(paper.read())

# paper['paper_text_processed'] = paper['paper_text'].map(lambda x: re.sub('[,\.!?]', '', x))

def plot_10_most_common_words(count_data, count_vectorizer):
    import matplotlib.pyplot as plt
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

def run():

    data = pathlib.Path(r'C:\Users\ROSSA\PycharmProjects\pickaxe\test', 'test.txt')
    paper = open(data, 'rb')
    count_vectorizer = CountVectorizer(stop_words='english')  # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(paper)  # Visualise the 10 most common words
    plot_10_most_common_words(count_data, count_vectorizer)


if __name__ == '__main__':

    run()