import firebase_admin
from firebase_admin import credentials, firestore
import random
from mako.template import Template
import db_adapter
from action import act, TestRequest

def main(request):
    return get_random_anek_page()

def dislike(request):
    return act(request, db_adapter.dislike)

def like(request):
    return act(request, db_adapter.like)

def get_random_anek_page():
    anek, id = db_adapter.select_random_anek()
    return Template(read_file("assets/index.html")).render(anek = anek[db_adapter.TEXT_FIELD_NAME].replace("\n", "<br/>"),
        id = id, likes = len(anek[db_adapter.LIKES_FIELD_NAME]), dislikes = len(anek[db_adapter.DISLIKES_FIELD_NAME]))

def fill_db():
    with open("aneks.txt", "r") as input:
        return db_adapter.add_aneks(list(map(lambda x: x.strip(), input.read().split("~"))))

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

#print(main(1))