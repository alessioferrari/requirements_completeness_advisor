'''
Created on Oct 3, 2013

@author: alessioferrari

This script compute the completeness score of requirements written without the tool
'''
from RelationshipDictionary import RelationshipDictionary
from RelationshipManager import RelationshipManager
from RelevantTermsDictionary import RelevantTermsDictionary
from RelevantTermsManager import RelevantTermsManager

RELATIONSHIP_FILE = '../docs/Finestra11.txt'
RELEVANT_TERMS_FILE = "../docs/ieeeATS2.term.tmp"

requirements_alessio = ['The ATS system shall have the capability to track all CBTC-equipped trains'
'The ATS system shall have the capability to store information about all the CBTC-equipped trains'
'The ATS sysm shall show the location of all CBTC-equipped trains  through the ATS user interface'
'The ATS system should show the schedule of all CBTC-equipped trains through the ATS user interface'
'The ATS system shall implement the functionality of train routing'
'The ATS system shall show the routes of the trains through the ATS user interface'
'The ATS system shall show the limit of the movement authorities through the user interface'
'The ATS system shall provide schedule and headway regulation for the CBTC-equipped trains'
'The ATS system shall have the capability to monitor the performance of CBTC-equipped trains'
'The ATS system shall have the capability to regulate the performance of CBTC-equipped trains'
'The ATS system shall send the desired station departure time to the CBTC-equipped trains'
'The ATS system shall send the desired speed profile to the CBTC-equipped trains'
'The ATS system shall provide automatic train regulation functions'
'The ATS system shall support energy-optimization'
'The ATS system shall implement the capability to stop a CBTC-equipped train at the next station'
'The ATS system shall implement the capability to hold a train in a station'
'The ATS system shall implement the capability to release a train that has been hold in a station'
'The ATS system shall implement the capability of skipping station stops'
'The ATS system shall implement the capability of inhibiting the control of the train doors'
'The ATS system shall have the capability to stop a train en route'
'The ATS system shall have the capability to define temporary speed restictions for CBTC-equipped trains'
'The ATS system shall allow the operator to define work zones'
'The ATS system shall enforce speed restrictions in the work zones'
'The ATS system shall shall provide methods to visually warn operators in the work zones'
'The ATS system shall provide an interface with the Passenger Information System'
'The ATS system shall support fault reporting from CBTC-equipped trains'
'The ATS system shall support interoperability among different devices'
'The ATS system shall allow the operator to manually route the trains'
'The ATS system shall notify the activation of the train brake to the train operator when stopping a train en route'
'The ATS sytem shall minimize the delay of CBTC equipped trains'
'The ATS system shall include the capability to block and unblock a switch'
'The ATS system shall include the capability to block and unblock a signal'
'The ATS system shall include the capability to block and unblock a route entry point'
'The ATS system shall include the capability to block and unblock a section of track'
'The ATS system shall indicate the approaching of trains and their direction in the work zones'
'The ATS system shall implement an interface to receive fault reports from the other devices of the CBTC system']

requirements_giorgio = [
'The ATS User interface shall be able to display all information of layout of railway, the position of train, a train identification.'
'The ATS shall be able to assign a train identification for each train operating in CBTC territory.'
'The ATS shall be able to automatically track each train operating in CBTC territory.'
'The ATS shall be able to permit CBTC-equipped trains operating in CBTC territory to be manually and automatically routed based on CBTC train location reports.'
'The ATS shall be able to automatically monitor and regulate the performance of CBTC-equipped trains operating in CBTC territory, in relation to schedule and/or headway adherence (e.g., through adjustments to train acceleration and service brake rates, and speeds)'
'The ATS should be able to facilitate appropriate train meets in order to minimize overall system delays.'
'The ATS should be able to have the capability to implement energy optimization algorithms for CBTC-equipped trains through the real-time control and coordination of train acceleration, train coasting, and train braking.'
'The ATS shall be able to communicate with ATO on CBTC-equipped train.'
'The ATS should be able to direct a single CBTC-equipped train or a group of CBTCequipped trains to stop at the next station, even if the train is scheduled to bypass that station'
'The ATS shall be able to include facilities to hold a CBTC-equipped train at a station, for trains operated without crews'
'The ATS should be able to include facilities to direct a CBTC-equipped train or group of CBTC-equipped trains to pass through a station or group of stations without stopping.'
'The ATS should be able to may include facilities to inhibit (and subsequently permit) CBTC control of the train doors.'
'The ATS shall be able to stop a single CBTC-equipped train or group of CBTC-equipped trains immediately.'
'The ATS shall be able to impose (and remove) temporary speed restrictions for CBTCequipped trains operating on any section of track in CBTC territory'
'The ATS shall be able to block (and subsequently unblock) a switch, an exit signal, a route entry point, or a section of track within CBTC territory.'
'The ATS shall be able to communicate with IXL on wayside equipped line.'
'The ATS shall be able to establish (and subsequently remove) temporary work zones for the protection of work crews and work trains.'
'The ATS should be able to interface with wayside and/or train-borne passenger information systems to trigger automatic passenger information messages, such as train arrival information.'
'The ATS shall be able to detect failures and out-of-tolerance conditions for a CBTC system that can impact the on-time performance of the transit system.'
'The ATS shall be able to automatically indicate on the ATS user interface display failures and out-of-tolerance conditions of the CBTC system  that can impact the on-time performance of the transit system.'
'The ATS should be able to display on the ATS user interface displays the train health data.'
]






#########Relationship completeness

requirements = requirements_alessio

relationship_dictionary = RelationshipDictionary(inputfile= RELATIONSHIP_FILE)
dictionary = relationship_dictionary.get_dictionary('loglikelihood')
relationship_manager = RelationshipManager(dictionary, float(10), stop_list = ['authority', 'jurisdiction'])

for current_requirement in requirements:
        for couple in relationship_manager.get_usable_couples():
            if couple[0].lower() in current_requirement.lower() and \
                couple[1].lower() in current_requirement.lower():
                    relationship_manager.set_related(couple)  
                    
print "Relationship completeness = ", relationship_manager.get_current_relationship_completeness_score()

########Term completeness

term_dictionary  = RelevantTermsDictionary(RELEVANT_TERMS_FILE)
term_manager = RelevantTermsManager(term_dictionary, stop_list = ['authority', 'jurisdiction'])
term_manager.set_current_threshold(99.0)

for current_requirement in requirements:
        for term in term_manager.get_list_of_usable_terms():
            if term.lower() in current_requirement.lower():
                term_manager.set_relevant(term)
    
print "Term completeness = ", term_manager.get_current_term_completeness_score()