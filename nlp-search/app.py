import os
import sys
from configparser import ConfigParser
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Request
from search_engine.es_search import es_data_search, es_multichannel_data_search
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Read configuration from .env file
config = ConfigParser()
config.read(".env")
IP = config.get("server", "ip")
PORT = int(config.get("server", "port"))

app = FastAPI(debug=True, docs_url='/nlp/docs',
              redoc_url='/nlp/redocs', openapi_url='/nlp/openapi.json')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/nlp/search")
async def root(request: Request):
    data = await request.json()
    result = es_data_search(data['user_query'])
    return result

@app.post("/nlp/multichannel_search")
async def root(request: Request):
    data = await request.json()
    result = es_multichannel_data_search(data['user_query'])
    return result

if __name__ == "__main__":
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=PORT)
