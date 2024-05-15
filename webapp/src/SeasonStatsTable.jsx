import { Table } from "reactstrap";
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
                        {seasonStats.map(match => {
                            return (
                                <tr key={match[0]}>
                                    <th scope="row">
                                        {match[1]}
                                    </th>
                                    <td>
                                        {match[2]}
                                    </td>
                                    <td>
                                        {match[3]}
                                    </td>
                                    <td>
                                        {match[4]}
                                    </td>
                                    <td>
                                        {match[5]}
                                    </td>
                                    <td>
                                        {match[6]}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </Table>
            </>
        );
    }
    else {
        return <h2>Loading</h2>;
    }
};

export default SeasonStatsTable