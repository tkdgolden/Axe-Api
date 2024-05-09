import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
import NavBar from './NavBar.jsx';
import Home from './Home.jsx';
import LoginForm from './LoginForm.jsx';
import UserContext from './UserContext';
import React, { useContext } from 'react';

/**
 * controls which route's are active based on whether the current user is logged in or not
 * redirects if an invalid route is attempted
 * @returns component
 */
const Router = () => {
    const { user, setUser } = useContext(UserContext);

    if (user !== "player") {
        return (
            <>
                <BrowserRouter>
                    <NavBar />
                    <Routes>
                        <Route path="/" element={<Home />}></Route>
                        <Route path="*" element={<Navigate to="/" />}></Route>
                    </Routes>
                </BrowserRouter>
            </>
        );
    }


    return (
        <>
            <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path="/" element={<Home />}></Route>
                    <Route path="/login" element={<LoginForm />}></Route>
                    <Route path="*" element={<Navigate to="/" />}></Route>
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default Router