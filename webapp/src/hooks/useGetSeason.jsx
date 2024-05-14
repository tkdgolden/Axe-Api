import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetSeason = (season_id) => {
    const [data, setData] = useState([]);
    
    async function getSeasons() {
        const dataResult = await AxeApi.getSeason(season_id);
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getSeasons();
    }, []);

    return data;
}



export default useGetSeason;