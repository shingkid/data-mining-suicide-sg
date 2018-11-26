#!/usr/bin/env python

import datetime as dt
import os

import pandas as pd


def file_to_set(file_name):
    """Read a file and convert each line to set of items"""
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def create_project_dir(directory):
    """Each website is a separate project (folder)"""
    # If specified directory does NOT exist, then create one.
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory) # makedirs --> make directory


def get_date(created):
    """Convert timestamp to date"""
    return dt.datetime.fromtimestamp(created)
