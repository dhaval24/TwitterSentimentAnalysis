import sys
import csv

def main():
    # sent_file = open(sys.argv[1])
    # csv_file = open(sys.argv[2])
    csv_file = open(sys.argv[2], encoding="utf-8")
    file_reader = csv.reader(csv_file, delimiter = ",")
    actor_tweet_map = create_actor_tweet_map(file_reader)
    fil = open(sys.argv[1], 'r')
    sentiment_map = populate_sentiment_map(fil)
    calculate_average_sentiment(actor_tweet_map, sentiment_map)

def create_actor_tweet_map(file_reader):
    actor_tweet_map = {}
    count = 1
    for each_line in file_reader:
        if count == 1:
            count += 1
            continue
        if each_line[0] not in actor_tweet_map.keys():
            actor_tweet_map[each_line[0]] = [each_line[1]]
        else:
            actor_tweet_map[each_line[0]].append(each_line[-1])
    return actor_tweet_map

def populate_sentiment_map(fil):
    dictionary = {}
    for each_line in fil:
        term , score = each_line.split('\t')
        dictionary[term] = float(score.strip("\n"))
    return dictionary

def calculate_average_sentiment(actor_tweet_map, sentiment_map):
    average_tweet_map = {}
    average_tweet_list = []
    for items in actor_tweet_map:
        total_sentiment_score = 0
        for each_tweet in actor_tweet_map[items]:
            total_words = each_tweet.split(" ")
            for each_word in total_words:
                if each_word.lower() in sentiment_map.keys():
                    total_sentiment_score += sentiment_map[each_word.lower()]
        average_tweet_map[items] = float(total_sentiment_score/len(actor_tweet_map[items]))
        average_tweet_list.append((items, float(total_sentiment_score/len(actor_tweet_map[items]))))
    sorted_average_tweet_list = sorted(average_tweet_list, key=lambda tup: tup[1], reverse = True)
    for each_element in sorted_average_tweet_list:
        print(each_element[1], each_element[0])

if __name__ == '__main__':
    main()