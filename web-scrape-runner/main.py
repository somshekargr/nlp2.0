from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from service.web_scrape import web_scrape
from configparser import ConfigParser

# Init App
app = FastAPI(debug=True, docs_url='/runner/docs',
              redoc_url='/runner/redocs', openapi_url='/runner/openapi.json')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config_file_path = './config.ini'
config = ConfigParser()
config.read(config_file_path)

api_port = config.get("application", "api_port")

@app.post('/runner/web_scrape')
def runner():
    document = web_scrape()
    return document


# Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(api_port))



