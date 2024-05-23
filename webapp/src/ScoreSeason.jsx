import { useParams } from 'react-router-dom';
import { act, useEffect, useState } from 'react';
import { Button, Table, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem, Row, Col } from 'reactstrap';
import useGetSeasonInfo from './hooks/useGetSeasonInfo';
import AddPlayerForm from './AddPlayerForm';
import useGetAllPlayers from './hooks/useGetAllPlayers';
import AxeApi from './Api';
import ScoreSeasonTable from './ScoreSeasonTable';
import useGetLapMatches from './hooks/useGetLapMatches';

const ScoreSeason = () => {
    const params = useParams();
    const [currentLap, setCurrentLap] = useState();
    const [hasCurrentLap, setHasCurrentLap] = useState(false);
    const [season, laps, enrolledPlayers, activePlayers, setEnrolledPlayers, setActive, removeActive] = useGetSeasonInfo(params.seasonId);
    const allPlayers = useGetAllPlayers();
    let unenrolledPlayers = [];
    allPlayers.forEach((player) => {
        let found = false;
        enrolledPlayers.forEach((enrolledPlayer) => {
            if (player[0] === enrolledPlayer[0]) {
                found = true;
            }
        });
        if (!found) {
            unenrolledPlayers.push(player);
        }
    });

    useEffect(() => {
        const oldSeason = JSON.parse(localStorage.getItem('currentSeasonId'));
        console.log("old", oldSeason);
        console.log(oldSeason !== params.seasonId)
        if (oldSeason !== params.seasonId) {
            console.log("HERE")
            console.log(localStorage);
            localStorage.removeItem('currentLap');
            localStorage.setItem('activePlayers', JSON.stringify([]));
            localStorage.removeItem('currentSeasonId');
            console.log(localStorage);
        }
        localStorage.setItem('currentSeasonId', JSON.stringify(params.seasonId));
        console.log(localStorage);
    }, [])


    useEffect(() => {
        const currentLap = JSON.parse(localStorage.getItem('currentLap'));
        if (currentLap) {
            setCurrentLap(currentLap);
            setHasCurrentLap(true);
        } else {
            setCurrentLap(laps[0]);
        }
    }, [laps]);

    const matches = useGetLapMatches(currentLap && currentLap[0]);
    console.log("matches", matches);

    useEffect(() => {
        if (activePlayers.length > 0) {
            localStorage.setItem('activePlayers', JSON.stringify(activePlayers));
        }
    }, [activePlayers]);

    useEffect(() => {
        if (currentLap) {
            localStorage.setItem('currentLap', JSON.stringify(currentLap));
        }
    }, [currentLap]);


    useEffect(function fetchStorage() {
        const currentLap = JSON.parse(localStorage.getItem('currentLap'));
        if (currentLap) {
            setCurrentLap(currentLap);
        }
        else {
            setCurrentLap(laps[0]);
        }
        console.log("current", currentLap);
    }, []);

    const enrollPlayer = async (player) => {
        const res = await AxeApi.enrollPlayer(player[0], parseInt(params.seasonId), null);
        setEnrolledPlayers([player, ...enrolledPlayers]);
    }

    const newLap = async () => {
        const res = await AxeApi.newLap(params.seasonId);
        console.log(res);
        setCurrentLap(res);
    }

    if (activePlayers !== undefined && season != undefined) {
        return (
            <>
                <div className='content judge'>
                    <h1>{season[0]} {season[1]}</h1>
                    <Row>
                        <Col>
                            <h4>Check In Players</h4>
                            <UncontrolledDropdown>
                                <DropdownToggle
                                    caret
                                    className="btn-icon"
                                    color="link"
                                    data-toggle="dropdown"
                                    type="button"
                                >
                                    <i className="tim-icons icon-bullet-list-67" />
                                </DropdownToggle>
                                <DropdownMenu aria-labelledby="dropdownMenuLink">
                                    {enrolledPlayers.map((player) =>
                                        <li key={player[0]} onClick={() => { setActive(player) }}>
                                            {player[1]} {player[2]}
                                        </li>
                                    )}
                                </DropdownMenu>
                            </UncontrolledDropdown>
                        </Col>
                        <Col>
                            <h4>Enroll Existing Player</h4>
                            <UncontrolledDropdown>
                                <DropdownToggle
                                    caret
                                    className="btn-icon"
                                    color="link"
                                    data-toggle="dropdown"
                                    type="button"
                                >
                                    <i className="tim-icons icon-bullet-list-67" />
                                </DropdownToggle>
                                <DropdownMenu aria-labelledby="dropdownMenuLink">
                                    {unenrolledPlayers.map((player) =>
                                        <li key={player[0]} onClick={() => { enrollPlayer(player) }}>
                                            {player[1]} {player[2]}
                                        </li>
                                    )}
                                </DropdownMenu>
                            </UncontrolledDropdown>
                        </Col>
                        <Col>
                            <AddPlayerForm seasonId={params.seasonId} />
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <h4>Score Existing Lap</h4>
                            <UncontrolledDropdown>
                                <DropdownToggle
                                    caret
                                    className="btn-icon"
                                    color="link"
                                    data-toggle="dropdown"
                                    type="button"
                                >
                                    <i className="tim-icons icon-bullet-list-67" />
                                </DropdownToggle>
                                <DropdownMenu aria-labelledby="dropdownMenuLink">
                                    {laps.map((lap) =>
                                        <li key={lap[0]} onClick={() => { setCurrentLap(lap) }}>
                                            {lap[1]} {lap[2]} {lap[3]}
                                        </li>
                                    )}
                                </DropdownMenu>
                            </UncontrolledDropdown>
                        </Col>
                        <Col>
                            <h4 onClick={() => newLap()}>Start a New Lap</h4>
                        </Col>
                    </Row>
                    <Row>
                        <ScoreSeasonTable activePlayers={activePlayers} lap={currentLap} removeActive={removeActive} matches={matches} />
                    </Row>
                </div>
            </>
        )
    }
}

export default ScoreSeason