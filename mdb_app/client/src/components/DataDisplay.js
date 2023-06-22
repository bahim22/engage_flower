import React, { useEffect, useState } from 'react';


export function DataDisplay() {
	const [data, setData] = useState([]);

	useEffect(() => {
		fetch('/api/endpoint') // Replace with your actual API endpoint
			.then((response) => response.json())
			.then((data) => setData(data));
	}, []);

	return (
		<>
			<div className="container">
				<h1>Data Display</h1>
				<table className="table table-striped">
					<thead>
						<tr>
							<th>ID</th>
							<th>Name</th>
							{/* Add more table headers if needed */}
						</tr>
					</thead>
					<tbody>
						{data.map((item) => (
							<tr key={item.id}>
								<td>{item.id}</td>
								<td>{item.name}</td>
								{/* Add more table cells if needed */}
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</>
	);
}
;
