import React, { useContext, useState } from 'react';
import AxeApi from './Api';
import { useNavigate } from 'react-router-dom';
import UserContext from './UserContext';

/**
 * controlled form for submitting username and password to log in
 * @returns component
 */
const NewTournamentForm = () => {
    const INITIAL_STATE = { name: "", discipline: "hatchet", date: "" };
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
        const success = await AxeApi.createTournament(fData);
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
                    <label htmlFor="name">Tournament Name: </label>
                    <input
                        id="name"
                        type="text"
                        value={fData.name}
                        onChange={handleChange}
                        name="name"
                    />
                    <label htmlFor="discipline">Discipline</label>
                    <select name="discipline" id="discipline" onChange={handleChange}>
                        <option value="hatchet">Hatchet</option>
                        <option value="big axe">Big Axe</option>
                        <option value="knives">Knives</option>
                        {/* <option value="duals">Duals</option> */}
                    </select>
                    <label htmlFor="date">Date: </label>
                    <input
                        id="date"
                        type="date"
                        value={fData.date}
                        onChange={handleChange}
                        name="date"
                    />
                    <button>Create Tournament</button>
                </form>
            </div>
        </>
    );
};

export default NewTournamentForm