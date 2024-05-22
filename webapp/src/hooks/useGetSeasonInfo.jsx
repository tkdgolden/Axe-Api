import { useState, useEffect } from 'react';
import AxeApi from "../Api.jsx";

const useGetSeasonInfo = (seasonId) => {
    const [season, setSeason] = useState([]);
    const [laps, setLaps] = useState([]);
    const [enrolledPlayers, setEnrolledPlayers] = useState([]);
    const [activePlayers, setActivePlayers] = useState([]);

    useEffect(function fetchStorage() {
        const active = JSON.parse(localStorage.getItem('activePlayers'));
        if (active) {
            setActivePlayers(active);
        }
        console.log("active", active);
    }, []);

    async function getSeason() {
        const [seasonResult, lapsResult, enrolledPlayersResult] = await AxeApi.seasonInfo(seasonId);
        setSeason(seasonResult);
        setLaps(lapsResult);
        setEnrolledPlayers(enrolledPlayersResult);
    }

    useEffect(function fetchData() {
        getSeason();
    }, []);

    const setActive = (selectedPlayer) => {
        const inActive = activePlayers.findIndex((player) => player == selectedPlayer);
        if (inActive < 0) {
            setActivePlayers([selectedPlayer, ...activePlayers]);
        }
    }

    const removeActive = (selectedPlayer) => {
        const filteredActive = activePlayers.filter((player) => player !== selectedPlayer);
        setActivePlayers(filteredActive);
    }

    return [season, laps, enrolledPlayers, activePlayers, setEnrolledPlayers, setActive, removeActive];
}

export default useGetSeasonInfo;