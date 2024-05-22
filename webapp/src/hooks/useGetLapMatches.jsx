import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetLapMatches = (lap) => {
    const [data, setData] = useState([]);

    async function getLapMatches() {
        const dataResult = await AxeApi.lapMatches(lap);
        setData(dataResult);
    }

    useEffect(function fetchData() {
        if (lap) {
            getLapMatches();
        }
    }, []);

    return data;
}



export default useGetLapMatches;