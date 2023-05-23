import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavbarBrand from 'react-bootstrap/NavbarBrand';
// import NavDropdown from 'react-bootstrap/NavDropdown';

const MainNav = (children) => {
	const author = [
		{
			id: 1,
			img: '/himacard.png',
			name: 'Hima Balde'
		}
	]

	const links = 'https://github.com/bahim22/bahim22'

	return (
		<Container>
			<h1>
				View {author.name} repos at {links}.
			</h1>
			<h2>
				{children}
			</h2>
			<Nav>
				<Navbar>
					<NavbarBrand></NavbarBrand>

				</Navbar>
			</Nav>

		</Container>
	)
};

export default MainNav;