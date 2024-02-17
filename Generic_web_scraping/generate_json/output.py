"""
    This function helps in generating the json output
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from utils.stem_words import stem_sentence


def generate_dict_data(subject, predicate, value, inner_table = []) -> dict:
    """
    Returns a dictionary with the given subject, predicate, and value.
    The value can be a string, a list of strings, or an HTML element.
    If the value is an HTML element, any URLs or image sources are also included
    in the dictionary as additional data.

    Args:
    - subject (str): the subject of the dictionary entry
    - predicate (str): the predicate of the dictionary entry
    - value (str or list or bs4.element.Tag): the value of the dictionary entry

    Returns:
    - dict: a dictionary with the subject, predicate, and value (and any additional data)
    """
    dict_data = {}
    dict_data['subject'] = subject
    dict_data['subject_stem'] = stem_sentence(subject)
    dict_data['pedicate'] = predicate
    dict_data['pedicate_stem'] = stem_sentence(predicate)
    dict_data['extended_table'] = inner_table
    if isinstance(value, str):
        dict_data['object'] = value.encode(
            'utf-8').decode('utf-8').strip()  # \u00a0 -> &nbsp utf-8
        dict_data['additional_data'] = {}
    elif isinstance(value, list):
        dict_data['object'] = value
        dict_data['additional_data'] = {}
    else:
        dict_data['object'] = value.text.encode(
            'utf-8').decode('utf-8').strip()  # \u00a0 -> &nbsp
        dict_data['additional_data'] = {}
        if value.find('a') is not None:
            dict_data['additional_data']['url'] = value.find('a').get('href')
        else:
            dict_data['additional_data']['url'] = ''
        if value.find('img') is not None:
            dict_data['additional_data']['img'] = value.find('img').get('src')
        else:
            dict_data['additional_data']['img'] = ''

    return dict_data
