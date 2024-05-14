import UserContext from './UserContext';
import React, { useContext, useState } from 'react';
import { Table, UncontrolledDropdown, DropdownToggle, DropdownMenu, NavLink, DropdownItem } from 'reactstrap';
import useGetAllSeasons from './hooks/useGetAllSeasons';
import useGetSeason from './hooks/useGetSeason';
import SeasonStatsTable from './SeasonStatsTable';

/**
 * welcomes guest or user
 * @returns component
 */
const SeasonStats = () => {
    const seasons = useGetAllSeasons();

    if (seasons.length !== 0) {

        return (
            <>
                <div className='content'>
                    <h1>Season Stats View</h1>
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
                            {seasons.map(season => 
                                <DropdownItem key={season[0]}>
                                    {season[1]} {season[2]}
                                </DropdownItem>
                            )}
                        </DropdownMenu>
                    </UncontrolledDropdown>
                    <SeasonStatsTable season_id={1} />
                </div>
            </>
        );
    }
    else {
        return (
            <>
                <div className='content'>
                    <h2>Loading</h2>
                </div>
            </>
        )
    }
};

export default SeasonStats