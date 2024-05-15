import UserContext from './UserContext';
import React, { useContext, useState } from 'react';
import { Table, UncontrolledDropdown, DropdownToggle, DropdownMenu, NavLink, DropdownItem, Card, CardHeader, CardTitle, CardBody } from 'reactstrap';
import DisciplineStatsTable from './DisciplineStatsTable';
import { Navigate, useParams, useNavigate } from 'react-router-dom';

const DisciplineStats = () => {
    const params = useParams();
    const navigate = useNavigate();
    let currentDiscipline;

    const changeDiscipline = (discipline) => {
        navigate(`/discipline-stats/${discipline}`);
    };

    {params.discipline ? currentDiscipline = `${params.discipline}` : currentDiscipline = "Choose a Discipline"}

        return (
            <>
                <div className='content'>
                    <h1>Discipline Stats View</h1>
                    <div>
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
                                <DropdownItem onClick={() => changeDiscipline('knives')}>
                                    Knives
                                </DropdownItem>
                                <DropdownItem onClick={() => changeDiscipline('big axe')}>
                                    Big Axe
                                </DropdownItem>
                                <DropdownItem onClick={() => changeDiscipline('duals')}>
                                    Duals
                                </DropdownItem>
                            </DropdownMenu>
                        </UncontrolledDropdown>
                    </div>
                    <Card>
                        <CardHeader>
                            <CardTitle tag="h4">{currentDiscipline}</CardTitle>
                        </CardHeader>
                        <DisciplineStatsTable discipline={params.discipline || 'knives'}/>
                    </Card>
                </div>
            </>
        );
};

export default DisciplineStats