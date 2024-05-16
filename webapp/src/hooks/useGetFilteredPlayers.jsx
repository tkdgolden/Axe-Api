import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetFilteredPlayers = () => {
    const [data, setData] = useState([]);

    async function getFilteredPlayers(playerName) {
        const dataResult = await AxeApi.searchPlayers(playerName);
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getFilteredPlayers();
    }, []);

    return [data, setData, getFilteredPlayers];
};



export default useGetFilteredPlayers;