from collections import Counter

import nltk
from nltk.tokenize import word_tokenize

nltk.download('wordnet')  # download if using this module for the first time

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')  # download if using this module for the first time


def mostCommonTopics(fileName):
    """
    Return the top 10 most common topics from a file of yaks

    :param fileName: TXT file of parsed yik yaks
    :return: List of top 10 most common topics with their count
    """
    with open(fileName) as file:
        yaks = file.read()

    yik_yak_token_to_ignore = {"comment", "share"}

    tokens = word_tokenize(yaks)
    lowercase_tokens = [t.lower() for t in tokens if t.isalpha()]

    stopwords_removed = [t for t in lowercase_tokens if
                         t not in stopwords.words("english") and t not in yik_yak_token_to_ignore]

    # Shorten words to their roots or stems
    lemmatizer = WordNetLemmatizer()
    lem_tokens = [lemmatizer.lemmatize(t) for t in stopwords_removed]

    word_counts = Counter(lem_tokens)

    return word_counts.most_common(10)


mostCommonTopics("yak-text-11-23-13-26-04.txt")
