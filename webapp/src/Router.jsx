import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
// import NavBar from './NavBar.jsx';
import JudgeHome from './JudgeHome.jsx';
import LoginForm from './LoginForm.jsx';
import RegisterForm from "./RegisterForm.jsx";
import UserContext from './UserContext';
import React, { useContext } from 'react';
import JudgeNavBar from "./JudgeNavBar.jsx";
import PlayerNavBar from "./PlayerNavBar.jsx";
import OverallStats from "./OverallStats.jsx";
import SeasonStats from "./SeasonStats";
import TournamentStats from "./TournamentStats";
import Sidebar from "./Sidebar.jsx";
import DisciplineStats from "./DisciplineStats";
import PlayerStats from "./PlayerStats.jsx";
import { Container, Col, Row } from "reactstrap";

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
                    <div className="wrapper">
                        <JudgeNavBar />
                        <div className="judge main-panel">
                            <Routes>
                                <Route path="/" element={<JudgeHome />}></Route>
                                <Route path="/register" element={<RegisterForm />}></Route>
                                <Route path="*" element={<Navigate to="/" />}></Route>
                            </Routes>
                        </div>
                    </div>

                </BrowserRouter>
            </>
        );
    }


    return (
        <>
            <BrowserRouter>
                <div className="wrapper">
                    <PlayerNavBar />
                    <Sidebar />
                    <div className="main-panel">
                        <Routes>
                            <Route path="/overall-stats" element={<OverallStats />}></Route>
                            <Route path="/login" element={<LoginForm />}></Route>
                            <Route path="/season-stats" element={<SeasonStats />}></Route>
                            <Route path="/season-stats/:seasonId" element={<SeasonStats/>}></Route>
                            <Route path="/tournament-stats/:tournamentId" element={<TournamentStats />}></Route>
                            <Route path="/tournament-stats" element={<TournamentStats />}></Route>
                            <Route path="/discipline-stats/:discipline" element={<DisciplineStats />}></Route>
                            <Route path="/discipline-stats" element={<DisciplineStats />}></Route>
                            <Route path="/player-stats" element={<PlayerStats />}></Route>
                            <Route path="*" element={<Navigate to="/overall-stats" />}></Route>
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        </>
    );
};

export default Router