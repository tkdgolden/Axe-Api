import { Navbar, NavbarBrand, Nav, NavItem, NavLink, InputGroup } from "reactstrap";
import Sidebar from "./Sidebar";


const PlayerNavBar = () => {
    return (
        <>
            <Navbar className="navbar-absolute" expand="lg">
                    <NavbarBrand href="/">Tap That Axe</NavbarBrand>
                    <Nav className="ml-auto" navbar>
                        <InputGroup>
                            <NavItem>
                                <NavLink href="/login">
                                    <i className="tim-icons icon-key-25" />  
                                    Login as Judge
                                </NavLink>
                            </NavItem>
                        </InputGroup>
                    </Nav>
            </Navbar>
            <Sidebar></Sidebar>
        </>
    );
}

export default PlayerNavBar