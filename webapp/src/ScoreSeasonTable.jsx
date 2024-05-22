import { Table } from 'reactstrap';
import useGetLapMatches from './hooks/useGetLapMatches';
import { useNavigate } from 'react-router-dom';
import AxeApi from './Api';

const ScoreSeasonTable = (props) => {
    const navigate = useNavigate();
    console.log("lap", props.lap);
    const matches = useGetLapMatches(props.lap ? props.lap[0] : null);

    const findMatches = (p1, p2) => {
        const index = matches.findIndex((match) =>
            ((match[1] == p1) && (match[2] == p2))
            ||
            ((match[2] == p1) && (match[1] == p2)));
        if (index >= 0) {
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

    const checkBeginMatch = async (p1, p2) => {
        const index = matches.findIndex((match) =>
            ((match[1] == p1) && (match[2] == p2))
            ||
            ((match[2] == p1) && (match[1] == p2)));
        if (index === 0) {
            return false;
        }
        else {
            const newMatchId = await AxeApi.newMatch(p1, p2, props.lap[0]);
            console.log(newMatchId);
            navigate(`/score-match/${newMatchId[0]}`);
        }
    };


    if (props.lap) {
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
                                    <td key={playerV[0]} className={findMatches(playerH[0], playerV[0])} onClick={() => checkBeginMatch(playerH[0], playerV[0])}></td>
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