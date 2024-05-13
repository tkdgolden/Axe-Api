import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";

/**
 * at the first page render, loads company data by API function
 * @returns company data, function to set company data, function for doing a search of company data
 */
const useGetOverallStats = () => {
    const [data, setData] = useState([]);
    
    async function getOverallStats() {
        const dataResult = await AxeApi.overall_stats();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getOverallStats();
    }, []);

    return [data, setData]
}



export default useGetOverallStats;