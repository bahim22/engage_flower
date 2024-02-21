
# Example Full app

1. **Set Up FastAPI Backend:**
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/db_name"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for development purposes (update with your specific frontend URL)
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/notes")
async def get_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return notes
```

2. **Set Up React Frontend:**
```bash
npx create-react-app frontend
cd frontend
npm install bootstrap
```

3. **Create React Component to Display Notes:**
```jsx
// src/components/NoteList.js
import React, { useEffect, useState } from 'react';

const NoteList = () => {
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    fetch('/api/notes') // Replace with your actual FastAPI endpoint
      .then((response) => response.json())
      .then((data) => setNotes(data));
  }, []);

  return (
    <div className="container">
      <h1>Notes</h1>
      <ul className="list-group">
        {notes.map((note) => (
          <li key={note.id} className="list-group-item">
            {note.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NoteList;
```

4. **Incorporate NoteList Component in App.js:**
```jsx
// src/App.js
import React from 'react';
import NoteList from './components/NoteList';

function App() {
  return (
    <div>
      <NoteList />
    </div>
  );
}

export default App;
```

5. **Run FastAPI Backend:**
```bash
uvicorn main:app --reload
```

6. **Start React Development Server:**
```bash
npm start
```

With these steps, you'll have a fully functional app where the FastAPI backend serves note data from a PostgreSQL database, and the React frontend displays it using the Bootstrap CSS framework.