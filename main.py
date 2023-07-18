from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random, csv

COMPANIES = [
    "New York Times",
    "CNN",
    "FOX",
    "New York Post",
    "BBC",
    "Washington Post",
    "USA Today",
    "Daily Mail",
    "CNBC",
    "The Guardian"
]
POSITIVE_SENTIMENT = "Positive"
NEGATIVE_SENTIMENT = "Negative"

def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def create_media_dict():
    media_dict = {}
    year_stats_dict = {"total_num_articles": 0, "num_positive_articles": 0, "num_negative_articles": 0}

    for company in COMPANIES:
        media_dict[company] = {}
        for year in range(2007, 2024):
            year_str = str(year)
            media_dict[company][year_str] = year_stats_dict.copy()

    return media_dict


def process_articles(file_name, classifier, media_dict):
    file = "datasets/" + file_name
    file = open(file)
    text_list = file.readlines()
    for line in text_list:
        parsed_data_arr = line.split(",")
        if len(parsed_data_arr) > 2:
            cleaned_headline = parsed_data_arr[2].replace('"', '').replace("'", '')
            year = parsed_data_arr[0][0:4]
            company = parsed_data_arr[1]

            if company in media_dict:
                calculate_article_sentiment(company, year, cleaned_headline, classifier, media_dict)
    file.close()

# returns the classifier
def train_sentiment_classifier():
    # import example positive and negative tweets to train on
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    # tokenize positive words
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
    # import stop words library
    stop_words = stopwords.words('english')

    # tokenize both positive and negative tweets
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # clean out the tokens, remove stop words)
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    # get the pos and neg tokens for the model
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    # randomize the positive and negative tokens
    random.shuffle(dataset)

    # train data and test it with 20% of the data
    train_data = dataset[:8000]
    test_data = dataset[8000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))  # Accuracy is: 0.995

    return classifier


# 20070101,New York Times,Rush to Hang Hussein Was  Questioned,http://www.nytimes.com/2007/01/01/world/middleeast/01iraq.html?hp&ex=1167714000&en=85dae91ed8178e3a&ei=5094&partner=homepage
def calculate_article_sentiment(company, year, cleaned_headline, classifier, media_dict):

    custom_tokens = remove_noise(word_tokenize(cleaned_headline))

    classification = classifier.classify(dict([token, True] for token in custom_tokens))

    # print("headline:" + cleaned_headline + " classification: " + classification)
    media_dict[company][year]["total_num_articles"] += 1
    if classification == POSITIVE_SENTIMENT:
        media_dict[company][year]["num_positive_articles"] += 1
    elif classification == NEGATIVE_SENTIMENT:
        media_dict[company][year]["num_negative_articles"] += 1

    print(media_dict[company][year])
    return classification


def remove_quotes_from_article(file_name):
    file = "datasets/" + file_name
    file = open(file)
    text_list = file.readlines()
    for line in text_list:
        line.replace('"', '').replace("'", "")
    file.close()

def calculate_annual_sentiment_by_company(media_dict):
    rows = []
    for company in media_dict:
        for year in media_dict[company]:
            curr_vals = media_dict[company][year]
            total_num_articles = curr_vals["total_num_articles"]
            if total_num_articles > 0:
                percent_pos = 100 * float(curr_vals["num_positive_articles"]) / float(total_num_articles)
                percent_neg = 100 * float(curr_vals["num_negative_articles"]) / float(total_num_articles)
                row = [company, year, total_num_articles, percent_pos, percent_neg]
                rows.append(row)
    return rows

def write_rows_to_csv(rows):
    fields = ['Company', 'Year', 'Total Num Articles', 'Percent Positive Sentiment', 'Percent Negative Sentiment']
    # filename = "output/sentiment_by_year.csv"
    filename = "output/sentiment_by_year.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


if __name__ == "__main__":
    # 1. make media_dict
    media_dict = create_media_dict()

    # 2. Train the classifier on twitter data to determine positive/ negative sentiment
    classifier = train_sentiment_classifier()

    # 3. Load each dataset file and iterate over each article and add to media_dict
    file_name = "headlines.csv"
    process_articles(file_name, classifier, media_dict)

    rows_with_annual_data = calculate_annual_sentiment_by_company(media_dict)
    write_rows_to_csv(rows_with_annual_data)

    print(media_dict)




# TODOS
# cache the classifier
# connect to bigquery
# combine datasets
# add column to write in classification
# classify by openAI vs. Google Vertex