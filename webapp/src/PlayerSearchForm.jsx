import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * controlled form for filtering/ searching companies
 * searches on submit
 * @param {function} searchCompanies alters state in parent and causes a rerender of companies list with the search results
 * @returns component
 */
const PlayerSearchForm = ({ searchPlayers }) => {
    const INITIAL_STATE = "PLAYER STATS";
    const [fData, setFormData] = useState(INITIAL_STATE);
    const navigate = useNavigate();


    const handleChange = evt => {
        const { value } = evt.target;
        setFormData(value);
    };

    const handleSubmit = evt => {
        evt.preventDefault();

        if (searchPlayers(fData)) {
            console.log(fData);
            navigate(`/player-stats/${fData[0]}`);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <i className="tim-icons icon-zoom-split" />
            <input
                id="name"
                type="text"
                value={fData.name}
                onChange={handleChange}
                name="name"
            />
            <button>Search</button>
        </form>
    );
};

export default PlayerSearchForm