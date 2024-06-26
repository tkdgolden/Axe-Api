import { Table, CardBody } from "reactstrap";
import { useEffect, useState } from "react";
import AxeApi from "./Api";

const SeasonStatsTable = (props) => {
    const [ seasonStats, setSeasonStats ] = useState([]);

    useEffect(() => {
        async function getSeasonStats() {
            const seasonStatsResult = await AxeApi.getSeason(props.seasonId);
            setSeasonStats(seasonStatsResult);
        }
        getSeasonStats();
    }, [props.seasonId]);

    console.log(seasonStats);


    if (seasonStats.length !== 0) {
        return (
            <>
                <CardBody>
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
                            {seasonStats.map(player => {
                                return (
                                    <tr key={player[0]}>
                                        <th scope="row">
                                            {player[1]}
                                        </th>
                                        <td>
                                            {player[2]}
                                        </td>
                                        <td>
                                            {player[3]}
                                        </td>
                                        <td>
                                            {player[4]}
                                        </td>
                                        <td>
                                            {player[5]}
                                        </td>
                                        <td>
                                            {player[6]}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </Table>
                </CardBody>
            </>
        );
    }
    else {
        return <h2>Loading</h2>;
    }
};

export default SeasonStatsTable