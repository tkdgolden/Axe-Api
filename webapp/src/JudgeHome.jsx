import UserContext from './UserContext';
import React, { useContext } from 'react';
import JudgeSeasonOptions from './JudgeSeasonOptions';
import JudgeTournamentOptions from './JudgeTournamentOptions';
import { Container, Row, Col, Button } from 'reactstrap';
import useGetAllTournaments from './hooks/useGetAllTournaments';
import { UncontrolledDropdown, DropdownToggle, DropdownItem, DropdownMenu } from 'reactstrap';
import useGetAllSeasons from './hooks/useGetAllSeasons';
import { useNavigate } from 'react-router-dom';

/**
 * welcomes guest or user
 * @returns component
 */
const JudgeHome = () => {
    const tournaments = useGetAllTournaments();
    const seasons = useGetAllSeasons();
    const navigate = useNavigate();

    const goToSeason = (seasonId) => {
        navigate(`/season/${seasonId}`);
    };

    const goToTournament = (tournamentId) => {
        navigate(`/tournament/${tournamentId}`);
    };

    if (seasons.length !== 0 && tournaments.length !== 0) {
        return (
            <>
                <div className="content judge">
                    <Container>
                        <Row>
                            <Col>
                                <Row>
                                    <Button onClick={() => goToSeason(seasons[0][0])}>
                                        {seasons[0][1]} {seasons[0][2]}
                                    </Button>
                                </Row>
                                <Row>
                                    <Button onClick={() => navigate("/new-season")}>
                                        Begin a New Season
                                    </Button>
                                </Row>
                                <Row>
                                    <UncontrolledDropdown>
                                        Choose an Older Season
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
                                            {seasons.map(season =>
                                                <DropdownItem key={season[0]} onClick={() => goToSeason(season[0])}>
                                                    {season[1]} {season[2]}
                                                </DropdownItem>
                                            )}
                                        </DropdownMenu>
                                    </UncontrolledDropdown>
                                </Row>
                            </Col>
                            <Col xs="1">
                            </Col>
                            <Col>
                                <Row>
                                    <Button onClick={()=> goToTournament[0][0]}>
                                        {tournaments[0][1]} {tournaments[0][2]}
                                    </Button>
                                </Row>
                                <Row>
                                    <Button onClick={() => navigate("/new-tournament")}>
                                        Begin a New Tournament
                                    </Button>
                                </Row>
                                <Row>
                                    <UncontrolledDropdown>
                                        Choose Another Tournament
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
                                            {tournaments.map(tournament =>
                                                <DropdownItem key={tournament[0]} onClick={() => goToTournament(tournament[0])}>
                                                    {tournament[1]} {tournament[2]}
                                                </DropdownItem>
                                            )}
                                        </DropdownMenu>
                                    </UncontrolledDropdown>
                                </Row>
                            </Col>
                        </Row>
                    </Container>
                </div>
            </>
        );
    }
};

export default JudgeHome