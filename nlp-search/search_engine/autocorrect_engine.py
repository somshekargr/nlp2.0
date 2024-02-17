import itertools
import numpy as np
from autocorrect import spell
from nltk.corpus import words

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()


def new_string(text_string,limit):
    newstring=[]
    new_s = [(a, list(b)) for a, b in itertools.groupby(text_string)]

    for a, b in new_s:

        if len(b)>limit:
            string=b[0]*limit

        else:
            string="".join(b)
        newstring.append(string)
    newstring="".join(newstring)

    return newstring

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])

def soundex(query: str):
    """
    https://en.wikipedia.org/wiki/Soundex
    :param query:
    :return:
    """

    # Step 0: Clean up the query string
    query = query.lower()
    letters = [char for char in query if char.isalpha()]

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If query contains only 1 letter, return query+"000" (Refer step 5)
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Step 3: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 5: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string
def read_text_to_dict(filename):
    f = open(filename, 'r')
    correct_word = {}
    for line in f:
        k, v = line.strip().split(':')
        correct_word[k.strip()] = v.strip()
    f.close()
    return correct_word

def autocorrect(query_string):
    word_list = query_string.split()
    auto_correct_string = ''
    for word in word_list:
        if word in setofwords:
            auto_correct_string += spell(word) + ' '
        else:
            auto_correct_string += (word) + ' '
    return auto_correct_string


def soundex_dict(filename):
    with open(filename) as f:
        data=f.readlines()
        
    
    data=[x.strip() for x in data]
    data = list(filter(None, data))
    soundex_dict={}
    cross_check=[]
    for list_item in range(len(data)):
        changed_word=new_string(data[list_item],2)
        
        corrected_string=soundex(changed_word)
        cross_check.append(str(data[list_item ])+" "+str(corrected_string))
        soundex_dict[data[list_item ]]=corrected_string

    return soundex_dict

def autocorrect_module(word_list,setofwords,soundex_dict,query_string):
    different_key=[]
    avoid_duplicates=[]
    for word in word_list:
      
        if not word in setofwords:
            if not word.isdigit():
                id_for_word=soundex(word)
                
                values = soundex_dict.values()
                for (key, value) in soundex_dict.items():
                    
                    if id_for_word == value:
                        
                        different_key.append(key)
                        
                        if key==word:
                        
                            
                            query_string=query_string.replace(word,key)
                            
                            avoid_duplicates.append(word)
                for (key, value) in soundex_dict.items():
                    
                    if id_for_word == value:
                        if not key==word:
                            
                            if not word in avoid_duplicates:
                                Ratio = levenshtein_ratio_and_distance(key,word,ratio_calc = True)
                                
                                if Ratio>0.80:
                                    
                                    query_string=query_string.replace(word,key)
                                elif Ratio>0.72:
                                    
                                    new_word=new_string(word,1)
                                    Ratio1 = levenshtein_ratio_and_distance(key,new_word,ratio_calc = True)

                                    
                                    if Ratio1>=0.72:
                                        
                                        query_string=query_string.replace(word,key)
                                    
                #query_string.replace(word,key)

    # ("soundex_query",query_string)
    import time
    import re
    start = time.process_time()

    update_output=[]
    correct_word=read_text_to_dict("./data/text/corrections_text.txt")

    for key,value in correct_word.items():
            
            if key.lower() in query_string.lower():
                
                #update_output=query_string.replace(key.lower(),value.lower())
                query_string = query_string.replace(key.lower(),value.lower())
            
            
                #update_output=re.sub(key.lower(),value.lower(),str(query_string.lower()))
            
            #query_string=update_output
    if update_output==[]:
        update_output=query_string
    
    final_auto_corrected_string=autocorrect(update_output)
    final_auto_corrected_string=re.sub(r'\?', '', final_auto_corrected_string)

    return final_auto_corrected_string

setofwords = set(words.words()) 
soundex_dict = soundex_dict("./data/text/scraped_text_from_bank_website1.txt")

def w_autocorrect(query_string):

    query_string = new_string(query_string,2)
    query_string = str(query_string).lower()

    word_list    = query_string.split()

    auto_correct_string = ''

    auto_correct_string = autocorrect_module(word_list, setofwords, soundex_dict, query_string)

    return auto_correct_string
