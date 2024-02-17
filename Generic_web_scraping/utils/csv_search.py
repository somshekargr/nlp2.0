import csv
import sys
sys.path.insert(0,'/path/to/mod_directory')


def search_csv(file_path, search_key, search_value):
    with open(file_path, encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader)
        result = []
        for row in reader:
            if search_key in header and row[header.index(search_key)] == search_value:
                d = {}
                for i, val in enumerate(row):
                    d[header[i]] = val
                result.append(d)
    return result

#example usage
# data = search_csv('data/dump_report.csv', 'FileName', 'indianbank_1.txt')
# print(data)