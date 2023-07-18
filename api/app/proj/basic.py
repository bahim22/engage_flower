# for PostgreSQL Server

from typing import List, Union
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
# import api.app.polls.endpoints as poll_endpoints
# from fastapi import APIRouter
from pydantic import BaseModel
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv('../.env.local')


host_server = os.environ.get('PGHOST', 'host')
db_server_port = quote_plus(str(os.environ.get('PGPORT', '5432')))
db_name = os.environ.get('PGDATABASE', 'postgres')
db_uname = quote_plus(str(os.environ.get('PGUSER', 'uname')))
db_password = quote_plus(str(os.environ.get('PGPASSWORD', 'password')))
ssl_mode = quote_plus(str(os.environ.get('sslmode', 'prefer')))
# host_server = os.environ.get('PGHOST', 'localhost')
# db_server_port = os.environ.get('PGPORT')
# db_name = os.environ.get('PGDATABASE', 'dev_db')
# db_uname = os.environ.get('PGUSER')
# db_password = os.environ.get('PGPASSWORD')
# ssl_mode = os.environ.get('sslmode')

DATABASE_URL = f'postgresql://{db_uname}:{db_password}@{host_server}:' \
    + f'{db_server_port}/{db_name}?sslmode={ssl_mode}'
# DATABASE_URL = f'postgresql://{db_uname}:{db_password}@{host_server}:' \
#     + f'{db_server_port}/{db_name}?sslmode={ssl_mode}'

# cnx = psycopg2.connect(user="hapg", password="{your_password}", host="glrp1.postgres.database.azure.com", port=5432, database="")

# DBURL = f'postgresql://glrp1.postgres.database.azure.com:5432/?user=hapg&password={password}&sslmode=require'

# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}' \
#     .format(db_uname, db_password, host_server,
#             db_server_port, db_name, ssl_mode)

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


app = FastAPI(title="Hima App using FastAPI, Azure PostgreSQL \
    DB Async EndPoints")

# origins: list[str] = [
#     "http://localhost",
#     "http://localhost:8000",
#     "https://localhost:8000",
#     "http://127.0.0.1:8000/",
#     "http://127.0.0.1:5432/",
#     "http://127.0.0.1:3000/",
#     "http://127.0.0.1:5050/",
# ]

app.add_middleware(
    CORSMiddleware,
    # all_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

# app.include_router(poll_endpoints.APIRouter)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @app.get("'/api/polls/")
@app.get("/")
async def root() -> Union[str, dict]:
    return {"Alert": "API is Live and Connected!"}


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
