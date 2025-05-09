# DPE-Energy-Performance-Analysis-API-server

API server repos submodule for DPE-Energy-Performance-Analysis.

API module with routers to handle communication with database server (RDMS).

## Requirement

You will need the others microservices (at least ETL) to work on this subject.
If used standalone, this repository/image is just an interface with a postgres-db server if credentials are set as well as for a S3 bucket.
ref : *url to main repo*

## LOCAL mode : clone this repo

### config

Add secrets and or env variables into `config/secrets.json`.

Run `pip install -r requirements.txt`

### running

run api with : `python main.py`

## NOLOCAL mode : use docker image

Run `docker run -it DPE-Energy-Performance-Analysis` with port and env variables. 

Those ones are listed below : 

```
ENV = "LOCAL" # with the image set is as NOLOCAL
app-name = "DPE-API"
POSTGRES_PWD = "your-value"
POSTGRES_USER = "your-value"
POSTGRES_PORT = "your-int-value"
API_RUNNING_PORT = "your-int-value"
S3_ACCESS_KEY = "your-value"
S3_SECRET_KEY = "your-value"
```

