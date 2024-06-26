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
import PlayerStats from "./PlayerStats.jsx";
import NewSeasonForm from "./NewSeasonForm.jsx";
import NewTournamentForm from "./NewTournamentForm.jsx";
import ScoreSeason from "./ScoreSeason.jsx";
import ScoreTournament from "./ScoreTournament.jsx";
import ScoreMatch from "./ScoreMatch.jsx";

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
                                <Route path="/new-season" element={<NewSeasonForm />}></Route>
                                <Route path="/new-tournament" element={<NewTournamentForm />}></Route>
                                <Route path="/season/:seasonId" element={<ScoreSeason />}></Route>
                                <Route path="/tournament/:tournamentId" element={<ScoreTournament />}></Route>
                                <Route path="/score-match/:matchId" element={<ScoreMatch />}></Route>
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
                            <Route path="/overall-stats/:discipline" element={<OverallStats />}></Route>
                            <Route path="/overall-stats" element={<OverallStats />}></Route>
                            <Route path="/login" element={<LoginForm />}></Route>
                            <Route path="/season-stats" element={<SeasonStats />}></Route>
                            <Route path="/season-stats/:seasonId" element={<SeasonStats/>}></Route>
                            <Route path="/tournament-stats/:tournamentId" element={<TournamentStats />}></Route>
                            <Route path="/tournament-stats" element={<TournamentStats />}></Route>
                            <Route path="/player-stats/:playerId" element={<PlayerStats />}></Route>
                            <Route path="*" element={<Navigate to="/overall-stats" />}></Route>
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        </>
    );
};

export default Router