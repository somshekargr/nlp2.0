import csv
import os
from datetime import datetime
import shutil
from html_dump_retrieval.html_dump import get_dom_text
from common.utils import get_error_details
from logger import logger_handler
logger = logger_handler.logger

def get_dump_with_report(document):
    report_data = []
    now = datetime.now()  # current date and time

    if os.path.exists("files") is False:
        os.mkdir("files")
    htmp_dumps_path = os.path.join("files", "html_dumps")
    if os.path.exists(htmp_dumps_path) is False:
        os.mkdir(htmp_dumps_path)
    date_path = os.path.join(htmp_dumps_path, now.strftime("%m_%d_%Y_%H_%M_%S"))
    if os.path.exists(date_path) is False:
        os.mkdir(date_path)
    dump_path = os.path.join(date_path, "dumps")
    if os.path.exists(dump_path) is False:
        os.mkdir(dump_path)
    report_path = os.path.join(date_path, "reports")
    if os.path.exists(report_path) is False:
        os.mkdir(report_path)

    for idx, url in enumerate(document, start=1):
        dom_data = get_dom_text(url['child'], dump_path, idx)
        report_data.append(
            {"Title": dom_data['title'], "Url": url['child'], "FileName": dom_data['file_name'], "Status": dom_data['status']})

    try:
        file = open('{}/report.csv'.format(report_path),
                    'w', newline='', encoding="utf-8")
        with file:
            # identifying header
            header = ['Title', 'Url', 'FileName', 'Status']
            writer = csv.DictWriter(file, fieldnames=header)

            # writing data row-wise into the csv file
            writer.writeheader()
            for data in report_data:
                writer.writerow(data)
            # logger.info("Done generating the report")
    except Exception:
        # logger.error("Error while fetching html dump")
        detail=get_error_details()
        raise Exception(status_code=500, detail= detail)  # type: ignore
    
       # writing files to a zipfile
    shutil.make_archive(date_path+"/document", 'zip', dump_path)

    return {'report_path': file.name, 'dumps_zip_path': date_path+"/document.zip" , 'dumps_path': dump_path}
