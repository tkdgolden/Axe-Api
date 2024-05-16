import React, { useState } from "react";

/**
 * controlled form for filtering/ searching companies
 * searches on submit
 * @param {function} searchCompanies alters state in parent and causes a rerender of companies list with the search results
 * @returns component
 */
const PlayerSearchForm = ({ searchPlayers }) => {
    const INITIAL_STATE = "PLAYER STATS";
    const [fData, setFormData] = useState(INITIAL_STATE);


    const handleChange = evt => {
        const { value } = evt.target;
        setFormData(value);
    };

    const handleSubmit = evt => {
        evt.preventDefault();

        searchPlayers(fData);
        setFormData(INITIAL_STATE);
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