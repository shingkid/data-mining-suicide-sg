#!/usr/bin/env python

import datetime as dt
import json
import os
import re
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from gensim.utils import simple_preprocess
import spacy

import urlmarker


def file_to_set(file_name):
    """Read a file and convert each line to set of items
    
    Args:
        file_name (str): name of file
    
    Returns:
        results (set): set of words from file
    """
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def create_project_dir(directory):
    """Each website is a separate project (folder)
    
    Args:
        directory (str): name of directory to be created
    """
    # If specified directory does NOT exist, then create one.
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory) # makedirs --> make directory


def get_date(created):
    """Convert timestamp to date
    
    Args:
        created (datetime): raw timestamp from Reddit
    
    Returns:
        (datetime): formatted datetime
    """
    return dt.datetime.fromtimestamp(created)


def extract_url_domains(df):
    """Extract netloc attribute for urls found and save to JSON

    Args:
        df (DataFrame): DataFrame of all Reddit posts
    """
    url_dict = {}
    for index, row in df.iterrows():
        urls = re.findall(urlmarker.WEB_URL_REGEX, str(row.content))
        for url in urls:
            domain = urlparse(url).netloc
            if domain!='':
                url_dict[url] = domain

    with open('../resources/urls.json', 'w') as file:
        json.dump(url_dict, file)


def sent_to_words(sentences):
    """Convert sentences to list of words

    Args:
        sentences (list): list of text from Reddit posts
    
    Yields:
        (str): a preprocessed word
    """
    for sentence in sentences:
        yield(simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def remove_stopwords(stop_words, texts):
    """Remove stopwords from text
    
    Args:
        stop_words (list): list of stop words
        texts (list): 2-dimensional list of words

    Returns:
        (list): list words excluding stop words
    """
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def make_bigrams(bigram_mod, texts):
    """Form bigrams in text
    
    Args:
        bigram_mod (gensim.models.phrases.Phraser): Gensim bigram model
        texts (list): 2-dimensional list of words

    Returns:
        (list): bigrams formed from texts
    """
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(bigram_mod, trigram_mod, texts):
    """Form trigrams in text
    
    Args:
        trigram_mod (gensim.models.phrases.Phraser): Gensim trigram model
        texts (list): 2-dimensional list of words

    Returns:
        (list): trigrams formed from texts
    """
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, dtype, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """Perform lemmatization
    
    Args:
        texts (list): 2-dimensional list of words
        dtype (str): Data type in which to return - 'list' or 'str'
        allowed_postags (list): allowed POS-tags

    Returns:
        texts_out (list): 2-dimensional lemmatized list of words
    """
    # https://spacy.io/api/annotation
    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    nlp = spacy.load('en', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        if dtype=='list':
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        elif dtype=='str':
            texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))

    # Write to file
    print("Saving to .npy file...")
    with open('../resources/data-clean-%s.npy' % dtype, 'wb') as outfile:
        np.save(outfile, np.array(texts_out))

    return texts_out
