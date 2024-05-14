import UserContext from './UserContext';
import React, { useContext } from 'react';
import { Table } from 'reactstrap';
import useGetOverallStats from './hooks/useGetOverallStats.jsx';

/**
 * welcomes guest or user
 * @returns component
 */
const OverallStats = () => {

    const stats = useGetOverallStats();

    if (stats.length !== 0) {
        return (
            <>
                <div className="content">
                    <h1>Overall Stats View</h1>
                    <Table hover>
                        <thead>
                            <tr>
                                <th>
                                    Name
                                </th>
                                <th>
                                    Average
                                </th>
                                <th>
                                    Total Wins
                                </th>
                                <th>
                                    Total Matches
                                </th>
                                <th>
                                    High Score
                                </th>
                                <th>
                                    Low Score
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {stats.map(row => <tr role="button" data={row[0]} key={row[0]}><th scope="row">{row[1]}</th><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>)}
                        </tbody>
                    </Table>
                </div>
            </>
        );
    }


};

export default OverallStats