# for PostgreSQL Server

from typing import List, Union
import databases

from sqlalchemy import create_engine, Column, Integer, String, \
    Boolean, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
from urllib.parse import quote_plus
# import api.app.polls.endpoints as poll_endpoints
# from fastapi import APIRouter
from dotenv import load_dotenv
load_dotenv('../.env.local')


host_server = os.environ.get('VER_PG_HOST', 'host')
db_server_port = quote_plus(str(os.environ.get('PGPORT', '5432')))
db_name = os.environ.get('VER_PG_DB', 'verceldb')
db_uname = quote_plus(str(os.environ.get('VER_PG_USER', 'default')))
db_password = quote_plus(str(os.environ.get('VER_PG_PASSWORD', 'password')))
ssl_mode = quote_plus(str(os.environ.get('AZ_sslmode', 'prefer')))


# DATABASE_URL11 = f'postgresql://{db_uname}:{db_password}@' \
#     + f'{host_server}:{db_server_port}/{db_name}?sslmode={ssl_mode}'


DATABASE_URL = f'postgresql://default:S4FtIbAr8Tkh@ep-soft-block-13293107.us-east-1.postgres.vercel-storage.com:5432/verceldb'

database = databases.Database(DATABASE_URL)


metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    # Column("title", String, nullable=False),
    Column("completed", Boolean),
)


engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)

# edit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


class NoteIn(BaseModel):
    text: str
    completed: bool
    # title: str


class Note(BaseModel):
    id: int
    text: str
    completed: bool
    # title: str


app = FastAPI(title="FastAPI, Vercel PostgreSQL \
    App", description="Async API EP with React frontend")

origins: list[str] = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:5050/",
    "http://127.0.0.1:5432/",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
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


@app.get("/")
async def root() -> Union[str, dict]:
    return {"Connection Info": "API for Vercel PG is Live!"}


# edit
""" @app.get("/notes")
async def get_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return notes """


@app.post('/notes/', response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), 'id': last_record_id}


@app.put("/notes/{note_id}/", response_model=Note,
         status_code=status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(
        text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}


@app.get("/notes/", response_model=List[Note], status_code=status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note,
         status_code=status.HTTP_200_OK)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.delete("/notes/{note_id}/", status_code=status.HTTP_200_OK)
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return print({f'message: Note with id: {note_id} deleted successfully!'})
