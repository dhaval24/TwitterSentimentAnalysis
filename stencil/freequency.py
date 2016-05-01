import sys
import json
import operator
set = set()
def main():
    fil = open(sys.argv[2], 'r')
    computeTermFrequency(fil,set)

def computeTermFrequency(fil, set):
    twitter = []
    dictionary = {}
    total_word_count = 0
    for each_line in fil:
        # print(each_line)
        twitter = json.loads(each_line)
        string_words_tweet = twitter['text'].split(" ")
        for each_word in string_words_tweet:
            each_word = each_word.lower()
            if each_word not in dictionary and each_word not in set and each_word != "":
                dictionary[each_word] = 1
                total_word_count+=1
            else:
                if each_word not in set and each_word !="":
                    dictionary[each_word] = dictionary[each_word]+1
                    total_word_count+=1
    compute_freequency_count(dictionary,total_word_count)

def populate_stop_wordsset():
    file = open(sys.argv[1] ,"r")
    for each_line in file:
        set.add(each_line.strip("\n"))


def compute_freequency_count(dictionary, total_word_count):
    term_frequncy_dictionary = {}
    count = 0
    for each_term in dictionary:
        term_frequncy = dictionary[each_term]/total_word_count
        term_frequncy = term_frequncy.__round__(5)
        term_frequncy_dictionary[each_term] = term_frequncy
    for items in sorted(term_frequncy_dictionary, key = term_frequncy_dictionary.get, reverse = True):
        print(term_frequncy_dictionary[items], items.encode("utf-8"))
        count += 1
        if count >= 30:
            break


populate_stop_wordsset()
main()