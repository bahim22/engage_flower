# app/main.py with db

from sqlite3 import connect
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
import urllib

# define connection string for app and sqlite db to communicate
DB_URL = "sqlite:///./test.db"
# create instance of database
database = databases.Database(DB_URL)

# create SQL Alchemy model. Table named notes, that stores detial of note \
# in text column and status in completed column. \
# sqlAlchemy defines the notes table so it matches w/ the relational db \
# schema in form of Python code

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DB_URL, connect_args={"check_same_thread": False}
    # DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


""" @asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to DB then release DB
    database.connect()
    yield
    await database.disconnect() """

app = FastAPI(title="FastAPI Prac App")

origins: list[str] = [
    "http://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8000/"
    "http://127.0.0.1:3000/"
]


app.add_middleware(
    CORSMiddleware,
    all_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# create/insert a new note in notes table
@app.post('/notes/', response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), 'id': last_record_id}


# update/modify existing notes in notes table
@app.put('/notes/{note_id}/', response_model=Note,
         status_code=status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):  # type: ignore
    query = notes.update().where(notes.c.id == note_id).values(
        text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), 'id': note_id}

# get a paginated list/collection of notes that're in table,
# get a single note | delete an existing note
# 	based on id given in the request as a note_id query :param


@app.get("/notes/", response_model=List[Note],
         status_code=status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):  # type: ignore
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note,
         status_code=status.HTTP_200_OK)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.delete("/notes/{note_id}/", status_code=status.HTTP_200_OK)
async def update_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {
        "message": "Note with id: {} deleted successfully!".format(note_id)
        }
