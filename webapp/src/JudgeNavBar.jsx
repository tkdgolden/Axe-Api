import { Navbar, NavbarToggler, NavbarBrand, Collapse, Nav, NavItem, NavLink, InputGroup } from "reactstrap";
import { useContext, useState } from "react";
import UserContext from "./UserContext";

const JudgeNavBar = () => {
    const { user, setUser } = useContext(UserContext);
    const [isOpen, setIsOpen] = useState(false);

    const toggle = () => setIsOpen(!isOpen);

    const logout = () => {
        setUser("player");
        localStorage.setItem("user", "player");
        navigate("/");
    }

    return (
        <>
            <Navbar className="navbar-absolute" expand="lg">
                <NavbarBrand href="/">Tap That Axe</NavbarBrand>
                <NavbarToggler onClick={toggle}>
                    <span className="navbar-toggler-bar navbar-kebab" />
                    <span className="navbar-toggler-bar navbar-kebab" />
                    <span className="navbar-toggler-bar navbar-kebab" />
                </NavbarToggler>
                <Collapse isOpen={isOpen} navbar>
                    <Nav className="ml-auto" navbar>
                        <InputGroup>
                            <NavItem>
                                <NavLink href="/register">Register New Judge</NavLink>
                            </NavItem>
                        </InputGroup>
                        <InputGroup onClick={logout}>
                            <NavItem>
                                Log Out
                            </NavItem>
                        </InputGroup>
                    </Nav>
                </Collapse>
            </Navbar>
        </>
    );
}

export default JudgeNavBar