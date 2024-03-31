#  Word Similarity with MapReduce

This project implements a MapReduce job for calculating word similarity based on Term Frequency-Inverse Document Frequency (TF-IDF) using MrJob library.

## Overview

This MapReduce job is designed to analyze a collection of articles and calculate the TF-IDF score for each word. It preprocesses the text, calculates TF and IDF values, and finally computes the TF-IDF score. The job also provides the functionality to calculate the TF-IDF score for user-provided query words and compute the similarity scores.

## Dependencies

- [MrJob](https://github.com/Yelp/mrjob)
- [NLTK](https://www.nltk.org/)
- [pandas](https://pandas.pydata.org/)

## Usage

1. Install the required dependencies:

    ```bash
    pip install mrjob nltk pandas
    ```

2. Download necessary NLTK resources:

    ```python
    import nltk
    nltk.download('wordnet')
    nltk.download('stopwords')
    ```

3. Run the MapReduce job:

    ```bash
    python mr_word_similarity.py --num-articles <num_articles> --query "<search_query>"
    ```

    Replace `<num_articles>` with the desired number of articles to check and `<search_query>` with the search query.

## Contributors

- 22i-1979 Abdulrehman
- 22i-1959 Ismael Hafeez
- 22i-1880 Saad Iftikhar
