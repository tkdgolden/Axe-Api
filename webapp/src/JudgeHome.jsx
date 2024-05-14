import UserContext from './UserContext';
import React, { useContext } from 'react';
import JudgeSeasonOptions from './JudgeSeasonOptions';
import JudgeTournamentOptions from './JudgeTournamentOptions';
import { Container, Row, Col } from 'reactstrap';

/**
 * welcomes guest or user
 * @returns component
 */
const JudgeHome = () => {

    return (
        <>
            <div className="content">
                <Container>
                    <Row xs="2">
                        <Col>
                            <JudgeSeasonOptions>

                            </JudgeSeasonOptions>
                        </Col>
                        <Col>
                            <JudgeTournamentOptions>

                            </JudgeTournamentOptions>
                        </Col>
                    </Row>
                </Container>
            </div>
        </>
    );
};

export default JudgeHome