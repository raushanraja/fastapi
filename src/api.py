import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .db import Person as PersonMongo

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


class Person(BaseModel):
    name: str


app = APIRouter()


@app.get('/', response_model=Person)
def get_person():
    new_person = PersonMongo(name='josh')
    new_person.save()
    josh = PersonMongo.objects().first().to_mongo().to_dict()
    return josh


@app.get('/test')
def test_html(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})
