import { NavLink, useNavigate } from "react-router-dom";
import { Navbar, Nav, NavItem } from "reactstrap";
import UserContext from './UserContext';
import React, { useContext } from 'react';

/**
 * displays nav bar with valid routes based on whether the user is logged in or not
 * @returns component
 */
const NavBar = () => {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();
  const logout = () => {
    setUser("player");
    localStorage.setItem("user", "player");
    navigate("/");
  }

  if (user !== "player") {
    return (
      <div>
        <Navbar expand="md">
          <NavLink to="/" className="navbar-brand">
            Tap That Axe - Judges
          </NavLink>
  
          <Nav className="ml-auto" navbar>
            <NavItem>
              <button onClick={logout}>Log Out {user}</button>
            </NavItem>
            <NavItem>
              <NavLink to="/register">Register a New Judge</NavLink>
            </NavItem>
          </Nav>
        </Navbar>
      </div>
    );
  }

  return (
    <div>
      <Navbar expand="md">
        <NavLink to="/" className="navbar-brand">
          Tap That Axe - Players
        </NavLink>

        <Nav className="ml-auto" navbar>
          <NavItem>
            <NavLink to="/login">Log In</NavLink>
          </NavItem>
        </Nav>
      </Navbar>
    </div>
  );
};

export default NavBar;