import { Navbar, NavbarBrand, Nav, NavItem, NavLink, InputGroup, NavbarToggler } from "reactstrap";
import Sidebar from "./Sidebar";
import { useState } from "react";
import classNames from "classnames";


const PlayerNavBar = () => {
    const [sidebarOpened, setsidebarOpened] = useState(
        document.documentElement.className.indexOf("nav-open") !== -1
    );
    const toggleSidebar = () => {
        document.documentElement.classList.toggle("nav-open");
        setsidebarOpened(!sidebarOpened);
    };

    return (
        <>
            <Navbar className="navbar-absolute" expand="lg">
                <div
                    className={classNames("navbar-toggle d-inline", {
                        toggled: sidebarOpened,
                    })}
                >
                    <NavbarToggler onClick={toggleSidebar}>
                        <span className="navbar-toggler-bar bar1" />
                        <span className="navbar-toggler-bar bar2" />
                        <span className="navbar-toggler-bar bar3" />
                    </NavbarToggler>
                </div>
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
        </>
    );
}

export default PlayerNavBar