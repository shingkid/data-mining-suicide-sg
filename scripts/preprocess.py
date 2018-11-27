#!/usr/bin/env python

import argparse
import json
import numpy as np
import os
import pandas as pd
from pprint import pprint
import re
from tempfile import TemporaryFile
outfile = TemporaryFile()

# Gensim
from gensim import corpora, models

# Googletrans
from googletrans import Translator
translator = Translator()

# NLTK
from nltk.corpus import stopwords

import utility as util
import urlmarker


def clean(data, dtype=list):
    # NLTK Stop words
    stop_words = stopwords.words('english')
    stop_words.extend(['singaporean', 'singapore', 'like', 'get', 'know', 'http', 'com', 'www', 'sg', 'r', 'reddit'])

    # Replace multiple consecutive whitespaces
    data = [re.sub('\s+', ' ', str(post)) for post in data]

    # Remove single quotation
    data = [re.sub("\'", "", str(post)) for post in data]

    # Remove zero width space
    data = [re.sub(r'&#x200B;', '', str(post)) for post in data]

    # Remove non-breaking space
    data = [re.sub(r'&nbsp;', '', post) for post in data]

    # TODO: Extract domain
    # Replace links with 'URL' token
    data = [re.sub(urlmarker.WEB_URL_REGEX, 'url', post) for post in data]

    # Translate Chinese to English
    with open('../resources/chinese.json') as f:
        chinese_dict = json.load(f)

    for i in range(len(data)):
        chinese = re.findall(u'[\u4e00-\u9fff]+', data[i])
        if chinese:
            # print(chinese)
            for ch in chinese:
                # print(ch)
                if ch in chinese_dict.keys():
                    en = chinese_dict[ch]
                else:
                    en = translator.translate(ch).text
                # print(en)
                data[i] = re.sub(u'[\u4e00-\u9fff]+', en, data[i])

    # TODO: Handle sarcasm

    # Convert sentences to list of words
    data_words = list(util.sent_to_words(data))

    # Build the bigram and trigram models
    bigram = models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = models.phrases.Phraser(bigram)
    trigram_mod = models.phrases.Phraser(trigram)

    # Remove Stop Words
    data_words_nostops = util.remove_stopwords(stop_words, data_words)

    # Form Bigrams
    data_words_bigrams = util.make_bigrams(bigram_mod,data_words_nostops)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = util.lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'], dtype=dtype)

    # Write to file
    print("Saving to .npy file...")
    with open('../resources/data-clean.npy', 'wb') as outfile:
        np.save(outfile, np.array(data_lemmatized))


def main():
    prog = "preprocess"
    descr = "Scrape and crawl r/Singapore"
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument("--gensim", help="Use Gensim topic modeling", action="store_true")
    parser.add_argument("--sklearn", help="Use Scikit-learn topic modeling", action="store_true")
    args = parser.parse_args()

    content_path = os.path.join('../resources', 'content.npy')
    if not os.path.isfile(content_path):
        df = pd.read_csv('../data/merged.csv')
        print(df.shape)
        df = df[df.content!='[removed]']
        print(df.shape)
        df = df[df.content!='[deleted]']
        print(df.shape)
        data = df.content.values.tolist()
        print("Saving to .npy file...")
        with open(content_path, 'wb') as outfile:
            np.save(outfile, np.array(data))
    else:
        with open(content_path, 'rb') as infile:
            data = np.load(infile)

    print(args.gensim, args.sklearn)
    if args.gensim:
        clean(data)
    
    if args.sklearn:
        clean(data, dtype=str)
