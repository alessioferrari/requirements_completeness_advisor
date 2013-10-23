'''
Created on Jul 4, 2013

@author: alessioferrari

This program takes in input a requirement string, and stores the words employed in the requirement.
Then, it asks the user to use at least one of the words contained in the requirement.
The more the words are used, the higher the score given to the user.
The same approach iterates for the other requirements. In the end, we have a ranked list 
of words that are employed in the requirements. 
'''

import nltk
from irutils.TextFilter import TextFilter


def filter_terms(sentence):
    
    text_filter = TextFilter();
    
    filtered_words = text_filter.remove_punct(sentence)
    filtered_words = text_filter.remove_single_char(filtered_words)
    filtered_words = text_filter.remove_stopwords(filtered_words)
    
    return filtered_words

def update_dictionary(used_words_dictionary, sentence):
    "this function associates a slot in the dictionary for each term"
    
    filtered_words = filter_terms(sentence)
    used_words_list = nltk.wordpunct_tokenize(filtered_words) 
  
    first_time_used_words = list()
    
    for w in used_words_list:
        if w in used_words_dictionary.keys():
            used_words_dictionary[w] = used_words_dictionary[w] + 1
        else:
            first_time_used_words.append(w)
  
    init_usage_counters = [1] * len(first_time_used_words)
    used_words_dictionary.update(zip(first_time_used_words, init_usage_counters))
    

if __name__ == '__main__':
    
    used_words_dictionary = dict() #stores the couples word-occurrences
    
    sentence = raw_input("Write your requirement: \n")
    
    update_dictionary(used_words_dictionary, sentence)
    
    
    for i in range(3):
        sentence = raw_input("Now write your second requirement. Use at least one of the following words \n" +
                         ' '.join(used_words_dictionary.keys()) + '\n')
    
        update_dictionary(used_words_dictionary, sentence)
    
    print used_words_dictionary
    
    ##NOTE: we could use also a thesaurus with the contrary of some words
    
    ##NOTE: we should map words to stems, but preserve a representative word
    
    pass

