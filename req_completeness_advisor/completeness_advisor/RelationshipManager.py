'''
Created on Sep 26, 2013

@author: alessioferrari
'''

from RelationshipDictionary import RelationshipDictionary
from random import choice
from decimal import Decimal


class RelationshipManager(object):
    '''
    classdocs
    '''


    def __init__(self, dictionary, threshold = float(0), stop_list = []):
        '''
        Each couple of terms in dictionary is placed in a list of term couples,
        where the first element is the couple of terms, and the second element
        is the 'status', which can be 'new', 'related', 'suspended' or 'unrelated'.
        We have also another list, that includes all the new and suspended couples.
        We have called this list list_of_usable_couples. When a couple is evaluated
        but not used, becomes suspended. When a couple is evaluated and used, becomes
        related. When it is suspended and not used, the couple becomes unrelated.
        @param dictionary: a dictionary of couples of terms
        @param threshold: all the terms that have a relatiohisp value that is lower that the one expressed in the input
        are not loaded in the dictionary
        @param stop_list: if a term is included in the stop_list, and it is also part of the relationship dictionary,
        all the relationships that are associated to that term are removed from the relationship dictionary
        '''
        #This is the complete list of couples
        self.listofcouples = list()
        terms = dictionary.keys()
        for term in terms:
            if term not in stop_list:
                for related_term in dictionary[term]:
                    if related_term[0] not in stop_list: 
                        if float(related_term[1]) >= threshold: #we append the couple only if the relationship is higher than 0.5
                            couple = [term, related_term[0]]
                            slot = [couple, 'new']
                            self.listofcouples.append(slot)
        
        
        #This is the list of couples that can be used to build requirements
        self.list_of_usable_couples = list() #I initially copy the previous list
        for item in self.listofcouples:
            self.list_of_usable_couples.append(item[0])
        
    def search_usable(self, couple):
        '''
        Given the couple of terms, returns the corresponding element in the list of usable couples
        '''
        for item in self.list_of_usable_couples:
            if item[0] == couple[0] and item[1] == couple[1]:
                return item
            
        return -1
    
    def __set_status(self, couple, status):      
        for item in self.listofcouples:
            if item[0][0] == couple[0] and item[0][1] == couple[1]:
                item[1] = status
                return 0
        
        return -1
    
    
    def __is_status(self, couple, status):
        '''
        This function tells if the status of the couple is the one 
        written in status
        @return -1, if the couple does not exist
        0 if the status is not as expected
        1 if the status is as expected
        '''
        for item in self.listofcouples:
            if item[0][0] == couple[0] and item[0][1] == couple[1]:
                if status == item[1]:
                    return 1
                else:
                    return 0
        return -1
                
    def set_related(self, couple):
        if self.__set_status(couple, 'related') == 0:
            if couple in self.list_of_usable_couples:
                self.list_of_usable_couples.remove(couple)
                return 0
            else: 
                return -1
        else:
            return -1
                
                
    def set_suspended(self, couple):
        if self.__set_status(couple, 'suspended') == -1:
            return -1
        else: 
            return 0
    
    def set_unrelated(self, couple):
        if self.__set_status(couple, 'unrelated') == 0:
            if couple in self.list_of_usable_couples:
                self.list_of_usable_couples.remove(couple)
                return 0
            else:
                return -1
        else:
            return -1
        
        
    def is_suspended(self, couple):
        if self.__is_status(couple, 'suspended') == 1:
            return True
        elif self.__is_status(couple, 'suspended') == 0:
            return False    
        else:
            print "Couple "+ str(couple) + " does not exist!"
            
    def is_related(self, couple):
        if self.__is_status(couple, 'related') == 1:
            return True
        elif self.__is_status(couple, 'related') == 0:
            return False    
        else:
            print "Couple "+ str(couple) + " does not exist!"    
        
    def get_current_relationship_completeness_score(self):
        '''
        This function returns the current completeness score for the relationships among terms.
        The score is computed as the ratio between the number relevant couples (i.e., couples that have been used),
        and the length of the list of usable couples.
        '''    
        relevant_couples_number = len([k for k in self.listofcouples if k[1] == 'related'])
        
        if len(self.list_of_usable_couples) != 0:
            score = Decimal(relevant_couples_number)/Decimal(len(self.list_of_usable_couples))
        else:
            score = Decimal(100.0)
        
        print relevant_couples_number, len(self.list_of_usable_couples), score
        
        return score
           
    def get_random_couple(self):
        """
        This function returns one of the couples of terms
        in a random manner, if the couple is still not 
        evaluated (i.e., it is new) or it is among the suspended
        couples
        """
        random_couple = choice(self.list_of_usable_couples)
        return random_couple
    
    def get_related_couples(self):
        """
        This function returns all the related couples
        """
        list_of_related_couples = list()
        for item in self.listofcouples:
            if item[1] == 'related':
                list_of_related_couples.append(item[0])
                
        return list_of_related_couples
    
    def get_usable_couples(self):
        return self.list_of_usable_couples
    
        
    
        
#r = RelationshipDictionary(inputfile= '../docs/Finestra11.txt')
#dictionary = r.get_dictionary('loglikelihood')
#m = RelationshipManager(dictionary, float(10), stop_list = ['authority', 'jurisdiction'])
#print len(m.get_usable_couples())
##print m.search(['CBTC territory', 'ATS user-directed service strategy'])
#print m.get_current_relationship_completeness_score()
#
#m.set_related(['CBTC territory', 'ATS user-directed service strategy'])
#
#print m.get_current_relationship_completeness_score()
#print m.search(['CBTC territory', 'ATS user-directed service strategy'])

