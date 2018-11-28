Scripts
=======

The ``crawl_reddit.py`` script can:
1. ``--s``: crawl submissions from the Singapore subreddit with terms from a vocabulary file,
2. ``--l``: allow data labelling, and/or
3. ``--c``: crawl for comments on the submissions labeled "relevant".

::

    python crawl_reddit.py [optional flags]

The ``preprocess.py`` script prepares the data for topic modeling using Gensim or Scikit-learn.

::

    python preprocess.py --gensim --sklearn

.. toctree::
   :maxdepth: 4

   crawl_reddit
   preprocess
   utility
