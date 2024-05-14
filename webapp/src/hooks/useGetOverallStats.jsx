import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetOverallStats = () => {
    const [data, setData] = useState([]);
    
    async function getOverallStats() {
        const dataResult = await AxeApi.overallStats();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getOverallStats();
    }, []);

    return data;
}



export default useGetOverallStats;