import React, { useContext, useState } from 'react';
import AxeApi from './Api';
import { useNavigate } from 'react-router-dom';
import UserContext from './UserContext';

/**
 * controlled form for submitting username and password to log in
 * @returns component
 */
const NewSeasonForm = () => {
    const INITIAL_STATE = { season: "", start_date: "" };
    const [fData, setFormData] = useState(INITIAL_STATE);
    const navigate = useNavigate();
    const { user, setUser } = useContext(UserContext);

    const handleChange = evt => {
        const { name, value } = evt.target;
        setFormData(fData => ({
            ...fData,
            [name]: value
        }));
    };

    const handleSubmit = async evt => {
        evt.preventDefault();
        const success = await AxeApi.createSeason(fData);
        if (success === true) {
            navigate("/");
        }
        else {
            setFormData(INITIAL_STATE);
        }
    }

    return (
        <>
            <div className="content">
                <form onSubmit={handleSubmit}>
                    <label htmlFor="season">Season Name: </label>
                    <input
                        id="season"
                        type="text"
                        value={fData.season}
                        onChange={handleChange}
                        name="season"
                    />
                    <label htmlFor="start_date">Start Date: </label>
                    <input
                        id="start_date"
                        type="date"
                        value={fData.date}
                        onChange={handleChange}
                        name="start_date"
                    />
                    <button>Create Season</button>
                </form>
            </div>
        </>
    );
};

export default NewSeasonForm