"""
    This file contains code to help reflect the number files in each sub-directories.
"""

import json
import os
import os.path

DIR_PATH = './classified_files'
total_files = {}

for name in os.listdir(DIR_PATH):
    total_files[name] = len([file_name for file_name in os.listdir(
        os.path.join(DIR_PATH, name)) if file_name != 'init_config.ini'])

total_files_data = dict(sorted(total_files.items(), key=lambda item: item[1]))
#print(total_files_data.items())

with open('./templates/file_count.json', 'w+',encoding="utf-8") as file:
    file.write(json.dumps(total_files_data))
