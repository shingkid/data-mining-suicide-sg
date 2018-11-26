#!/usr/bin/env python

import argparse
import os
# import pprint
import random
import socket
import sys
import time

import numpy as np
import pandas as pd
import praw
from tqdm import tqdm

from utility import create_project_dir, file_to_set, get_date


def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def obtain_token():
    """Provide the program's entry point when directly executed."""
    print('Go here while logged into the account you want to create a '
        'token for: https://www.reddit.com/prefs/apps/')
    print('Click the create an app button. Put something in the name '
        'field and select the script radio button.')
    print('Put http://localhost:8080 in the redirect uri field and '
        'click create app')
    client_id = input('Enter the client ID, it\'s the line just under '
                    'Personal use script at the top: ')
    client_secret = input('Enter the client secret, it\'s the line next '
                        'to secret: ')
    commaScopes = input('Now enter a comma separated list of scopes, or '
                        'all for all tokens: ')

    if commaScopes.lower() == 'all':
        scopes = ['creddits', 'edit', 'flair', 'history', 'identity',
                'modconfig', 'modcontributors', 'modflair', 'modlog',
                'modothers', 'modposts', 'modself', 'modwiki',
                'mysubreddits', 'privatemessages', 'read', 'report',
                'save', 'submit', 'subscribe', 'vote', 'wikiedit',
                'wikiread']
    else:
        scopes = commaScopes.strip().split(',')

    reddit = praw.Reddit(client_id=client_id.strip(),
                        client_secret=client_secret.strip(),
                        redirect_uri='http://localhost:8080',
                        user_agent='praw_refresh_token_example')
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes, state, 'permanent')
    print('Now open this url in your browser: '+url)
    sys.stdout.flush()

    client = receive_connection()
    data = client.recv(1024).decode('utf-8')
    param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
    params = {key: value for (key, value) in [token.split('=')
                                            for token in param_tokens]}

    if state != params['state']:
        send_message(client, 'State mismatch. Expected: {} Received: {}'
                    .format(state, params['state']))
    elif 'error' in params:
        send_message(client, params['error'])

    refresh_token = reddit.auth.authorize(params['code'])
    send_message(client, 'Refresh token: {}'.format(refresh_token))

    return reddit


def crawl_submissions(reddit, words, subreddit_name):
    """Crawls submissions from r/Singapore
    
    Parameters
    ----------
    reddit : Reddit
        Reddit instance after authentication
    words : set
        set of words from a vocabulary file
    subreddit_name : str
        name of subreddit, e.g. Singapore

    Returns
    -------
    submissions : DataFrame
        DataFrame of crawled submissions
    """
    print("Crawling submissions...")
    t0 = time.time()
    subreddit = reddit.subreddit(subreddit_name)
    submissions = pd.DataFrame(columns=['title', 'score', 'id', 'url', 'comms_num', 'created', 'body', 'author_name', 'query'])
    for word in tqdm(words):
        subreddit_query = subreddit.search(word)

        if subreddit_query:
            topics_dict = {
                "title":[],
                "score":[],
                "id":[],
                "url":[],
                "comms_num": [],
                "created": [],
                "body": [],
                "author_name": [],
#                 "reports_num":[],
                "query": []
            }

            for submission in subreddit_query:
                topics_dict["title"].append(submission.title)
                topics_dict["score"].append(submission.score)
                topics_dict["id"].append(submission.id)
                topics_dict["url"].append(submission.url)
                topics_dict["comms_num"].append(submission.num_comments)
                topics_dict["created"].append(get_date(submission.created))
                topics_dict["body"].append(submission.selftext[:-3])
                topics_dict["author_name"].append(submission.author.name)
#                 topics_dict["reports_num"].append(submission.num_reports)
                topics_dict["query"].append(word)

            submissions = pd.concat([submissions, pd.DataFrame(topics_dict)])
    print("Seconds:", time.time()-t0)

    submissions.drop_duplicates('id', inplace=True)
    submissions.reset_index(inplace=True)
    submissions.drop(columns=['index'], inplace=True)

    print(submissions)
    sub_path = os.path.join('../data', 'submissions.csv')
    if os.path.isfile(sub_path):
        replace = input("File already exists. Replace %s? [y/n]" % sub_path)
        if replace=='y':
            print("Saving to %s" % sub_path)
            submissions.to_csv(sub_path, index=False)
    else:
        print("Saving to %s" % sub_path)
        submissions.to_csv(sub_path, index=False)

    return submissions


