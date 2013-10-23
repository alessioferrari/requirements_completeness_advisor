'''
Created on Sep 26, 2013

@author: alessioferrari
'''
from RelationshipDictionary import RelationshipDictionary
from RelationshipManager import RelationshipManager
from RelevantTermsDictionary import RelevantTermsDictionary
from RelevantTermsManager import RelevantTermsManager
from Tkinter import *
from nltk.tokenize import word_tokenize
from nltk.tokenize.simple import LineTokenizer
from tkFileDialog import askopenfilename
from tkMessageBox import showerror
from ttk import Frame, Notebook, Button
from CustomText import CustomText
import nltk




def update_highlights_terms(rel_manager, term_manager, in_text):
    '''
    This function updates the current highlights for the text area 
    where the input document is loaded.
    '''
    relevant_terms = term_manager.get_relevant_terms()
    unrelevant_terms = term_manager.get_unrelevant_terms()
    
    for relevant_term in relevant_terms:
        in_text.highlight_pattern(relevant_term, "used_highlight")
        
    for unrelevant_term in unrelevant_terms:
        in_text.highlight_pattern(unrelevant_term, "unrelevant_highlight")


def update_relationship_status(current_requirement):
    suggested_term_a_tmp = suggested_term_a.get()
    suggested_term_b_tmp = suggested_term_b.get()
    
    if suggested_term_a_tmp.lower() in current_requirement.lower() and \
    suggested_term_b_tmp.lower() in current_requirement.lower():
        relationship_manager.set_related([suggested_term_a_tmp, suggested_term_b_tmp])
    ##if the relatioship is not suspended, then they can be suspended
    ##otherwise the terms become unrelated
    else:
        if relationship_manager.is_suspended([suggested_term_a_tmp, suggested_term_b_tmp]) and suspend_relationships.get() == "not_suspended":
            relationship_manager.set_unrelated([suggested_term_a_tmp, suggested_term_b_tmp])
        else:
            if not relationship_manager.is_related([suggested_term_a_tmp, suggested_term_b_tmp]):
                relationship_manager.set_suspended([suggested_term_a_tmp, suggested_term_b_tmp])
    
    ##if a relationship that is not suggested is reported in the requirement
    ##the system shall update the relationship status to "related"
    for couple in relationship_manager.get_usable_couples():
        if couple[0].lower() in current_requirement.lower() and \
        couple[1].lower() in current_requirement.lower():
            relationship_manager.set_related(couple)    
    
def update_terms_status(current_requirement):
    suggested_term_single_tmp = suggested_term_single.get()
    
    if suggested_term_single_tmp.lower() in current_requirement.lower():
        term_manager.set_relevant(suggested_term_single_tmp)
    else:
        if term_manager.is_suspended(suggested_term_single_tmp) and suspend_terms.get() == "not_suspended":
            term_manager.set_unrelevant(suggested_term_single_tmp)
        else:
            if not term_manager.is_relevant(suggested_term_single_tmp):
                term_manager.set_suspended(suggested_term_single_tmp)
    
    #if the current requirement contains terms that are not suggested,
    #but belong to the relevant terms, we shall update the term_manager
    for term in term_manager.get_list_of_usable_terms():
        if term.lower() in current_requirement.lower():
            term_manager.set_relevant(term)
    
    

def add_requirement():
    current_requirement = requirement.get()
    t.insert(END, str(requirements_counter.get())+ '. ' + current_requirement + '\n')
    requirement_entry.delete(0, END)
    requirements_counter.set(requirements_counter.get() + 1)
    
    update_relationship_status(current_requirement)
    update_terms_status(current_requirement)
    
    relationship_completeness.set(round(relationship_manager.get_current_relationship_completeness_score(), 4))
    term_completeness.set(round(term_manager.get_current_term_completeness_score(), 4))
    
    #here we update the terms highlight, according to the stored data.
    #indeed, by deleting the highlight of the previously suggested terms, we might have deleted
    #some highlight that depend on the data
    
    update_highlights_terms(relationship_manager, term_manager, input_txt_updated)
    #update_highlights_terms(relationship_manager, term_manager, input_txt)
    
    if suspend_terms.get() == "not_suspended":
        get_other_relevant_terms()
    
    if suspend_relationships.get() == "not_suspended":
        get_other_relationships()
    
    return 0

