
# Display response data from a MongoDB

## from a table requested via FastAPI using React

1. Set up a FastAPI backend: Create an API endpoint in FastAPI that connects to your MongoDB database, retrieves the data from the desired table, and sends it as a response.

2. Create React App & Fetch data from the API: In your React component, use the `fetch` or `axios` library to make an HTTP request to the FastAPI endpoint you created. This will retrieve the data from the MongoDB table.
   1. fetch data in React using the `fetch` function:

   ```jsx
   import React, { useEffect, useState } from 'react';

   function MyComponent() {
     const [data, setData] = useState([]);

     useEffect(() => {
       fetch('/api/endpoint') // Replace with your actual API endpoint
         .then((response) => response.json())
         .then((data) => setData(data));
     }, []);

     return (
       <div>
         {/* Display the data here */}
       </div>
     );
   }
   ```

3. Render the data: Once the data is fetched successfully, you can render it in your React component. You can use JavaScript's array mapping function to iterate over the data and generate the necessary elements.
   1. ex. of rendering the data as a list:

   ```jsx
   function MyComponent() {
     // ...

     return (
       <div>
         <ul>
           {data.map((item) => (
             <li key={item.id}>{item.name}</li>
           ))}
         </ul>
       </div>
     );
   }
   ```

   In this example, it assumes that each item in the data has an `id` and `name` property. Modify it according to your specific data structure.

4. Style and enhance the UI: Apply CSS styles and additional components as needed to enhance the UI and provide a better user experience.

Remember to replace `/api/endpoint` in the code snippets with the actual endpoint URL of your FastAPI server that retrieves the data from the MongoDB table. Additionally, make sure your FastAPI server is running and accessible from your React application.

```js
import React from 'react';
import './styles.css';

function MyComponent() {
  return (
    // <div className="container">
    <div className="container" style="">
      {/* Content */}
    </div>
  );
}
```

```js
import React, { useEffect, useState } from 'react';

function MyComponent() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/endpoint') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      {/* Display the data here */}
    </div>
  );
}
```

## FastAPI with React

- To create the backend server-side of a full-stack web app using FastAPI to retrieve data from a MongoDB table and display it in a React app, you'll need to perform the following steps:

1. Set up FastAPI and MongoDB: Install FastAPI and the necessary MongoDB library (such as `motor`) in your Python environment. Set up the MongoDB connection with the appropriate credentials and database details.

2. Create FastAPI endpoints: Define the necessary FastAPI endpoints to retrieve data from the MongoDB table. This typically involves creating a route that queries the database and returns the data as a JSON response.

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

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

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["your_database_name"]
collection = db["your_collection_name"]


@app.get("/api/data")
async def get_data():
	data = []
	async for document in collection.find():
				data.append(document)
	return data

"""
	In this example, the `/api/data` endpoint queries the `collection` in the specified MongoDB database and returns the data as a JSON response.
"""
```

1. Run the FastAPI server: Start the FastAPI server to make the endpoints available for requests.

```sh
uvicorn main:app --reload
```

Assuming the code is in a file named `main.py`, this command starts the server on `http://localhost:8000` and enables auto-reloading for development.

1. Fetch and display the data in the React app: In your React app, fetch the data from the FastAPI endpoint and display it using the steps outlined in a previous response.

```jsx
   import React, { useEffect, useState } from 'react';

   function MyComponent() {
     const [data, setData] = useState([]);

     useEffect(() => {
       fetch('http://localhost:8000/api/data') // Update with your FastAPI server URL
         .then((response) => response.json())
         .then((data) => setData(data));
     }, []);

     return (
       <div>
         <ul>
           {data.map((item) => (
             <li key={item.id}>{item.name}</li>
           ))}
         </ul>
       </div>
     );
};

  // # replace `'http://localhost:8000/api/data'` with the actual URL of your FastAPI server.
```

- adjust the code based on your specific MongoDB database and collection names, as well as any authentication or additional data processing requirements you may have.


To build the frontend of a full-stack web app using React.js and incorporate the Bootstrap CSS framework, follow these steps:

1. Set Up React App:
   First, create a new React app using Create React App or your preferred method:

   ```bash
   npx create-react-app frontend
   cd frontend
   ```

2. Install Bootstrap:
   Install Bootstrap in your React app using npm:

   ```bash
   npm install bootstrap
   ```

3. Create React Components:
   Create a new component to display the note data from the backend. In this example, we'll create a component called `NoteList`.

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

4. Set Up API Endpoint in FastAPI:
   In your FastAPI backend, create an endpoint that retrieves the note data from the PostgreSQL database and returns it as a JSON response.

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

5. Run FastAPI Backend:
   Run your FastAPI backend to make the `/api/notes` endpoint accessible.

   ```bash
   uvicorn main:app --reload
   ```

6. Incorporate the NoteList Component in App.js:
   In your `App.js` file, import and include the `NoteList` component.

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

7. Start React Development Server:
   Start the React development server:

   ```bash
   npm start
   ```

   The React app will be served at `http://localhost:3000`.

Now you have a full-stack web app with the frontend displaying note data from the backend PostgreSQL database using FastAPI for the API endpoints and React.js with the Bootstrap CSS framework for the frontend.
