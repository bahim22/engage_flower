import React from 'react'
import Navbar from 'react-bootstrap/esm/NavbarBrand'
import Container from 'react-bootstrap/esm/Container'

export const Navi = () => {
  return (
	<>
		<Navbar bg='dark' variant='dark'>
			<Container>
				<Navbar.Brand href='#base' >
					<img
						alt='base'
						src='../../public/logo512.png'
						className=''
						width={25}
						height={25}
					/>{' '}
					Hima Hima Hima
				</Navbar.Brand>
			</Container>
		</Navbar>
	</>
  );
}

