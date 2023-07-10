# app/main.py with db

from sqlite3 import connect
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import urllib

# define connection string for app and sqlite db to communicate
DB_URL = "sqlite:///./test.db"
# create instance of database
database = databases.Database(DB_URL)


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

origins: List = [  # or origins: list[str]
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

""" from fastapi import FastAPI
import polls.endpoints

app = FastAPI()
app.include_router(polls.endpoints.router, prefix="/polls")


@app.get("/")
async def root():
    return {"message": "Main.py Init Message"}
# uvicorn app.main:app --reload """
