import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetMatch = (matchId) => {
    const [data, setData] = useState([]);
    
    async function getMatch() {
        const dataResult = await AxeApi.getMatch(matchId);
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getMatch();
    }, []);

    return data;
}



export default useGetMatch;