import sys
import json
import operator

def main():
    sent_file = open(sys.argv[1],encoding="utf-8")
    tweet_file = open(sys.argv[2], encoding="utf-8")
    # fil = open('AFINN-111.txt', 'r')
    sentiment_map = populate_sentiment_map(sent_file)
    # fil_tweet_stream = open('streaming_output_full.txt', 'r')
    compute_sentiment_tweet(tweet_file, sentiment_map)

def compute_sentiment_tweet(fil, sentiment_map):
    tweet_sentiment_score_map = {}
    for each_line in fil:
        twitter = json.loads(each_line)
        string_words_tweet = twitter['text'].split(" ")
        for index in range(0, len(string_words_tweet)):
            string_words_tweet[index] = string_words_tweet[index].lower()
        tweet_sentiment_score = 0
        for each_word in string_words_tweet:
            if each_word in sentiment_map:
                tweet_sentiment_score += sentiment_map[each_word]
        tweet_sentiment_score_map[twitter['text']] = tweet_sentiment_score
    counter = 0
    for items in sorted(tweet_sentiment_score_map, key=tweet_sentiment_score_map.get, reverse=True):
        print(tweet_sentiment_score_map[items], items.encode("utf-8"))
        counter+=1
        if counter>=10:
            break
    counter  = 0
    for items in sorted(tweet_sentiment_score_map, key=tweet_sentiment_score_map.get):
        print(tweet_sentiment_score_map[items], items.encode("utf-8"))
        counter+=1
        if counter>=10:
            break

def populate_sentiment_map(fil):
    dictionary = {}
    for each_line in fil:
        term , score = each_line.split('\t')
        dictionary[term] = float(score.strip("\n"))
    return dictionary

if __name__ == '__main__':
    main()
