# writing to CSV
import json
import shutil
from zipfile import ZipFile
import os
from datetime import datetime
import csv
from logger import logger_handler
logger = logger_handler.logger

def write_document_file(document):
    row1 = ['Number of url links', len(document['url_links'])]
    row2 = ['Number of pdf file links', len(document['doc_links'])]
    now = datetime.now()  # current date and time

    #path for files
    if os.path.exists("files") is False:
        os.mkdir("files")
    sitemap_path = os.path.join("files", "site_map")
    if os.path.exists(sitemap_path) is False:
        os.mkdir(sitemap_path)
    date_path = os.path.join(sitemap_path, now.strftime("%m_%d_%Y_%H_%M_%S") )
    if os.path.exists(date_path) is False:
        os.mkdir(date_path)
    doc_path = os.path.join(date_path, "documents" )
    if os.path.exists(doc_path) is False:
        os.mkdir(doc_path)

    # writing to json file
    with open("{}/sitemap.json".format(doc_path), "w", encoding="utf-8") as sitemap_json:
        json_object = json.dumps(document['url_links'], indent=4)
        sitemap_json.write(json_object)
    document['sitemap_json'] = sitemap_json.name
    
    # writing to csv file
    with open("{}/report.csv".format(doc_path), 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        header = ['Items', 'Number']
        # writing the fields
        csvwriter.writerow(header)
        csvwriter.writerow(row1) 
        csvwriter.writerow(row2)
        csvfile.close()
    document['csv_file'] = csvfile.name

    with open("{}/urls_file.txt".format(doc_path), 'w', encoding="utf-8") as urls_file:
        for item in document['url_links']:
            urls_file.write("%s\n" % item)
        ('Done writing urls links to file')
    document['urls_file'] = urls_file.name

    # writing docs links to a text file
    with open("{}/docs_file.txt".format(doc_path), 'w', encoding="utf-8") as docs_file:
        for idx, item in enumerate(document['doc_links'], start=1):
            # write each item on a new line
            docs_file.write("%s\n" % item)
        logger.info('Done writing docs links to a file')
    document['docs_file'] = docs_file.name

    document['dir_path'] = doc_path

       # writing files to a zipfile
    shutil.make_archive(date_path+"/sitemap", 'zip', doc_path)

    # file_paths = get_all_file_paths(path)
    # print('Following files will be zipped:')
    # for file_name in file_paths:
    #     print(file_name)

    #    # writing files to a zipfile
    # with ZipFile('{}/document.zip'.format(path), 'w') as zip_file:
    #     # writing each file one by one
    #     for file in file_paths:
    #         zip_file.write(file)
    # logger.info('All files zipped successfully!')

    document['zip_file'] = '{}/sitemap.zip'.format(date_path)
    # logger.info(document['zip_file'])

    return document


def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


# def test():
#     row1 = ['Number of url links', 22]
#     row2 = ['Number of pdf file links', 121]
#     path = os.path.join("files/", now.strftime("%m_%d_%Y_%H_%M_%S"))
#     os.mkdir(path)
#     with open("{}/report{}.csv".format(path, now.strftime("_%m_%d_%Y_%H_%M_%S")), 'w', newline='') as csvfile:
#         # creating a csv writer object
#         csvwriter = csv.writer(csvfile)

#         # writing the fields
#         csvwriter.writerow(row1)
#         csvwriter.writerow(row2)
#         csvfile.close()
#     return csvfile.name
