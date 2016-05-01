import sys
import csv
import json
import operator

from builtins import print


def main():
    # sent_file = open(sys.argv[1])
    # csv_file = open(sys.argv[2])
    # file_reader = csv.reader(csv_file)
    fil = open('AFINN-111.txt', 'r')
    sentiment_map = populate_sentiment_map(fil)
    fil_tweet_stream = open('streaming_output_full.txt', 'r')
    actor_tweet_map = create_actor_tweet_map(fil_tweet_stream)
    calculate_tweet_sentiment_of_actors(actor_tweet_map, sentiment_map)

def populate_sentiment_map(fil):
    dictionary = {}
    for each_line in fil:
        term , score = each_line.split('\t')
        dictionary[term] = float(score.strip("\n"))
    return dictionary

def create_actor_tweet_map(fil_tweet_stream):
    actor_tweet_map = {}
    for each_line in fil_tweet_stream:
        twitter = json.loads(each_line)
        if "user" in twitter:
            if twitter['user']['name'] not in actor_tweet_map:
                actor_tweet_map[twitter['user']['name']] = [twitter['text']]
            else:
                 actor_tweet_map[twitter['user']['name']].append(twitter['text'])

    return actor_tweet_map

def calculate_tweet_sentiment_of_actors(actor_tweet_map, sentiment_map):
    actor_averagetweet_map = {}
    for items in actor_tweet_map:
        total_tweet_Sentimentscore = 0
        for each_tweet in actor_tweet_map[items]:
            total_tweet_Sentimentscore += calculate_individual_tweetsentiment(each_tweet, sentiment_map)
        actor_averagetweet_map[items] = float(total_tweet_Sentimentscore/len(actor_tweet_map[items]))
    sorted_actor_averagetweet_map = sorted(actor_averagetweet_map.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_actor_averagetweet_map)

def calculate_individual_tweetsentiment(each_tweet ,sentiment_map):
    total_tweet_score = 0
    tweet_words = each_tweet.split(" ")
    for index in range(0 , len(tweet_words)):
        tweet_words[index] = tweet_words[index].lower()

    for each_word in tweet_words:
        if each_word in sentiment_map:
            total_tweet_score += sentiment_map[each_word]
    return total_tweet_score

if __name__ == '__main__':
    main()
