
# FastAPI info

- import FastAPI (Python class that provides functionality for APIs)
- create an "instance"
- Here the app variable will be an "instance" of the class FastAPI.
- create path operation (path refers to last part of the URL from the first /)
  - aka endpoint or route
  - path is main way to separate concerns and resources
- Operations refer to HTTP methods: POST, GET, PUT, DELETE, OPTIONS, HEAD, PATH, TRACE
- DEFINE A PATH OPERATION DECORATOR

1. Schema: def or description; not the code, but abstract def
   1. ex. API paths, param., etc.
2. Data Schema: shape of some data, (ex. JSON content)
   1. JSON attributes and data types they have
3. OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using JSON Schema, the standard for JSON data schemas.

- create __init__.py file so the folder with Python script is recognized as a Python module
- run live server from shell, need to change main:app (depending on dir main.py is located)

```sh
# uvicorn app.main:app --reload
# uvicorn prac.main:app --reload --host 0.0.0.0 --port 80
uvicorn main:app --reload
```

- Use `APIRouter` to declare path ops
- Then make endpoint available by declaring in main.py
