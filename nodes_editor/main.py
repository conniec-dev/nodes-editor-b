from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "nodes-editor",
})

db = firestore.client()

class DrawflowDiagram(BaseModel):
    name: str
    drawflow_output: str


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "OK"

@app.post("/item")
async def create_item(item: DrawflowDiagram):

    doc_ref = db.collection(u'drawflowdiagrams').document()
    new_doc_id = doc_ref.id
    item_dict = item.dict()
    item_dict["id"] = new_doc_id
    item_dict["date"] = firestore.SERVER_TIMESTAMP
    doc_ref.set(item_dict)
    return f"{item_dict['name']} was stored successfully"

# @app.get("/programs")
# async def list_programs():
#     doc_ref = db.collection(u'drawflowdiagrams')
#     docs = doc_ref.stream()
#     list_of_programs = []

#     for doc in docs:
#         list_of_programs.append(doc.id)

#     return list_of_programs

@app.get("/programs")
async def list_programs():
    doc_ref = db.collection(u'drawflowdiagrams')
    docs = doc_ref.stream()
    list_of_programs_id = []
    list_of_values = []

    for doc in docs:
        list_of_programs_id.append(doc.id)
        list_of_values.append(doc.to_dict())
        dict_of_programs = dict(zip(list_of_programs_id, list_of_values))

    return dict_of_programs

@app.get("/programs/{program_id}")
async def get_program(program_id: str):
    doc_ref = db.collection(u'drawflowdiagrams')
    docs = doc_ref.stream()
    list_of_programs_id = []
    list_of_values = []

    for doc in docs:
        list_of_programs_id.append(doc.id)
        list_of_values.append(doc.to_dict())
        dict_of_programs = dict(zip(list_of_programs_id, list_of_values))

    if program_id in dict_of_programs:
        return (dict_of_programs[program_id])
    else:
        return("The program doesn't exist")