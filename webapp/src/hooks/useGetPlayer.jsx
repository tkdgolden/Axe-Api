import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetPlayerStats = (playerId) => {
    const [data, setData] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const dataResults = await AxeApi.getPlayer(playerId);
            setData(dataResults);
        }
        fetchData();
    }, [playerId]);

    return data;
}



export default useGetPlayerStats;