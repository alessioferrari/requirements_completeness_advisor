'''
Created on Sep 27, 2013

@author: alessioferrari
'''
from RelevantTermsDictionary import RelevantTermsDictionary
from decimal import Decimal
from random import choice

class RelevantTermsManager(object):
    '''
    This class manipulates the relevant terms loaded into a dictionary
    '''


    def __init__(self, relevant_terms_dictionary, stop_list = []):
        '''
        @param dictionary: shall be of type RelevantTermsDictionary
        @loads a term only if it is not in the stop_list
        '''
        basic_dictionary = relevant_terms_dictionary.get_dictionary()
        self.original_dictionary = dict()
        
        for key in basic_dictionary:
            if key not in stop_list: 
                self.original_dictionary[key] = [basic_dictionary[key], 'new']
            
        #the current dictionary is different from the original dictionary,
        #since we can modify the number of terms included in the current dictionary
        #by means of the threshold variable
        self.current_dictionary = self.original_dictionary.copy()
        
        self.list_of_usable_terms = list(self.current_dictionary.keys()) 
        
    def set_current_threshold(self, relevance_threshold):
        '''
        This function sets the current dictionary to a specific threshold:
        only the terms with a domain relevance above relevance_threshold
        are considered as part of the current dictionary
        '''
        self.current_dictionary = dict()
        for key in self.original_dictionary.keys():
            if float(self.original_dictionary[key][0][0]) >= relevance_threshold:                
            #self.original_dictionary[key][0][0] contains domain-specific relevance for key
                self.current_dictionary[key] = list(self.original_dictionary[key])
                
        self.list_of_usable_terms = self.current_dictionary.keys() 
                
    def __set_status(self, term, status):      
        if term not in self.current_dictionary.keys():
            return -1
        else:
            self.current_dictionary[term][1] = status
            
            
    def __is_status(self, term, status):
        '''
        This function tells if the status of the term is the one 
        written in status
        @return -1, if the term does not exist
        0 if the term status is not as expected
        1 if the term status is as expected
        '''
        if term not in self.current_dictionary.keys():
            return -1
        else:
            if self.current_dictionary[term][1] == status:
                return 1
            else:
                return 0
                
    def set_relevant(self, term):
        if term not in self.list_of_usable_terms:
            return -1
        elif self.__set_status(term, 'relevant') == 0:
            self.list_of_usable_terms.remove(term)
            return 0
        else:    
            return -1
                
                
    def set_suspended(self, term):
        if self.__set_status(term, 'suspended') == -1:
            return -1
        else: 
            return 0
    
    def set_unrelevant(self, term):
        if term not in self.list_of_usable_terms:
            return -1
        elif self.__set_status(term, 'unrelevant') == 0:
            self.list_of_usable_terms.remove(term)
            return 0
        else:
            return -1         
        
    def is_suspended(self, term):
        if self.__is_status(term, 'suspended') == 1:
            return True
        else:
            return False
        
    def is_relevant(self, term):
        if self.__is_status(term, 'relevant') == 1:
            return True
        else:
            return False        
    
    def get_current_dictionary(self):
        return self.current_dictionary
    
    def get_list_of_usable_terms(self):
        return self.list_of_usable_terms
    
    def __get_term_type(self, term_type):
        terms_to_get = list()
        for term in self.current_dictionary.keys():
            if self.current_dictionary[term][1] == term_type:
                terms_to_get.append(term)

        return terms_to_get
    
    def get_relevant_terms(self):
        return self.__get_term_type("relevant")
    
    
    def get_unrelevant_terms(self):
        return self.__get_term_type("unrelevant")
    
    def get_current_term_completeness_score(self):
        '''
        Term completeness is computed as the number of relevant terms
        in status 'relevant' divided by the terms in status 'suspended'
        or in status 'new' (i.e., the length of list_of_usable_terms). 
        The terms in status 'unrelevant' are not considered for counting the completeness,
        since they are not considered relevant by the human operator.
        '''
        relevant_terms_number = len([k for k in self.current_dictionary.keys() if self.current_dictionary[k][1] == 'relevant'])
        
        if len(self.list_of_usable_terms) != 0:
            score = Decimal(relevant_terms_number)/Decimal(len(self.list_of_usable_terms))
        else:
            score = Decimal(100.0)
        
        return score
    
    def get_random_term(self):
        if len(self.list_of_usable_terms) != 0:
            return choice(self.list_of_usable_terms)
        else :
            return -1
        
r = RelevantTermsDictionary("../docs/OLDDOCS/ieeeATSfunctions.conll.term.tmp")
man = RelevantTermsManager(r, ['authority', 'jurisdiction'])
print man.get_current_dictionary()
#print len(man.get_list_of_usable_terms())
#man.set_current_threshold(99.0)
#mydictionary = man.get_current_dictionary()
#print len(man.get_list_of_usable_terms())
#print 'completeness score: ', man.get_current_term_completeness_score()
#
#man.set_relevant('cbtc train location')
#man.set_relevant('cbtc equipment')
#print 'completeness score: ', man.get_current_term_completeness_score()
#
#print 'random term', man.get_random_term()
#print 'random term', man.get_random_term()
#
#for k in mydictionary.keys():
#    man.set_relevant(k)
#
#print man.get_current_dictionary()
#print 'completeness score: ', man.get_current_term_completeness_score()
#print man.get_random_term()
#print man.get_random_term()