import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
// import NavBar from './NavBar.jsx';
import JudgeHome from './JudgeHome.jsx';
import LoginForm from './LoginForm.jsx';
import RegisterForm from "./RegisterForm.jsx";
import UserContext from './UserContext';
import React, { useContext } from 'react';
import JudgeNavBar from "./JudgeNavBar.jsx";
import PlayerNavBar from "./PlayerNavBar.jsx";
import PlayerHome from "./PlayerHome.jsx";
import SeasonStats from "./SeasonStats";
import TournamentStats from "./TournamentStats";
import DisciplineStats from "./DisciplineStats";

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
                    <JudgeNavBar />
                    <h1>This is the router</h1>
                    <Routes>
                        <Route path="/" element={<JudgeHome />}></Route>
                        <Route path="/register" element={<RegisterForm />}></Route>
                        <Route path="*" element={<Navigate to="/" />}></Route>
                    </Routes>
                </BrowserRouter>
            </>
        );
    }


    return (
        <>
            <BrowserRouter>
                <PlayerNavBar />
                <h1>This one</h1>
                <Routes>
                    <Route path="/" element={<PlayerHome />}></Route>
                    <Route path="/login" element={<LoginForm />}></Route>
                    <Route path="/season-stats" element={<SeasonStats />}></Route>
                    <Route path="/tournament-stats" element={<TournamentStats />}></Route>
                    <Route path="/discipline-stats" element={<DisciplineStats />}></Route>
                    <Route path="*" element={<Navigate to="/" />}></Route>
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default Router