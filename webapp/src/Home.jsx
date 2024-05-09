import UserContext from './UserContext';
import React, { useContext } from 'react';

/**
 * welcomes guest or user
 * @returns component
 */
const Home = () => {
    const { user, setUser } = useContext(UserContext);

    if (user) {
        return (
            <>
                <h1>Judge Homepage</h1>
                <p>Options to create, edit, score...</p>
            </>
        );
    }
    return (
        <>
            <h1>Player Homepage</h1>
            <p>Lots of different ways to view stats...</p>
        </>
    );
};

export default Home