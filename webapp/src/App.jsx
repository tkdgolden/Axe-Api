import Router from './Router';
import UserContext from './UserContext.jsx';
import React, { useEffect, useState } from 'react';

/**
 * main component, contains user state shared via context with child components
 * can retrieve user from localstorage
 * @returns component
 */
const App = () => {
  const [user, setUser] = useState("player");
  
  console.log(user);

  useEffect(function setUserOnRender() {
    if (localStorage.getItem("user") !== ("player" || null)) {
      setUser(localStorage.getItem("user"));
    }
  }, [localStorage.user]);
  console.log(user);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Router />
    </UserContext.Provider>
  );
};

export default App