import TournamentBracket from './TournamentBracket';
import { useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, UncontrolledDropdown, DropdownToggle, DropdownMenu, NavLink, DropdownItem, Card, CardHeader, CardTitle, CardBody, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import useGetAllTournaments from './hooks/useGetAllTournaments';
import { useWindowSize } from "@uidotdev/usehooks";



const TournamentStats = () => {
    const ref = useRef(null);
    const tournaments = useGetAllTournaments();
    const params = useParams();
    const navigate = useNavigate();
    let currentTournament;
    const [modal, setModal] = useState(false);

    const toggle = () => setModal(!modal);

    const changeTournament = (tournamentId) => {
        navigate(`/tournament-stats/${tournamentId}`);
    };

    { params.tournamentId ? currentTournament = `${tournaments[params.tournamentId - 1][1]} ${tournaments[params.tournamentId - 1][2]}` : currentTournament = "Choose a Tournament" }

    return (
        <>
            <div className='content' ref={ref}>
                <h1>Tournament Stats View</h1>
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
                        {tournaments.map(tournament =>
                            <DropdownItem key={tournament[0]} onClick={() => changeTournament(tournament[0])}>
                                {tournament[1]} {tournament[2]}
                            </DropdownItem>
                        )}
                    </DropdownMenu>
                </UncontrolledDropdown>
                <Card>
                    <CardHeader>
                        <CardTitle tag="h4">{currentTournament}</CardTitle>
                    </CardHeader>
                    <TournamentBracket parentReference={ref} />
                    <Button color="green" onClick={toggle}>
                        Full Screen
                    </Button>
                </Card>
                <Modal 
                    className="modal-fullscreen"
                    isOpen={modal}
                    toggle={toggle}
                >
                    <ModalHeader toggle={toggle}>{currentTournament}</ModalHeader>
                    <TournamentBracket parentReference={ref} fullScreen={modal} />
                </Modal>
            </div>
        </>
    );
};

export default TournamentStats