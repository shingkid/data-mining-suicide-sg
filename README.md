# Data Mining Approach to the Detection of Suicide in Social Media: A Case Study of Singapore
### IS470 Guided Research Project
In this research, we focus on the social phenomenon of suicide. Specifically, we perform social sensing on digital traces obtained from Reddit. We analyze the posts and comments in that are related to suicide. We perform natural language processing to better understand different aspects of human life that relate to suicide.

## Data
The dataset consists of 406 submissions - of which 161 were deemed relevant to suicide and depression - and 9,010 comments (responding to the 161 submissions), that were crawled from https://www.reddit.com/r/singapore/ using the **PRAW API**. [Queries](resources/jashinsky.txt) were informed by previous work in *"Tracking suicide risk factors through Twitter in the US" by J. Jashinsky, S.H. Burton, C.L. Hanson, J. West, C. Giraud-Carrier, M.D. Barnes, and T. Argyle (2013)*.

All data was saved to CSV format and can be found in the `data` folder included in this repository.

## Dependencies
This repository was written in Python 3.7.0 and uses the following libraries heavily:
- Gensim
- GoogleTranslate (**Fix**: git clone and install from https://github.com/BoseCorp/py-googletrans.git)
- Pandas
- PRAW
- pyLDAvis

## Scripts
The `crawl_reddit.py` script can:
1. `--s`: crawl submissions from the Singapore subreddit with terms from a vocabulary file,
2. `--l`: allow data labelling, and/or
3. `--c`: crawl for comments on the submissions labeled "relevant"

```
python crawl_reddit.py [optional flags]
```

## Work-in-Progress
- [ ] Links embedded in posts (which domains? what are they about?)
- [ ] Sentiment analysis (including emoticons and emojis, accounting for sarcasm)
- [ ] POS-tagging
- [ ] Social network analysis

## Acknowledgements
`urlmarker.py` provided by @gruber was used to Regex match urls during data cleaning.
