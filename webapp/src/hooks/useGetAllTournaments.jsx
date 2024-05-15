import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetAllTournaments = () => {
    const [data, setData] = useState([]);
    
    async function getOverallStats() {
        const dataResult = await AxeApi.allTournaments();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getOverallStats();
    }, []);

    return data;
}



export default useGetAllTournaments;