# for PostgreSQL Server

# from contextlib import asynccontextmanager
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
from urllib.parse import quote_plus
# from python-dotenv import load_dotenv
from dotenv import load_dotenv

load_dotenv()

host_server = os.environ.get('host_server', 'localhost')
db_server_port = quote_plus(str(os.environ.get('db_server_port', '5432')))
db_name = os.environ.get('db_name', 'fastapi')
db_uname = quote_plus(str(os.environ.get('db_uname', 'postgres')))
db_passwrd = quote_plus(str(os.environ.get('db_passwrd', 'secre_key')))
ssl_mode = quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

DATABASE_URL = f'postgresql://{db_uname}:{db_passwrd}@{host_server}:' \
    + f'{db_server_port}/{db_name}?sslmode={ssl_mode}'

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI(title="Hima FastAPI, React App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


""" @app.post('/notes/', response_model=Note,\
status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn):  # type: ignore
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), 'id': last_record_id}
"""


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/notes/", response_model=Note,
          status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.put("/notes/{note_id}/", response_model=Note,
         status_code=status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(
        text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}


@app.get("/notes/", response_model=List[Note],
         status_code=status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note,
         status_code=status.HTTP_200_OK)
async def read_notes_id(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.delete("/notes/{note_id}/", status_code=status.HTTP_200_OK)
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
