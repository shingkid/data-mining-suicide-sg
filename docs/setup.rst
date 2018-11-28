Setup
=====

::

    pip install -r requirements.txt

This repository was written in Python 3.7.0 and uses the following libraries heavily:

Gensim LDA Mallet
~~~~~~~~~~~~~~~~~

::

    sudo apt-get install default-jdk
    sudo apt-get install ant
    git clone git@github.com:mimno/Mallet.git
    cd Mallet/
    ant

GoogleTranslate
~~~~~~~~~~~~~~~
**Fix:**
https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group

::

    pip uninstall googletrans
    git clone https://github.com/BoseCorp/py-googletrans.git
    cd ./py-googletrans
    python setup.py install

Spacy
~~~~~

::

    pip install spacy
    python3 -m spacy download en
