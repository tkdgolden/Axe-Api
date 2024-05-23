import { Table } from 'reactstrap';
import { useNavigate } from 'react-router-dom';
import AxeApi from './Api';

/* FURTHER STUDY:
    reduce table so that each matchup only appears once,
    so instead of looking like this:
    X000
    0X00
    00X0
    000X
    it would look like this:
    X000
    XX00
    XXX0
    in "waiting" squares, display the sum of the "time since last match" from each player in that matchup, 
    for quickly identifying the ideal next match based on player's wait times */

const ScoreSeasonTable = (props) => {
    const navigate = useNavigate();

    if (!props.lap || !props.activePlayers) {
        return null;
    }

    console.log("lap", props.lap);
    console.log("activePlayers", props.activePlayers);
    console.log("matches", props.matches);

    const findMatches = (p1, p2) => {
        const index = props.matches.findIndex((match) =>
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
        const index = props.matches.findIndex((match) =>
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


export default ScoreSeasonTable