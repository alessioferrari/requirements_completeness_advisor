'''
Created on 25/gen/2012

@author: Alessio
'''

from nltk.stem.porter import PorterStemmer
import nltk
import re
from nltk.corpus import stopwords

stopwords_file = "stop_words.txt"

class TextFilter(object):
    '''
    This class filter a text providing typical IR functions such as stop words removal,
    stemming and so forth
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #self.stopwords = open(stopwords_file, 'r').read().split()
        self.stopwords = stopwords.words('english')
        
        
    def remove_stopwords(self, string_text):
        """
        The function takes a string as input and returns a string
        without the stopwords
        """
        tokens = nltk.word_tokenize(string_text)
        filteredtext = ' '.join([t for t in tokens if t.lower() not in self.stopwords])
        return filteredtext

    def __remove_item_from_term(self, term, item):
        """
        remove charachter @param item from the @param term
        """
        return ''.join([c for c in term if c != item])
        

    def remove_item(self, string_text, item):
        """
        remove charachter @param item from the string
        """
        tokens = nltk.word_tokenize(string_text)
        filteredtext = ' '.join([self.__remove_item_from_term(t, item) for t in tokens])
        return filteredtext
    
    def stem_words(self, string_text):
        """
        The function takes a string as input and returs a string with stemmed words
        """
        tokens = nltk.word_tokenize(string_text)
        stemmer = PorterStemmer()
        stemmedtext = ' '.join([stemmer.stem(t) for t in tokens]) 
        return stemmedtext
    
    def remove_punct(self, string_text):
        """
        The function takes a string as input and returns the same string without punctuation
        """ 
        nopunct_text = ''.join([c for c in string_text if re.match("[a-zA-Z\-\' \n\t]", c)]) 
        return nopunct_text

    def lower_all(self, string_text):
        """
        Reduce each term in @param string_text to lowecase
        """
        tokens = nltk.word_tokenize(string_text)
        lowercase_string = ' '.join([t.lower() for t in tokens])
        return lowercase_string

    def remove_single_char(self, string_text):
        """
        remove single char items from @param string_text
        """
        tokens = nltk.word_tokenize(string_text)
        no_single_char_string = ' '.join([t for t in tokens if len(t) > 1])
        return no_single_char_string
    
    def filter_all(self, string_text):
        """
        executes all the filter functions on @param string_text 
        @param string_text: input text
        """
        sentence_no_punct = self.remove_punct(string_text)
        sentence_no_single_char = self.remove_single_char(sentence_no_punct)
        sentence_no_stopwords = self.remove_stopwords(sentence_no_single_char)
        filtered_sentence = self.stem_words(sentence_no_stopwords)

        filtered_sentence = self.lower_all(filtered_sentence)
        #filtered_sentence = self.lower_all(sentence_no_single_char)
        
        return filtered_sentence


