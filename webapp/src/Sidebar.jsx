/*!

=========================================================
* Black Dashboard React v1.2.2
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/black-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
/*eslint-disable*/
import { useState } from "react";


// reactstrap components
import { Nav, NavLink, InputGroup, Button, Modal, ModalHeader, Input } from "reactstrap";



function Sidebar() {

    const [modalSearch, setmodalSearch] = useState(false);
    // this function is to open the Search modal
    const toggleModalSearch = () => {
        setmodalSearch(!modalSearch);
    };

    return (
        <div className="sidebar" data="green">
            <div className="sidebar-wrapper">
                <Nav>
                    <li>
                        <NavLink href="/" className="nav-link">
                            <i className="tim-icons icon-trophy" />
                            Overall Stats View
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="/season-stats" className="nav-link">
                            <i className="tim-icons icon-chart-bar-32" />
                            Season Stats View
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="/tournament-stats" className="nav-link">
                            <i className="tim-icons icon-vector" />
                            Tournament Stats View
                        </NavLink>
                    </li>
                    <li>
                        <NavLink href="/discipline-stats" className="nav-link">
                            <i className="tim-icons icon-settings" />
                            Discipline Stats View
                        </NavLink>
                    </li>
                    <li>
                        <InputGroup className="search-bar">
                            <i className="tim-icons icon-zoom-split" />
                            <Input placeholder="SEARCH PLAYER" type="text" />
                        </InputGroup>
                    </li>
                </Nav>
            </div>
        </div>
    )
}

export default Sidebar;
