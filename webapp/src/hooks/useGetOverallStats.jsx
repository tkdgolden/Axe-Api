import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetOverallStats = () => {
    const [data, setData] = useState([]);
    
    async function getOverallStats() {
        console.log("inner function");
        const dataResult = await AxeApi.overallStats();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        console.log("callback");
        getOverallStats();
    }, []);

    return data;
}



export default useGetOverallStats;