def suspend_unsuspend_terms():
    "This function suspends the updating of the terms when the button Add is pressed"
    if suspend_terms.get() == "not_suspended":
        suspend_terms.set("suspended")
        suspend_button.config(text='Resume Terms')
    else:
        suspend_terms.set("not_suspended")
        suspend_button.config(text='Suspend Terms')
        
        
def suspend_unsuspend_relationships():
    "This funciton suspend/unsuspend the random update of terms when the button Add is pressed"
    if suspend_relationships.get() == "not_suspended":
        suspend_relationships.set("suspended")
        suspend_relationship_button.config(text='Resume Relationships')
    else:
        suspend_relationships.set("not_suspended")
        suspend_relationship_button.config(text='Suspend Relationships')

def get_other_relevant_terms():
    input_txt.remove_highlight(suggested_term_single.get(), "relevant_term_highlight")
    input_txt.remove_highlight(suggested_term_single.get().lower(), "relevant_term_highlight")
    random_term = term_manager.get_random_term()
    #random_term = "conductor" 
    
    suggested_term_single.set(random_term)
    input_txt.highlight_pattern(random_term, "relevant_term_highlight")
    input_txt.highlight_pattern(random_term.lower(), "relevant_term_highlight")
    
def get_other_relationships():
        #first, we remove the highlight of the previously suggested terms from the text
    input_txt.remove_highlight(suggested_term_a.get(), "relatioship_highlight")
    input_txt.remove_highlight(suggested_term_a.get().lower(), "relatioship_highlight")
    input_txt.remove_highlight(suggested_term_b.get(), "relatioship_highlight")
    input_txt.remove_highlight(suggested_term_b.get().lower(), "relatioship_highlight")
    
    #here we update the suggested terms
    couple = relationship_manager.get_random_couple()
    #couple = ["control", "train doors"]

    suggested_term_a.set(couple[0])
    suggested_term_b.set(couple[1])
    
    input_txt.highlight_pattern(couple[0], "relatioship_highlight")
    input_txt.highlight_pattern(couple[0].lower(), "relatioship_highlight")
    input_txt.highlight_pattern(couple[1], "relatioship_highlight")
    input_txt.highlight_pattern(couple[1].lower(), "relatioship_highlight")

def get_other_terms():
    if suspend_terms.get() == "not_suspended":
        get_other_relevant_terms()
    
    if suspend_relationships.get() == "not_suspended":
        get_other_relationships()
    

RELATIONSHIP_FILE = '../docs/Finestra11.txt'
RELEVANT_TERMS_FILE = "../docs/ieeeATS2.term.tmp"
INPUT_FILE = "../docs/ieeeATSfunctions.txt"

root = Tk()
root.title("Completeness Assistant for Requirements")

relationship_background = "red"
relevant_term_background = "orange"

#Relationship dictionary and managers

relationship_dictionary = RelationshipDictionary(inputfile= RELATIONSHIP_FILE)
dictionary = relationship_dictionary.get_dictionary('loglikelihood')
#relationship_manager = RelationshipManager(dictionary, float(10), stop_list = ['authority', 'jurisdiction'])
dictionary = relationship_dictionary.get_dictionary('frequency')
relationship_manager = RelationshipManager(dictionary, stop_list = ['authority', 'jurisdiction'])

#Term dictionary and managers

term_dictionary  = RelevantTermsDictionary(RELEVANT_TERMS_FILE)
term_manager = RelevantTermsManager(term_dictionary, stop_list = ['authority', 'jurisdiction'])
#term_manager.set_current_threshold(99.0)

