import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetAllSeasons = () => {
    const [data, setData] = useState([]);
    
    async function getOverallStats() {
        const dataResult = await AxeApi.allSeasons();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getOverallStats();
    }, []);

    return data;
}



export default useGetAllSeasons;