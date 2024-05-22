import React, { useContext, useState } from 'react';
import AxeApi from './Api';
import UserContext from './UserContext';

/**
 * controlled form for submitting username and password to log in
 * @returns component
 */
const AddPlayerForm = (props) => {
    const INITIAL_STATE = { first_name: "", last_name: "" };
    const [fData, setFormData] = useState(INITIAL_STATE);

    const handleChange = evt => {
        const { name, value } = evt.target;
        setFormData(fData => ({
            ...fData,
            [name]: value
        }));
    };

    const handleSubmit = async evt => {
        evt.preventDefault();
        const newId = await AxeApi.createPlayer(fData);
        console.log("id", newId);
        setFormData(INITIAL_STATE);
    }

    return (
        <>
            <div className="content">
                <form onSubmit={handleSubmit}>
                    <label htmlFor="first_name">Player First Name: </label>
                    <input
                        id="first_name"
                        type="text"
                        value={fData.first_name}
                        onChange={handleChange}
                        name="first_name"
                    />
                    <label htmlFor="last_name">Player Last Name: </label>
                    <input
                        id="last_name"
                        type="text"
                        value={fData.last_name}
                        onChange={handleChange}
                        name="last_name"
                    />
                    <button>Create Player</button>
                </form>
            </div>
        </>
    );
};

export default AddPlayerForm