print "num of terms", len(term_manager.get_current_dictionary())
print "num of relations", len(relationship_manager.get_usable_couples())

#main frame
supermainframe = Frame(root, padding="3 3 12 12")
supermainframe.grid(column=0, row=0, sticky=(N, W, E, S))
supermainframe.columnconfigure(0, weight=1) 
supermainframe.rowconfigure(0, weight=1)

mainframe = Frame(supermainframe, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1) 
mainframe.rowconfigure(0, weight=1) 


suggested_term_a = StringVar()
suggested_term_b = StringVar()

suggested_term_single = StringVar()


couple = relationship_manager.get_random_couple()
couple = ['speed restrictions','application']
suggested_term_a.set(couple[0])
suggested_term_b.set(couple[1])

suggested_term_single.set(term_manager.get_random_term())
#suggested_term_single.set("conductor")

mycolor = '#%02x%02x%02x' % (237, 237, 237) # this is the default background color for the mainframe
Label(mainframe, text="Write a requirement with the following terms:", bg=mycolor).grid(column=0, row=4, sticky=(W))
Label(mainframe, textvariable=suggested_term_a, relief="groove", bg=relationship_background).grid(column=0, row=6, sticky=(W))
Label(mainframe, textvariable=suggested_term_b, relief="groove", bg=relationship_background).grid(column=0, row=7, sticky=(W))
Label(mainframe, textvariable=suggested_term_single, relief="groove", bg=relevant_term_background).grid(column=0, row=5, sticky=(W))

Button(mainframe, text="Get other terms", command=get_other_terms).grid(column=2, row=5, sticky=W)

suspend_relationship_button = Button(mainframe, text="Suspend Relations", command=suspend_unsuspend_relationships)
suspend_relationship_button.grid(column=2, row=7, sticky=W)

suspend_button = Button(mainframe, text="Suspend Terms", command=suspend_unsuspend_terms)
suspend_button.grid(column=2, row=6, sticky=W)

suspend_terms = StringVar()
suspend_terms.set("not_suspended")

suspend_relationships = StringVar()
suspend_relationships.set("not_suspended")

#enter requirements area
requirement = StringVar()
requirement_entry = Entry(mainframe, textvariable=requirement) #by writing text variable feet here, 
requirement_entry.grid(column=0, columnspan=3, row=8, sticky=(W,E))
requirement_entry.pack()

#this variable counts the requirements
requirements_counter = IntVar()
requirements_counter.set(1)

Button(mainframe, text="Add", command=add_requirement).grid(column=2, row=9, sticky=(N,W))

#text area
#txt_frm = Frame(mainframe, width=200, height=100) #larger
txt_frm = Frame(mainframe, width=500, height=100) #smaller
txt_frm.pack(fill="both", expand=True)

#for a smaller frame
txt_frm.pack_propagate(0)

txt_frm.grid(column=0, columnspan= 2, row=9, sticky=(W,E))
# ensure a consistent GUI size
txt_frm.grid_propagate(False)
# implement stretchability
txt_frm.grid_rowconfigure(0, weight=1)
txt_frm.grid_columnconfigure(0, weight=1)

# create a Text widget
t = Text(txt_frm, borderwidth=3, relief="sunken")
t.config(font=("consolas", 12), undo=True, wrap='word')
t.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

