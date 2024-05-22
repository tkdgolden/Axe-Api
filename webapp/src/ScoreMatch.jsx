import { useParams } from 'react-router-dom';
import useGetMatch from './hooks/useGetMatch';
import ScoreMatchTable from './ScoreMatchTable';

const ScoreMatch = () => {
    const params = useParams();
    const matchId = params.matchId;
    const matchInfo = useGetMatch(matchId ? matchId : null);
    console.log(matchInfo);

    return (
        <>
            <div className="content judge">
                <ScoreMatchTable matchInfo={matchInfo} />
            </div>
        </>
    )

}

export default ScoreMatch