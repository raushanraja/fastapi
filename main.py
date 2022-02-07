from fastapi import FastAPI, Request, Depends

DATABASE_URL = "mongodb://raushan:raushan1234@127.0.0.1:27017"
SECRET = "SECRET"


app = FastAPI()
