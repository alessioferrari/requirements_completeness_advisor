'''
Created on Sep 27, 2013

@author: alessioferrari
'''

class RelevantTermsDictionary(object):
    '''
    classdocs
    '''

    def __load_input_file(self, inputfile):
        f = open(inputfile, 'rU')
        content = f.read()
        content = content.split('Configuration:')[0]
        
        lines = content.split('\n')
        lines = [l for l in lines if l != ''] #remove blank lines
        lines = lines[1:len(lines)] #removing the header of the file
        
        for line in lines:
            [term, domain_relevance, frequency] = line.split('\t') 
            self.relevant_terms_dictionary[term] = [domain_relevance, frequency]
        
        

    def __init__(self, inputfile):
        '''
        The dictionary is composed of lemma -> [domain_relevance, frequency] 
        '''
        self.relevant_terms_dictionary = dict()
        self.__load_input_file(inputfile)
        
    def get_dictionary(self):
        return self.relevant_terms_dictionary
    
    def get_element(self):
        print self.relevant_terms_dictionary['cbtc-equipped train']
        
#r = RelevantTermsDictionary("../docs/ieeeATSfunctions.conll.term.tmp")
