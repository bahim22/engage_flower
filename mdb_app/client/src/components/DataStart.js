import React, { useEffect, useState } from 'react';

export function MyComponent() {
	const [data, setData] = useState([]);

	useEffect(() => {
		fetch('/api/endpoint') // Replace with your actual API endpoint
			.then((response) => response.json())
			.then((data) => setData(data));
	}, []);

	return <div style='background-color:#f2f2f2 padding:20px'>{/* Display the data here */}</div>;
}

const NavTabs = () => {
	return (
		<>
			<ul className='nav nav-tabs' id='navId'>
				<li className='nav-item'>
					<a href='#tab1Id' className='nav-link active'>
						Active
					</a>
				</li>
				<li className='nav-item dropdown'>
					<a
						className='nav-link dropdown-toggle'
						data-toggle='dropdown'
						href='#'
						role='button'
						aria-haspopup='true'
						aria-expanded='false'>
						Dropdown
					</a>
					<div className='dropdown-menu'>
						<a className='dropdown-item' href='#tab2Id'>
							Action
						</a>
						<a className='dropdown-item' href='#tab3Id'>
							Another action
						</a>
						<div className='dropdown-divider'></div>
						<a className='dropdown-item' href='#tab4Id'>
							Action
						</a>
					</div>
				</li>
				<li className='nav-item'>
					<a href='#tab5Id' className='nav-link'>
						Another link
					</a>
				</li>
				<li className='nav-item'>
					<a href='#' className='nav-link disabled'>
						Disabled
					</a>
				</li>
			</ul>
			{/* // <!-- Tab panes --> */}
			<div className='tab-content'>
				<div className='tab-pane fade show active' id='tab1Id' role='tabpanel'></div>
				<div className='tab-pane fade' id='tab2Id' role='tabpanel'></div>
				<div className='tab-pane fade' id='tab3Id' role='tabpanel'></div>
				<div className='tab-pane fade' id='tab4Id' role='tabpanel'></div>
				<div className='tab-pane fade' id='tab5Id' role='tabpanel'></div>
			</div>
		</>
	);
};

{
	/*
<script>
	$('#navId a').click(e => {
		e.preventDefault();
		$(this).tab('show');
	});
</script>
*/
}

// import React from 'react';

export const Start = () => {
	return (
		<>
			<div className='card' style='background-color:cadetblue; border-color:darkblue;'>
				<img className='card-img-top' src='holder.js/100x180/' alt='' />
				<div className='card-body'>
					<h4 className='card-title'>Title</h4>
					<p className='card-text'>Text</p>
				</div>
			</div>
		</>
	);
};

import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';

export function TableTwo() {
	return (
		<>
			<div classNameName='container my-custom-table'>
				<table className='table table-striped table-inverse table-responsive'>
					<thead className='thead-inverse'>
						<tr>
							<th></th>
							<th></th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td scope='row'></td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td scope='row'></td>
							<td></td>
							<td></td>
						</tr>
					</tbody>
				</table>
			</div>
			<table style='background-color:#f2f2f2 padding: 20px'></table>
		</>
	);
}
