import { UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem, Card, CardHeader, CardTitle } from 'reactstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, CardBody } from "reactstrap";
import { useEffect, useState } from "react";
import AxeApi from "./Api";


const PlayerStats = () => {
    const params = useParams();
    let currentPlayer = params.playerId;

    const [playerStats, setPlayerStats] = useState([]);

    useEffect(() => {
        async function getPlayerStats() {
            const playerStatsResult = await AxeApi.getPlayer(currentPlayer);
            setPlayerStats(playerStatsResult[0]);
        }
        getPlayerStats();
    }, [currentPlayer]);

    console.log(playerStats);

    if (playerStats.length !== 0) {
        return (
            <>
                <div className='content'>
                    <Card>
                        <CardHeader>
                            <CardTitle tag="h4">{playerStats[1]} {playerStats[2]}</CardTitle>
                        </CardHeader>
                        <CardBody>
                            <Table hover>
                                <thead>
                                    <tr>
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
                                    <tr key={playerStats[0]}>
                                        <td>
                                            {playerStats[3]}
                                        </td>
                                        <td>
                                            {playerStats[4]}
                                        </td>
                                        <td>
                                            {playerStats[5]}
                                        </td>
                                        <td>
                                            {playerStats[6]}
                                        </td>
                                        <td>
                                            {playerStats[7]}
                                        </td>
                                    </tr>
                                </tbody>
                            </Table>
                        </CardBody>
                    </Card>
                </div>
            </>
        );
    }

};

export default PlayerStats