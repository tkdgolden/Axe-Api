import { Table } from 'reactstrap';
import useGetLapMatches from './hooks/useGetLapMatches';

const ScoreSeasonTable = (props) => {
    if (props.lap) {
        console.log("lap", props.lap);
        console.log(props.lap[0]);
        const matches = useGetLapMatches(props.lap[0]);

        const findMatches = (p1, p2) => {
            const index = matches.findIndex((match) =>
                ((match[1] == p1) && (match[2] == p2))
                ||
                ((match[2] == p1) && (match[1] == p2)));
            if (index === 0) {
                return "completed";
            }
            else if (p1 === p2) {
                return "double";
            }
            else {
                return "waiting";
            }
        };

        const removeActivePlayer = (player) => {
            props.removeActive(player);
        };


        return (
            <>
                <Table>
                    <thead>
                        <tr>
                            <th>{props.lap[1]} {props.lap[2]} {props.lap[3]}</th>
                            {props.activePlayers.map((playerV) =>
                                <th key={playerV[0]} onClick={() => removeActivePlayer(playerV)}>
                                    {playerV[1]} {playerV[2]}
                                </th>
                            )}
                        </tr>
                    </thead>
                    <tbody>
                        {props.activePlayers.map((playerH) =>
                            <tr key={playerH[0]}>
                                <th scope="row" onClick={() => removeActivePlayer(playerH)}>{playerH[1]} {playerH[2]}</th>
                                {props.activePlayers.map((playerV) =>
                                    <td key={playerV[0]} className={findMatches(playerH[0], playerV[0])}></td>
                                )}
                            </tr>
                        )}
                    </tbody>
                </Table>
            </>
        );
    }

}

export default ScoreSeasonTable