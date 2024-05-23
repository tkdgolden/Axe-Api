import { Container, Row, Col, Table, Button } from 'reactstrap';
import { useEffect, useState } from 'react';
import useGenerateRandom from './hooks/useGenerateRandom';
import ThrowScore from './ThrowScore';
import AxeApi from './Api';
import { useNavigate } from 'react-router-dom';

const ScoreMatchTable = (props) => {
    const navigate = useNavigate();
    const [p1Total, setP1Total] = useState(null);
    const [p2Total, setP2Total] = useState(null);
    const [p1t1, setP1t1] = useState(null);
    const [p2t1, setP2t1] = useState(null);
    const [p1t2, setP1t2] = useState(null);
    const [p2t2, setP2t2] = useState(null);
    const [p1t3, setP1t3] = useState(null);
    const [p2t3, setP2t3] = useState(null);
    const [p1t4, setP1t4] = useState(null);
    const [p2t4, setP2t4] = useState(null);
    const [p1t5, setP1t5] = useState(null);
    const [p2t5, setP2t5] = useState(null);
    const [p1t6, setP1t6] = useState(null);
    const [p2t6, setP2t6] = useState(null);
    const [p1t7, setP1t7] = useState(null);
    const [p2t7, setP2t7] = useState(null);
    const [p1t8, setP1t8] = useState(null);
    const [p2t8, setP2t8] = useState(null);
    const sequence = useGenerateRandom();

    const revealTarget = (evt) => {
        console.log(evt);
        evt.target.nextElementSibling.removeAttribute("hidden");
        evt.target.setAttribute("hidden", "");
        console.log(evt.target.parentNode.nextElementSibling);
        evt.target.parentNode.nextElementSibling.removeAttribute("hidden");
    };

    useEffect(function updateTotal() {
        setP1Total(p1t1 + p1t2 + p1t3 + p1t4 + p1t5 + p1t6 + p1t7 + p1t8);
        setP2Total(p2t1 + p2t2 + p2t3 + p2t4 + p2t5 + p2t6 + p2t7 + p2t8);
    }, [p1t1, p2t1, p1t2, p2t2, p1t3, p2t3, p1t4, p2t4, p1t5, p2t5, p1t6, p2t6, p1t7, p2t7, p1t8, p2t8]);

    useEffect(() => {
        if (p1t1 !== null && p2t1 !== null) {
            document.getElementById("t2").removeAttribute("hidden", "");
        }
    }, [p1t1, p2t1]);

    useEffect(() => {
        if (p1t2 !== null && p2t2 !== null) {
            document.getElementById("t3").removeAttribute("hidden", "");
        }
    }, [p1t2, p2t2]);

    useEffect(() => {
        if (p1t3 !== null && p2t3 !== null) {
            document.getElementById("t4").removeAttribute("hidden", "");
        }
    }, [p1t3, p2t3]);

    useEffect(() => {
        if (p1t4 !== null && p2t4 !== null) {
            document.getElementById("t5").removeAttribute("hidden", "");
        }
    }, [p1t4, p2t4]);

    useEffect(() => {
        if (p1t5 !== null && p2t5 !== null) {
            document.getElementById("t6").removeAttribute("hidden", "");
        }
    }, [p1t5, p2t5]);

    useEffect(() => {
        if (p1t6 !== null && p2t6 !== null) {
            document.getElementById("t7").removeAttribute("hidden", "");
        }
    }, [p1t6, p2t6]);

    useEffect(() => {
        if (p1t7 !== null && p2t7 !== null) {
            document.getElementById("t8").removeAttribute("hidden", "");
        }
    }, [p1t7, p2t7]);

    useEffect(() => {
        if (p1t8 !== null && p2t8 !== null) {
            document.getElementById("submit").removeAttribute("hidden", "");
        }
    }, [p1t8, p2t8]);

    const handleSubmit = async (evt) => {
        evt.preventDefault();
        let winner = null;
        /* FURTHER STUDY handle ties */
        if (p1Total > p2Total) {
            winner = props.matchInfo[0];
        }
        else if (p2Total > p2Total) {
            winner = props.matchInfo[1];
        }
        const data = {
            p1: {
                competitor_id: props.matchInfo[0],
                match_id: props.matchId,
                /* FURTHER STUDY save quickpoints */
                quick_points: 0,
                sequence: sequence,
                throw1: p1t1,
                throw2: p1t2,
                throw3: p1t3,
                throw4: p1t4,
                throw5: p1t5,
                throw6: p1t6,
                throw7: p1t7,
                throw8: p1t8,
                total: p1Total,
                /* FURTHER STUDY handle ties */
                win: p1Total > p2Total
            },
            p2: {
                competitor_id: props.matchInfo[1],
                match_id: props.matchId,
                /* FURTHER STUDY save quickpoints */
                quick_points: 0,
                sequence: sequence,
                throw1: p2t1,
                throw2: p2t2,
                throw3: p2t3,
                throw4: p2t4,
                throw5: p2t5,
                throw6: p2t6,
                throw7: p2t7,
                throw8: p2t8,
                total: p2Total,
                /* FURTHER STUDY handle ties */
                win: p2Total > p1Total
            },
            match: {
                winner_id: winner,
                judge_id: localStorage.user,
                player_1_total: p1Total,
                player_2_total: p2Total
            }
        }
        const res = await AxeApi.submitMatch(data);
        console.log(res);
        navigate(-1);
    }

    if (props.matchInfo) {
        return (
            <>
                <Container>
                    <Row>
                        <Col></Col>
                        <Col><h4>{props.matchInfo[0]}</h4></Col>
                        <Col><h4>{p1Total} :: {p2Total}</h4></Col>
                        <Col><h4>{props.matchInfo[1]}</h4></Col>
                    </Row>
                    <Row>
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 1</Button>{sequence[0]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t1} p2={p2t1} setP1={setP1t1} setP2={setP2t1} /></Col>
                    </Row>
                    <Row hidden id="t2">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 2</Button>{sequence[1]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t2} p2={p2t2} setP1={setP1t2} setP2={setP2t2} /></Col>
                    </Row>
                    <Row hidden id="t3">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 3</Button>{sequence[2]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t3} p2={p2t3} setP1={setP1t3} setP2={setP2t3} /></Col>
                    </Row>
                    <Row hidden id="t4">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 4</Button>{sequence[3]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t4} p2={p2t4} setP1={setP1t4} setP2={setP2t4} /></Col>
                    </Row>
                    <Row hidden id="t5">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 5</Button>{sequence[4]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t5} p2={p2t5} setP1={setP1t5} setP2={setP2t5} /></Col>
                    </Row>
                    <Row hidden id="t6">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 6</Button>{sequence[5]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t6} p2={p2t6} setP1={setP1t6} setP2={setP2t6} /></Col>
                    </Row>
                    <Row hidden id="t7">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 7</Button>{sequence[6]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t7} p2={p2t7} setP1={setP1t7} setP2={setP2t7} /></Col>
                    </Row>
                    <Row hidden id="t8">
                        <Col><Button onClick={(evt) => {revealTarget(evt)}}>Throw 8</Button>{sequence[7]}</Col>
                        <Col hidden xs="10"><ThrowScore p1={p1t8} p2={p2t8} setP1={setP1t8} setP2={setP2t8} /></Col>
                    </Row>
                    <Row>
                        <Button hidden id="submit" onClick={(evt) => handleSubmit(evt)}>
                            Submit Match
                        </Button>
                    </Row>
                </Container>
            </>
        );
    }
    else {
        console.log("here");
    }
}

export default ScoreMatchTable