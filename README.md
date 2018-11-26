# IS470 Guided Research Project
### Data Mining Approach to the Detection of Suicide in Social Media: A Case Study of Singapore
In this research, we focus on the social phenomenon of suicide. Specifically, we perform social sensing on digital traces obtained from Reddit. We analyze the posts and comments in that are related to suicide. We perform natural language processing to better understand different aspects of human life that relate to suicide.

## Data
The dataset consists of 406 submissions - of which 161 were deemed relevant to suicide and depression - and 9010 comments (responding to the 161 submissions), that were crawled from https://www.reddit.com/r/singapore/ using the PRAW API. Queries (see `vocab/jashinsky.txt`) were informed by previous work in *"Tracking suicide risk factors through Twitter in the US" by J. Jashinsky, S.H. Burton, C.L. Hanson, J. West, C. Giraud-Carrier, M.D. Barnes, and T. Argyle (2013)*. All data was saved to CSV format and can be found in the `data` folder included in this repository.

## Scripts
The `crawl_reddit.py` script can either [1] crawl submissions from the Singapore subreddit with terms from a vocabulary file, [2] allow data labelling, or [3] crawl for comments on the submissions labeled "relevant".

```
python crawl_reddit.py [1, 2, or 3]
```
