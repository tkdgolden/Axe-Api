import { Navbar, NavbarToggler, NavbarBrand, NavbarText, Collapse, Nav, NavItem, NavLink, InputGroup } from "reactstrap";
import { useContext, useState } from "react";
import UserContext from "./UserContext";
import { Navigate } from "react-router-dom";

const JudgeNavBar = () => {
    const { user, setUser } = useContext(UserContext);
    const [isOpen, setIsOpen] = useState(false);

    const toggle = () => setIsOpen(!isOpen);

    const logout = () => {
        setUser("player");
        localStorage.setItem("user", "player");
        Navigate("/");
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
                                <NavLink href="/register">
                                    <i className="tim-icons icon-badge" />
                                    Register
                                </NavLink>
                            </NavItem>
                        </InputGroup>
                        <InputGroup onClick={logout}>
                            <NavItem style={{margin:"auto"}}>
                                <i className="tim-icons icon-single-02" />  
                                <NavbarText>Logout</NavbarText>
                            </NavItem>
                        </InputGroup>
                    </Nav>
                </Collapse>
            </Navbar>
        </>
    );
}

export default JudgeNavBar