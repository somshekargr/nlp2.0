import re
from collections import Counter


def search_dictionary(dictionary, search_string):
    max_match_key = None
    max_match_count = 0

    for key, values in dictionary.items():
        #combined_values = ' '.join(values)
        word_counts = Counter(values)
        search_counts = Counter(search_string.split())
        match_count = sum((word_counts & search_counts).values())

        if match_count > max_match_count:
            max_match_count = match_count
            max_match_key = key

    return max_match_key


def get_intent_data(data, query):
    for key, value in data.items():
        for val_item in value:
            if val_item:
                if re.search(val_item, query):
                    return key
    return None

def get_value_from_dictionary(dictionary, input_string):
    if input_string in dictionary:
        return dictionary[input_string]
    else:
        return None

def search_dict_by_value(dictionary_list, search_value):
    result = []
    for dictionary in dictionary_list:
        for value in dictionary.values():
            if value == search_value:
                return dictionary
    return None

def search_key_by_value(dictionary, search_value):
    max_matched_words = 0
    matching_key = None

    for key, values in dictionary.items():
        matched_words = sum(1 for value in values if search_value in value) 
        if search_value in values:
             # Exact match found, return the key immediately
            return key
        if matched_words > max_matched_words:
            max_matched_words = matched_words
            matching_key = key

    return matching_key

