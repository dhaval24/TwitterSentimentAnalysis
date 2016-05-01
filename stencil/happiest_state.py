import sys
import json

def main():
    sent_file = open(sys.argv[1], encoding="utf-8")
    tweet_file = open(sys.argv[2])
    abrre_file = open("abbrevations.txt")
    sentiment_map = populate_sentiment_map(sent_file)
    state_abbre_map = populate_state_abbre_map(abrre_file)
    happiest_state(tweet_file, sentiment_map, state_abbre_map)

def happiest_state(tweet_file, sentiment_map, state_abbre_map):
    state_tweet_map = {}
    state_tweet_count = {}
    for each_line in tweet_file:
        twitter = json.loads(each_line)
        if twitter['place'] is not None:
            if twitter['place']['country'] == "United States" and twitter['place']['place_type'] == "city":
                full_name_array = twitter['place']['full_name'].split(",")
                if full_name_array[-1].strip(" ") not in state_tweet_map:
                  state_tweet_map[full_name_array[-1].strip(" ").strip("\n")] = calculate_tweet_sentiment(twitter, sentiment_map)
                  state_tweet_count[full_name_array[-1].strip(" ").strip("\n")] = 1
                else:
                  state_tweet_map[full_name_array[-1].strip(" ").strip("\n")] += calculate_tweet_sentiment(twitter, sentiment_map)
                  state_tweet_count[full_name_array[-1].strip(" ").strip("\n")] += 1
            if twitter['place']['country'] == "United States" and twitter['place']['place_type'] == "admin":
                full_name_array = twitter['place']['full_name'].split(",")
                if state_abbre_map[full_name_array[0]] not in state_tweet_map.keys():
                    state_tweet_map[state_abbre_map[full_name_array[0]].strip("\n")] = calculate_tweet_sentiment(twitter, sentiment_map)
                    state_tweet_count[state_abbre_map[full_name_array[0]].strip("\n")] = 1
                else:
                    state_tweet_map[state_abbre_map[full_name_array[0]].strip("\n")] += calculate_tweet_sentiment(twitter, sentiment_map)
                    state_tweet_count[state_abbre_map[full_name_array[0]].strip("\n")] += 1
    for items in state_tweet_map:
        state_tweet_map[items] = state_tweet_map[items]/state_tweet_count[items]
    for items in sorted(state_tweet_map, key=state_tweet_map.get, reverse = True):
        print(state_tweet_map[items],":", items)


def calculate_tweet_sentiment(twitter, sentiment_map):
    string_words_tweet = twitter['text'].split(" ")
    for index in range(0, len(string_words_tweet)):
        string_words_tweet[index] = string_words_tweet[index].lower()
    tweet_sentiment_score = 0
    for each_word in string_words_tweet:
        if each_word in sentiment_map:
            tweet_sentiment_score += sentiment_map[each_word]
    return tweet_sentiment_score

def populate_state_abbre_map(abrre_file):
    state_map = {}
    for each_line in abrre_file:
        each_line_array = each_line.split(":")
        state_map[each_line_array[0]] = each_line_array[-1]
    return state_map

def populate_sentiment_map(fil):
    dictionary = {}
    for each_line in fil:
        term , score = each_line.split('\t')
        dictionary[term] = float(score.strip("\n"))
    return dictionary

if __name__ == '__main__':
    main()
