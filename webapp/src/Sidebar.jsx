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


// reactstrap components
import { DropdownToggle, Nav, NavLink, UncontrolledDropdown, DropdownMenu, DropdownItem } from "reactstrap";
import PlayerSearchForm from "./PlayerSearchForm";
import useGetFilteredPlayers from "./hooks/useGetFilteredPlayers";
import { useNavigate } from 'react-router-dom';


function Sidebar() {
    const navigate = useNavigate();
    const [players, setPlayers, searchPlayers] = useGetFilteredPlayers();

    console.log(players);

    if (players.length === 1) {
        const playerId = players[0][0];
        setPlayers([])
        navigate(`/player-stats/${playerId}`);
    }
    else {
        return (
            <div className="sidebar" data="green">
                <div className="sidebar-wrapper">
                    <Nav>
                        <li>
                            <NavLink href="/" className="nav-link">
                                <i className="tim-icons icon-trophy" />
                                Overall Stats
                            </NavLink>
                        </li>
                        <li>
                            <NavLink href="/season-stats" className="nav-link">
                                <i className="tim-icons icon-chart-bar-32" />
                                Stats by Season
                            </NavLink>
                        </li>
                        <li>
                            <NavLink href="/tournament-stats" className="nav-link">
                                <i className="tim-icons icon-vector" />
                                Tournament Stats View
                            </NavLink>
                        </li>
                        <li>
                            <PlayerSearchForm searchPlayers={searchPlayers} />
                        </li>
                    </Nav>
                </div>
            </div>
        )
    }



}

export default Sidebar;
