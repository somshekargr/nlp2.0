import json

def convert_to_json(user_query, auto_corrected_query, source, result):
    data = {
        'user_query': user_query,
        'auto_corrected_query': auto_corrected_query,
        'source': source,
        'result': result
    }

    return data
