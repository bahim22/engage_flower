import React, { useEffect, useState } from "react";

const NoteList = () => {
	const [notes, setNotes] = useState([]);
	const EndPoint = process.env.EndPoint || `/notes/`;

	useEffect(() => {
		fetch('http://localhost:8000/notes')
		// fetch(`${EndPoint}/notes`)
			.then((response) => response.json())
			.then((data) => setNotes(data));
	}, []);

	return (
		<div className="container">
			<h1>Notes</h1>
			<ul className="list-group">
				{notes.map((note) => (
					<>
						<li key={note.id} className="list-group-item">
							{note.title}
						</li>
						<li className="list-group-item">
							{note.text}
						</li>
					</>
				))}
			</ul>
       </div>
	);
};

export default NoteList;