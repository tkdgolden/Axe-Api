import { Table } from "reactstrap";
import useGetSeason from "./hooks/useGetSeason";

const SeasonStatsTable = (props) => {

    const seasonStats = useGetSeason(props.season_id);
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