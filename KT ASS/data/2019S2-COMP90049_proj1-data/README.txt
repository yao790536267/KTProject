This README describes the data files for COMP90049 2019S2, Project 1. 
This archive contains six files, of which the dictionary, candidate, and blend files
form the central data sources for this Project, although you may be interested in the
other files in some circumstances. These file present in this archive are described in
more detail below.


  - dict.txt: This is a list of approximately 370K English entries, which should
    comprise the dictionary for your approximate string search method(s). This
    dictionary is a slightly-altered version of the data from:
    https://github.com/dwyl/english-words
    The format of this file is one entry per line, in alphabetical order.
    You may use a different dictionary if you wish; if so, you should state
    the data source and justification in your report.

  - tweets.txt: This is a list of the text from 62345 tweets, one tweet per line.
    (The ordering is random.)

  - wordforms.txt: This is an alphabetically-sorted list of 31763 unique tokens present
    within the tweets.
    To construct this list, the tweets were separated based on one (or more) characters
    of whitespace (\s), and tokens not consisting entirely of English alphabetic
    characters (^[a-zA-Z]+$) were excluded.
    Obviously, there are better ways in which the tweets could be tokenised; this 
    was intentionally simplistic.

  - candidates.txt: This is the list of 16925 tokens present in wordforms.txt, except
    that any token appearing in the dictionary has been excluded.
    One logical framework for the problem of finding lexical blends is that any token
    not present within the dictionary is potentially a blend. Note that there are other
    possible strategies, but we have structured this Project specifically so that
    blends do not appear in the dictionary (which may not be true for data in general).

  - blends.txt: This is a tab-delimited list of tokens appearing in the tweets,
    which have been manually identified as being lexical blends.
    Each line takes the form: blend token, tab character, component word, tab character,
    component word, newline.
    Note that some of the blends do not appear in the candidates list, because they have
    been excluded in the preprocessing stage. You might be interested to try out other
    preprocessing strategies instead.
    Note that some of the tokens in the tweets may be blends that are not listed in
    blends.txt; we make no guarantees that this file represents an exhaustive list,
    only that these tokens have indeed been identified as blends.

  - README.txt: This is the file that you are currently reading.
