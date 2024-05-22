import React, { useState, useEffect } from "react";
import AxeApi from "../Api.jsx";


const useGetAllPlayers = () => {
    const [data, setData] = useState([]);
    
    async function getAllPlayers() {
        const dataResult = await AxeApi.allPlayers();
        setData(dataResult);
    }

    useEffect(function fetchData() {
        getAllPlayers();
    }, []);

    return data;
}



export default useGetAllPlayers;