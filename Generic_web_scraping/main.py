import json
from logger import logger_handler
from fastapi.middleware.cors import CORSMiddleware
from multiprocessing.dummy import Array
import os
from pydantic import BaseModel
from site_map.write_file import write_document_file
from site_map.get_sites import get_urls, get_doc_links
from html_dump_retrieval.generate_report import get_dump_with_report
from dump_classifiction.classifiction import html_classification
from get_tag_attr import get_tag_with_attr
from generate_json.generate_json_files import generate_json_files
from fastapi.responses import FileResponse
from http.client import HTTPResponse
import uvicorn
from common.utils import get_error_details
from configparser import ConfigParser
from typing import List, Optional, Union
from fastapi import HTTPException, FastAPI
import requests
# Disable the annoying "Unverified HTTPS request is being made" warning
requests.packages.urllib3.disable_warnings()

config_file_path = './config.ini'
config = ConfigParser()
config.read(config_file_path)

api_port = config.get("application", "api_port")

http_proxy = config.get("proxies", "http")
https_proxy = config.get("proxies", "https")

proxies = {"http": http_proxy, "https": https_proxy} if (
    http_proxy and https_proxy) else None
# logging
logger = logger_handler.logger
# app = FastAPI()
app = FastAPI(debug=True, docs_url='/dws/docs',
              redoc_url='/dws/redocs', openapi_url='/dws/openapi.json')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParentChildUrl(BaseModel):
    parent: str
    child: str

class SiteMapLink(BaseModel):
    url_links: List[Union[ParentChildUrl, None]] = None
    doc_links: Optional[List[str]]

class SiteMapRequest(BaseModel):
    url: str
    toZip: bool

class InsertDocRequest(BaseModel):
    folder_path: str    
    csv_file_path : str
class ClassificationRequest(BaseModel):
    dumps_path : str
    report_path : str
    
class FileDownloadRequest(BaseModel):
    file_path : str

class GetDumpRequest(BaseModel):
    site_map : str
    zip_file : str
    
# @app.post('/dws/get_site_map')
# def get_site_map(req_data:SiteMapRequest):
#     url = req_data.url
#     toZip = req_data.toZip
#     logger.info("Retriving sitemap for {} and toZip is {} ".format(url, toZip))
#     try:
#         # getting url n docs link
#         document = get_urls(url)

#         if toZip:
#             # writing csv file n gets filename
#             document = write_document_file(document)
#             logger.info("Sitemap zip file successfully retrived.")
#             return FileResponse(document['zip_file'], media_type="application/zip", filename="sitemap.zip")

#         else:
#             if document is not None:
#                 logger.info("Sitemap successfully retrived.")
#                 return {'url_links': document["url_links"], 'doc_links': document["doc_links"]}
#             return f"Scraping could not be done on the provided url: {url}"
#     except Exception:
#         logger.error("error while retriving site map for {} : {}".format(
#             url, get_error_details()))
#         raise HTTPException(status_code=500, detail=get_error_details())

@app.post('/dws/get_site_map')
def get_site_map(req_data:SiteMapRequest):
    url = req_data.url
    toZip = req_data.toZip
    # logger.info("Retriving sitemap for {} and toZip is {} ".format(url, toZip))
    try:
        # getting url n docs link
        document = get_urls(url)

        # writing csv file n gets filename
        document = write_document_file(document)
        # logger.info("Sitemap zip file successfully retrived.")
        # return FileResponse(document['zip_file'], media_type="application/zip", filename="sitemap.zip")

        
        # logger.info("Sitemap successfully retrived.")
        return {'site_map': document["sitemap_json"], 'zip_file': document["zip_file"]}

    except Exception:
        # logger.error("error while retriving site map for {} : {}".format(
        #     url, get_error_details()))
        raise HTTPException(status_code=500, detail=get_error_details())


# @app.post('/dws/get_html_dumps')
# def get_html(body: SiteMapLink):
#     try:
#         logger.info("Retriving html dumps")
#         response = get_dump_with_report(body.url_links)
#         return response

#     except Exception:
#         logger.error("Error while fetching html dump")
#         raise HTTPException(status_code=500, detail=get_error_details())

@app.post('/dws/get_html_dumps')
def get_html(body: GetDumpRequest):
    try:
        f = open(body.site_map)
        url_links = json.load(f)
        # logger.info("Retriving html dumps")
        response = get_dump_with_report(url_links)
        return response

    except Exception:
        # logger.error("Error while fetching html dump")
        raise HTTPException(status_code=500, detail=get_error_details())


@app.post("/dws/classification")
def classify_dump(req_data : ClassificationRequest):
    dump_path = req_data.dumps_path
    csv_file_path = req_data.report_path
    try:
        logger.info("classifing htmps dumps from file path : " + dump_path)
        if os.path.exists(dump_path):
            print("folder exists")
            file = html_classification(dump_path, csv_file_path)
            if file is False:
                raise HTTPException(
                    status_code=500, detail="Internal Server Error")
            else:
                return file

        else:
            logger.info("Folder Not Found : {}".format(dump_path))
            return HTTPException(status_code=404, detail="Not found")
    except:
        logger.info("Error While classifing ".format(dump_path))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/dws/insert_documents")
def generate_and_insert_docs(req_data : InsertDocRequest):
    classified_dir_path = req_data.folder_path
    csv_file_path = req_data.csv_file_path
    try:
        print("Generating the json documents")
        response = generate_json_files(classified_dir_path, csv_file_path)
        return response

    except:
        logger.info("Error While json document creation and insertion")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/dws/download_file")
def download_file(req_data : FileDownloadRequest):
    file_path = req_data.file_path
    if os.path.isfile(file_path):
        logger.info("Filepath : {}".format(file_path))
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_extension = os.path.splitext(file_path)[1]
        return FileResponse(file_path, media_type="application/"+file_extension.replace(".", ""), filename=file_name+file_extension)
    else:
        logger.error("File Not Found : {}".format(file_name))
        raise HTTPException(status_code=404, detail="Not found")


@app.get('/dws/test2')
def test(): 

    try:
        return "ok"
    except Exception:
        print("error while retriving site map for {} : {}".format(
            get_error_details()))
        raise HTTPException(status_code=500, detail=get_error_details())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(api_port))
