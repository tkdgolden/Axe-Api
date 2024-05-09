import React, { useContext, useState } from 'react';
import AxeApi from './Api';
import { useNavigate } from 'react-router-dom';
import UserContext from './UserContext';

/**
 * controlled form for submitting username and password to log in
 * @returns component
 */
const RegisterForm = () => {
    const INITIAL_STATE = {name: "", password: ""};
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
        const success = await AxeApi.register(fData);
        if (success === "true") {
            navigate("/");
        }
        else {
            setFormData(INITIAL_STATE);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="name">Username: </label>
            <input
                id="name"
                type="text"
                value={fData.name}
                onChange={handleChange}
                name="name"
            />
            <label htmlFor="password">Password: </label>
            <input
                id="password"
                type="text"
                value={fData.password}
                onChange={handleChange}
                name="password"
            />
            <button>Register</button>
        </form>
    );
};

export default RegisterForm