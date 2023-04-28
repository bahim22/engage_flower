import Container from "react-bootstrap/esm/Container";
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Navi } from "./Navi";
import TableApp from "./Table";
import ToDoApp from "./Todo";

function Layout({children}) {
	return (
		<>
			<Container fluid>
				<Row>
					<Col>
						{children}
						<Navi />
						{/* insert Nav component */}
					</Col>
				</Row>
				<Row>
					<Col>
						{children}
						<TableApp />
						{/* insert body compo */}
					</Col>
					<Col>
						{children}
						<ToDoApp />
						{/* insert body compo */}
					</Col>
				</Row>
				<Row>
					{children}
					{/* Footer Nav */}
				</Row>
			</Container>
		</>
	);
}

export default Layout;