def remove_irrelevant_posts():
    """Manually screen through every submission and determine its relevance"""
    filename = os.path.join('../data', 'submissions.csv')
    if not os.path.isfile(filename):
        print("Need to crawl for submissions first.")
        exit()

    df = pd.read_csv(filename)
    print("No. of submissions:", df.shape[0])
    for index, row in df.iterrows():
        print(index, 'Query:', row.query)
        print('Title:', row.title)
        keep = input("Keep submission [y/n] (Enter 'more' to see body): ")
        if keep=='more':
            print(row.body)
            keep = input('Keep submission [y/n]: ')
        
        if keep=='n':
            df.at[index, 'relevant'] = True
        else:
            df.at[index, 'relevant'] = False
    
    df = df.replace(np.nan, '', regex=True)
    print(df)
    path = os.path.join('../data', 'submissions-clean.csv')
    print("Saving to %s" % path)
    df.to_csv(path, index=False)

    return df


def crawl_comments(reddit):
    """Crawl comments on submissions labeled 'relevant'
    
    Parameters
    ----------
    reddit : Reddit
        Reddit instance after authentication

    Returns
    -------
    comments : DataFrame
        DataFrame of crawled comments
    """
    filename = os.path.join('../data', 'submissions-clean.csv')

    if not os.path.isfile(filename):
        print("You have not cleaned your submissions.")
        exit()

    print("Crawling comments...")
    t0 = time.time()
    df = pd.read_csv(filename)
    comments = []
    for index, row in df[df.relevant].iterrows():
        submission_id = row.id
        submission = praw.models.Submission(reddit, id=submission_id)
        print(index, "Submission:", row.id, "Num comments:", submission.num_comments)
        comment_forest = submission.comments
        submission.comments.replace_more(limit=None)
        for comment in comment_forest.list():
    #         pprint.pprint(vars(comment))
            redditor_name = ""    
            if comment.author:
                redditor_name = comment.author.name
    #             pprint.pprint(vars(comment.author))
            comments.append([submission_id, comment.id, comment.body, comment.score, redditor_name, get_date(comment.created), comment.parent().id])
    print("Seconds:", time.time()-t0)

    comments = pd.DataFrame(comments, columns=['submission_id', 'id', 'body', 'score', 'author_name', 'created', 'parent'])

    com_path = os.path.join('../data', 'comments.csv')
    if os.path.isfile(com_path):
        replace = input("File already exists. Replace %s? [y/n]" % com_path)
        if replace=='y':
            print("Saving to %s" % com_path)
            comments.to_csv(com_path, index=False)
    else:
        print("Saving to %s" % com_path)
        comments.to_csv(com_path, index=False)

    return comments


def main():
    prog = "crawl_reddit"
    descr = "Scrape and crawl r/Singapore"
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument("--s", help="Crawl submissions", action="store_true")
    parser.add_argument("--l", help="Label submissions", action="store_true")
    parser.add_argument("--c", help="Crawl comments", action="store_true")
    args = parser.parse_args()

    if args.s or args.c:
        reddit = obtain_token()

    if args.s:
        vocab_file_path = input('Enter path to vocabulary file: ')
        while not os.path.isfile(vocab_file_path):
            vocab_file_path = input('Invalid file. Enter path to vocabulary file: ')
        words = file_to_set(vocab_file_path)
        crawl_submissions(reddit, words, 'Singapore')

    if args.l:
        remove_irrelevant_posts()

    if args.c:
        crawl_comments(reddit)

    DATA_DIR = '../data'
    merged_path = os.path.join(DATA_DIR, 'merged.csv')
    sub_path = os.path.join(DATA_DIR, 'submissions-clean.csv')
    com_path = os.path.join(DATA_DIR, 'comments.csv')
    print(not os.path.isfile(merged_path), os.path.isfile(sub_path), os.path.isfile(com_path))
    if not os.path.isfile(merged_path) and os.path.isfile(sub_path) and os.path.isfile(com_path):
        submissions = pd.read_csv(sub_path)
        submissions = submissions[submissions.relevant]
        print(submissions)
        comments = pd.read_csv(com_path)
        comments.rename(columns={'body': 'content'}, inplace = True)
        print(comments)
        submissions['content'] = submissions.title.map(str) + ' ' + submissions.body.map(str)
        df = pd.concat([submissions, comments])
        df = df[['id', 'author_name', 'content']]
        print(df)
        print("Saving to %s" % merged_path)
        df.to_csv(merged_path, index=False)


if __name__ == "__main__":
    main()