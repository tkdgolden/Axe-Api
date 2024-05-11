import { Navbar, NavbarBrand, Nav, NavItem, NavLink, InputGroup } from "reactstrap";


const PlayerNavBar = () => {
    return (
        <>
            <Navbar className="navbar-absolute" expand="lg">
                    <NavbarBrand href="/">Tap That Axe</NavbarBrand>
                    <Nav className="ml-auto" navbar>
                        <InputGroup>
                            <NavItem>
                                <NavLink href="/login">Login as Judge</NavLink>
                            </NavItem>
                        </InputGroup>
                    </Nav>
            </Navbar>
        </>
    );
}

export default PlayerNavBar