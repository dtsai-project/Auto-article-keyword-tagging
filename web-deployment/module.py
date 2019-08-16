import nltk
import re
from nltk import (
    word_tokenize,
    sent_tokenize,
    probability,
    corpus,
    util,
    stem
)

from nltk.util import (
    bigrams,
    trigrams,
    ngrams
)

from nltk.stem import (
    wordnet,
    WordNetLemmatizer
)


def tokenization(words):
    out_word = word_tokenize(words)
    fdist = probability.FreqDist(out_word)
    return fdist, out_word


def process(sentences):
    hamlet = sentences
    hamlet = hamlet.split(" ")
    new_hamlet = []
    for word in hamlet:
        new_hamlet.append(word)
    hamlet_data = ' '.join(new_hamlet)

    fdist, tokenized = tokenization(hamlet_data)
    stemmer = stem.PorterStemmer()
    stemmed_out = [stemmer.stem(word) for word in new_hamlet]
    stemmed_out_join = ' '.join(stemmed_out)

    lemmitaizers = []
    words_to_lem = stemmed_out
    word_lem = WordNetLemmatizer()
    ls_word_lem = []
    for words in words_to_lem:
        ls_word_lem.append(word_lem.lemmatize(words))
        out = str(words+" "+"=>"+" "+word_lem.lemmatize(words))
        lemmitaizers.append(out)

    punctuation = re.compile(r"[.,:;&-?!()|0-9]")
    post_punctuation = []
    for words in ls_word_lem:
        word = punctuation.sub("", words)
        if len(word) > 0:
            post_punctuation.append(word)

    # menghilangkan kata2 yang kurang bermakna seperti i, me , you dll
    # stops = corpus.stopwords.words("english")
    # final_hamlet = []
    # for idx, word in enumerate(post_punctuation):
    #     if word in stops:
    #         stops.remove(word)
    #     else:
    #         final_hamlet.append(word)

    punctuation = re.compile(r"[.,:;&-?!()|0-9]")
    post_punctuation = []
    for words in ls_word_lem:
        word = punctuation.sub("", words)
        if len(word) > 0:
            post_punctuation.append(word)

    # menghilangkan kata2 yang kurang bermakna seperti i, me , you dll
    stops = corpus.stopwords.words("english")
    final_hamlet = []
    for idx, word in enumerate(post_punctuation):
        if word in stops:
            stops.remove(word)
        else:
            final_hamlet.append(word)

    cleaned_story = []
    thrash = ["the", "a", "of", "in", "is", "to", "wa", "he", "she",
              "hi", "it", "from", "by", "with", "In", "for", "that", "who", "and"]
    for word in final_hamlet:
        if word in thrash or '\n\n' in word:
            final_hamlet.remove(word)
        else:
            cleaned_story.append(word)

    final_hamlet_join = ' '.join(cleaned_story)
    fdist_, tokenized_ = tokenization(final_hamlet_join)
    print("ini tokenized : \n", tokenized_, fdist_)
    fdist_top10_ = fdist_.most_common(10)

    store = []
    for fd, num in fdist_top10_:
        store.append(fd)
    return store
