import { Navbar, Nav } from 'react-bootstrap';

function Header() {

    return (
        <Navbar bg="light" expand="lg" className='mt-3 mt-sm-0'>
            <Navbar.Brand href="#home" className="mb-0 h1 d-flex">Alfred
                <span className="fw-light d-none d-sm-block ms-2"> Dein persönlicher SAP Assistent.</span>
            </Navbar.Brand>
            {/*<Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="#home">Einstellungen</Nav.Link>
                    <Nav.Link href="#about">Über uns</Nav.Link>
                </Nav>
            </Navbar.Collapse>*/}
        </Navbar>
    )
}

export default Header