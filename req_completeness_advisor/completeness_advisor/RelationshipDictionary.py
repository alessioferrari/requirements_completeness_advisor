'''
Created on Sep 25, 2013

@author: alessioferrari
'''

class RelationshipDictionary(object):
    '''
    This class loads a file of relationship into three dictionaries,
    one for each of the similarity metrics adopted to compute the relationships
    (frequency, loglikelihood, cosine similarity) 
    '''
    
    def __load_into_dictionary(self, lines, dictionary_type):
        for idx, line in enumerate(lines):
            if line.strip().startswith('---->'):
                #This line removes leading and trailing strings#
                term = line.lstrip('----> ').rsplit(' ', 1)[0] 
                #This line takes the line that follows the term, where the related terms are placed
                #strip() is required to remove the trailing '\n' character
                related_terms_line = lines[idx+1].strip()
                related_terms_couples =  related_terms_line.split('\t')
                
                #This is a list for each term, in the form [['term','value']['term','value'],...]
                #to store the related terms
                related_terms_list = list()
                
                for couple in related_terms_couples:
                    #TERM is the separator among the term and the numerical value
                    splitted_couple = couple.split('TERM')
                    
                    for indx, elem in enumerate(splitted_couple):
                        splitted_couple[indx] = elem.strip()
                    
                    related_terms_list.append(splitted_couple)
                
                self.add_element(term, related_terms_list, dictionary_type)

    def __load_input_file(self, inputfile):
        """
        This function reads the input file and loads the content into the dictionaries
        Three dictionaries are provided, one for each type of relatedness function 
        """
        f = open(inputfile, 'rU')
        content = f.read()
        
        
        [empty, frequency_related_part, loglikelihood_related_part, cosine_related_part] = content.split('#')
        
        frequency_lines = frequency_related_part.split('\n')
        self.__load_into_dictionary(frequency_lines, 'frequency')
                    
        loglikelihood_lines = loglikelihood_related_part.split('\n')
        self.__load_into_dictionary(loglikelihood_lines, 'loglikelihood')  
        
        cosine_lines = cosine_related_part.split('\n')
        self.__load_into_dictionary(cosine_lines, 'cosine')      

    def __init__(self, inputfile):
        '''
        Constructor
        '''
        self.relationship_dictionary_frequency = dict()
        self.relationship_dictionary_loglikelihood = dict()
        self.relationship_dictionary_cosine = dict()
        self.__load_input_file(inputfile)
        
    
    def add_element(self, key, related_terms_list, dictionary_type):
        """
        @param key: is the term
        @param related_term_list: has the form [['term','value']['term','value'],...]  
        """
        if dictionary_type == 'frequency':
            self.relationship_dictionary_frequency[key] = related_terms_list 
        elif dictionary_type == 'loglikelihood':
            self.relationship_dictionary_loglikelihood[key] = related_terms_list 
        elif dictionary_type == 'cosine':
            self.relationship_dictionary_cosine[key] = related_terms_list
        
#    def get_element(self):
#        """
#        @todo: ADJUST or REMOVE
#        """
#        #lastelement = len(self.relationship_dictionary_frequency['train at station'])
#        #print self.relationship_dictionary_loglikelihood[0]
#        print self.relationship_dictionary_frequency['train at station'] 
#        print self.relationship_dictionary_loglikelihood['CBTC territory'][0][0]
#        print self.relationship_dictionary_cosine.keys()[0]
#        print len(self.relationship_dictionary_cosine.keys())
#        print len(self.relationship_dictionary_frequency.keys())

    def get_dictionary(self, dictionary_type): 
        if dictionary_type == 'frequency':
            return self.relationship_dictionary_frequency
        elif dictionary_type == 'loglikelihood':
            return self.relationship_dictionary_loglikelihood
        elif dictionary_type == 'cosine':
            return self.relationship_dictionary_cosine
        else:
            return -1
            
            
#r = RelationshipDictionary(inputfile= '../docs/finestra20.txt')
#print r.get_dictionary('frequency')