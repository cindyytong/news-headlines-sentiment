# How Negative Are Our News Headlines



## Overview
Every day we are bombarded with breaking news.  Another tragedy is just seconds away. Is this the result of our own biases towards the news or could it be due to specific news sources prioritizing negative content? Just how negative have our news sources become? 

This project attempts to answer the following questions:
* On average, how negative have our news sources become? 
* Do specific news sources publish more negative articles? 

## Methodology Used
An analysis of nearly 4.5 million headlines from a publicly available Kaggle dataset throughout 2007 - 2022.  
Using the Natural Language Toolkit (NLTK), a sentiment classifier was trained to label "Positive" and "Negative" text on publically available Twitter tweets. 
By This classifier was then used to classify nearly 4.5 million tweets from various news organizations.  
Organizations where headlines were not available across the period of 2002- 2022 were excluded.

The percent negative sentiment plotted in the line graph represents the number of negatively labeled headlines for a company / total number of articles available in the dataset for the specified company.

Companies analyzed:
   * The New York Times
   * CNN
   * FOX News
   * Washington Post
   * CNBC

## Findings
[How Negative Are Our News Headlines? .ipynb](docs%2FHow%20Negative%20Are%20Our%20News%20Headlines%3F%20.ipynb)
* The overall average percent of negative news headlines across the five analyzed companies and slightly decreased BY ~ 6% since 2002. 
* CNN experienced the most volatile swing towards a higher negative sentiment 
* CNBC expereinced the largest decline in negative sentiment 

## Limitations
* The classifier is only able to label "Positive" and "Negative".  It has not been trained to label "Neutral"
* The classifer has been trained on a limited sample of tweets which may include more informal language not found in news publications
* The classifer only analyzed headlines and not the entire articles. 
* The dataset used may not represent all articles published by each publication

## Datasets Used: Kaggle 4.5M headlines from 10 sites throughout 2007-2022
1. [Link to dataset](https://www.kaggle.com/datasets/jordankrishnayah/45m-headlines-from-2007-2022-10-largest-sites)
News articles sourced from the following sites across 2007 - 2022

2. [NLTK Twitter dataset](https://www.nltk.org/howto/twitter.html)
Twitter dataset access through NLTK of 10,000 tweets used to train a positive and negative sentiment model

## Additional Resources Used
1. [Digital Ocean Guide on How to Perform A Sentiment Analysis](https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk)
2. [Natural Language Toolkit](https://www.nltk.org/)
3. [NLTK Corpora](https://www.nltk.org/nltk_data/) 
4. NLTK Packages needed
   * punkt: for tokenization 
   * averaged_perceptron_tagger: used to determine context of a word 
   * wordnet: lexical database to determine base word 
   * stopwords: words to exclude 
   * FreqDist: determine frequency of words 
   * classify: help with training sentiment model 
   * NaiveBayesClassifier:  probabilistic machine learning model that’s used for classification task used here for sentiment analysis 
6. matplotlib


## Additional stretch goals
* Explore sentiment analysis with [openvertex](https://cloud.google.com/vertex-ai/docs/text-data/sentiment-analysis/prepare-data) 
* Explore sentiment analysis with Open AI 
* House the classified articles in a DB
* Train the classifier on more data 
