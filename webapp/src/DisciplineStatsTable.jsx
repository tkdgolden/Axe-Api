import { Table, CardBody } from "reactstrap";
import { useEffect, useState } from "react";
import AxeApi from "./Api";

const DisciplineStatsTable = (props) => {
    const [ disciplineStats, setDisciplineStats ] = useState([]);

    useEffect(() => {
        async function getDisciplineStats() {
            const disciplineStatsResult = await AxeApi.getDiscipline(props.discipline);
            setDisciplineStats(disciplineStatsResult);
        }
        getDisciplineStats();
    }, [props.discipline]);

    console.log(disciplineStats);


    if (disciplineStats.length !== 0) {
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
                            {disciplineStats.map(player => {
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

export default DisciplineStatsTable