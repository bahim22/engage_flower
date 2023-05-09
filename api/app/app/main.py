from fastapi import FastAPI
import polls.endpoints

app = FastAPI()
app.include_router(polls.endpoints.router, prefix="/polls")


@app.get("/")
async def root():
    return {"message": "Main.py Init Message"}
# uvicorn app.main:app --reload
