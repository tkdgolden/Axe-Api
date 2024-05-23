import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";

const useGetLapMatches = (lap) => {
    const [data, setData] = useState([]);

    useEffect(() => {
        async function getLapMatches() {
            if (lap) {
                const dataResult = await AxeApi.lapMatches(lap);
                setData(dataResult);
            }
        }
        getLapMatches();
    }, [lap]);

    return data;
}

export default useGetLapMatches;