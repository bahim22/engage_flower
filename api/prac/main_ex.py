# for PostgreSQL Server
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from urllib.parse import quote_plus

host_server = os.environ.get('host_server', 'localhost')
db_server_port = quote_plus(str(os.environ.get('db_server_port', '5432')))
db_name = os.environ.get('db_name', 'fastapi')
db_uname = quote_plus(str(os.environ.get('db_uname', 'postgres')))
db_passwrd = quote_plus(str(os.environ.get('db_passwrd', 'secre_key')))
ssl_mode = quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

DATABASE_URL = f'postgresql://{db_uname}:{db_passwrd}@{host_server}:{db_server_port}/{db_name}?sslmode={ssl_mode}'

dbsection1 = f'postgresql://{db_uname}:{db_passwrd}@'
dbsection2 = f'{host_server}:{db_server_port}/{db_name}?sslmode={ssl_mode}'
db_url2 = f'{dbsection1}{dbsection2}'

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


app = FastAPI()

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


@app.get("/")
async def main() -> dict[str, str]:
    return {"message": "Welcome Middleware"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

######
#  Original base example

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Welcome to DeD"}
#####