# create a Scrollbar and associate it with txt
scrollb = Scrollbar(txt_frm, command=t.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
t['yscrollcommand'] = scrollb.set

t.pack()

#########The frame below is the one where completeness values are stored

relationship_completeness = DoubleVar()
term_completeness = DoubleVar()

completeness_frame = Frame(mainframe, width=200)
completeness_frame.grid(column=0, row=10, sticky=(W))

Label(completeness_frame, text="Concept Completeness", bg=mycolor).grid(column=0, row=0, sticky=(W))
Label(completeness_frame, textvariable=term_completeness).grid(column=1, row=0, sticky=(E))

Label(completeness_frame, text="Interaction Completeness", bg=mycolor).grid(column=0, row=1, sticky=(W))
Label(completeness_frame, textvariable=relationship_completeness).grid(column=1, row=1, sticky=(E))

#########The frame below is the one where the inputfile is loaded. It is a lateral frame

#text area
inputdoc_frm = Frame(supermainframe, width=500, height=200)
inputdoc_frm.grid(column=0, row=11, sticky=(W,E)) #below
#inputdoc_frm.grid(column=1, row=0, sticky=(N,S,W,E)) #lateral
inputdoc_frm.pack(fill="both", expand=True)
# ensure a consistent GUI size
inputdoc_frm.grid_propagate(False)
# implement stretchability
inputdoc_frm.grid_rowconfigure(0, weight=1)
inputdoc_frm.grid_columnconfigure(0, weight=1)

# create a Text widget
input_txt = CustomText(inputdoc_frm, borderwidth=3, relief="sunken")
input_txt.config(font=("consolas", 12), undo=True, wrap='word')
input_txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

# create a Scrollbar and associate it with txt
scrollbar_input_txt = Scrollbar(inputdoc_frm, command=input_txt.yview)
scrollbar_input_txt.grid(row=0, column=1, sticky='nsew')
input_txt['yscrollcommand'] = scrollbar_input_txt.set

# here we load the actual input file
fp = open(INPUT_FILE, 'r')
file_text = fp.read()
input_txt.insert('0.0', file_text)
fp.close()

###The frame below is the one where the input file is loaded and relationships are shown
#text area
inputdoc_frm_relationship = Frame(supermainframe, width=500, height=200)
inputdoc_frm_relationship.grid(column=2, row=0, sticky=(N,S,W,E)) #lateral
#inputdoc_frm_relationship.grid(column=0, columnspan=2, row=11, sticky=(N,S,W,E)) #below
inputdoc_frm_relationship.pack(fill="both", expand=True)
# ensure a consistent GUI size
inputdoc_frm_relationship.grid_propagate(False)
# implement stretchability
inputdoc_frm_relationship.grid_rowconfigure(0, weight=1)
inputdoc_frm_relationship.grid_columnconfigure(0, weight=1)

# create a Text widget
input_txt_updated = CustomText(inputdoc_frm_relationship, borderwidth=3, relief="sunken")
input_txt_updated.config(font=("consolas", 12), undo=True, wrap='word')
input_txt_updated.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

# create a Scrollbar and associate it with txt
scrollbar_input_txt_relationship = Scrollbar(inputdoc_frm_relationship, command=input_txt_updated.yview)
scrollbar_input_txt_relationship.grid(row=0, column=1, sticky='nsew')
input_txt_updated['yscrollcommand'] = scrollbar_input_txt_relationship.set

# here we load the actual input file
fp = open(INPUT_FILE, 'r')
file_text = fp.read()
input_txt_updated.insert('0.0', file_text)
fp.close()



used_background = "green"
unrelevant_background = "grey"
# here we configure the highlighting

input_txt.tag_configure("relatioship_highlight",background=relationship_background)
input_txt.tag_configure("relevant_term_highlight",background=relevant_term_background)
input_txt.tag_configure("used_highlight",background=used_background)
input_txt.tag_configure("unrelevant_highlight",background=unrelevant_background)

input_txt_updated.tag_configure("relatioship_highlight",background=relationship_background)
input_txt_updated.tag_configure("relevant_term_highlight",background=relevant_term_background)

input_txt_updated.tag_configure("used_highlight",background=used_background)
input_txt_updated.tag_configure("unrelevant_highlight",background=unrelevant_background)

######################################################################
for child in inputdoc_frm.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5) 
for child in supermainframe.winfo_children(): child.grid_configure(padx=5, pady=5) 

#here we hide the form
inputdoc_frm_relationship.grid_forget()

root.mainloop()
