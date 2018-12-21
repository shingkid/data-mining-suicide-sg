# Data Mining Approach to the Detection of Suicide in Social Media: A Case Study of Singapore
### IS470 Guided Research Project
In this research, we focus on the social phenomenon of suicide. Specifically, we perform social sensing on digital traces obtained from Reddit. We analyze the posts and comments in that are related to suicide. We perform natural language processing to better understand different aspects of human life that relate to suicide.

The poster paper for this project was accepted to the 2018 IEEE International Conference on Big Data.

## Data
The dataset consists of 406 submissions dating from July 2010 to November 2018 - of which 161 were deemed relevant to suicide and depression - and 9,010 comments (responding to the 161 submissions), that were crawled from https://www.reddit.com/r/singapore/ using the **PRAW API**. [Queries](resources/jashinsky.txt) were informed by previous work in *"Tracking suicide risk factors through Twitter in the US" by J. Jashinsky, S.H. Burton, C.L. Hanson, J. West, C. Giraud-Carrier, M.D. Barnes, and T. Argyle (2013)*.

All data was saved to CSV format and can be found in the `data` folder included in this repository.

### Sample
| | title | score | id | url | comms_num | created | body | author_name | query 
|---|---|---|---|---|---|---|---|---|---
| 0 | Update from the Depressed Asshole | 59 | 8vgrob | https://www.reddit.com/r/singapore/comments/8v... | 30 | 2018-07-02 23:26:04 | About 3-4 months ago, I posted on reddit about... | GramTooNoob | feel alone depressed
| 1 | Friends, family, acquaintances of someone who ... | 20 | 5scrdi | https://www.reddit.com/r/singapore/comments/5s... | 12 | 2017-02-06 22:45:00 | How did you feel then, and how has it affected... | depressings | friend suicide
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ...

## Setup
```
pip install -r requirements.txt
```

This repository was written in Python 3.7.0 and uses the following libraries heavily:
- Gensim
    LDA Mallet
    ```
    sudo apt-get install default-jdk
    sudo apt-get install ant
    git clone git@github.com:mimno/Mallet.git
    cd Mallet/
    ant
    ```
- GoogleTranslate
    (**Fix:** https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group)
    ```
    pip uninstall googletrans
    git clone https://github.com/BoseCorp/py-googletrans.git
    cd ./py-googletrans
    python setup.py install
    ```
- Spacy
    ```
    pip install spacy
    python3 -m spacy download en
    ```

## Scripts
The `crawl_reddit.py` script can:
1. `--s`: crawl submissions from the Singapore subreddit with terms from a vocabulary file,
2. `--l`: allow data labelling, and/or
3. `--c`: crawl for comments on the submissions labeled "relevant"

```
python crawl_reddit.py [optional flags]
```


The `preprocess.py` script prepares the data for topic modeling using Gensim or Scikit-learn

```
python preprocess.py --gensim --sklearn
```

## Visualization
Both Gensim and Scikit-learn implementations of LDA topic modeling can be run from their respective notebooks. The output plots from pyLDAvis can be found in the `plots` folder.

## Work-in-Progress
- [ ] Links embedded in posts (which domains? what are they about?)
- [ ] Sentiment analysis ([including emoticons and emojis, accounting for sarcasm](https://github.com/bfelbo/DeepMoji))
- [ ] POS-tagging
- [ ] Social network analysis

## Acknowledgements
`urlmarker.py` written by [@gruber](https://gist.github.com/gruber/8891611) was used to Regex match urls during data cleaning.

The `malletmodel2ldamodel()` method provided by [Roger Mähler](https://groups.google.com/forum/#!topic/gensim/ZesMoKZCf4c) is an improvement on Gensim's implementation for converting ldamallet to ldamodel.

Many thanks to Dr Kyong Jin Shim for her superb support and guidance.
