Sentiment Analysis using Python 
======

Required Packages
-----------------
1. Pandas
2. Numpy
3. Matplotlib
4. Seaborn
5. Cartopy
6. Tweepy (important) 
7. TextBlob
8. NLTK

Suggested IDE
--------------
[Anaconda (Spyder)](https://www.continuum.io/downloads)

** IPython should be install with the Anaconda package


Installation
------------
The easiest way to install the latest version
is by using pip/easy_install to pull it from PyPI:

    pip install tweepy

You may also use Git to clone the repository from
Github and install it manually:

    git clone https://github.com/tweepy/tweepy.git
    cd tweepy
    python setup.py install

Python 2.6 and 2.7, 3.3 & 3.4 are supported.

Seaborn
	
	pip install seaborn
	
Cartopy
	
	pip install cartopy
	
TextBlob

	pip install textblob
	
NLTK
	
	pip install nltk
	
** Pandas, Numpy, Matplotlib will be installed with Anaconda 

Setup
-----

Make sure you the PYTHONPATH manager is pointing to the following:

	1. TextBlob
	2. Seaborn
	3. Tweepy
	4. candidate_list, private_keys, spam_detection
	>> if this does not work, copy and paste the libraries to ~/3.4/lib/python3.4/site-packages/