import { InputGroup, Input, ButtonGroup, Button } from 'reactstrap';
import { useEffect, useState } from 'react';

const ThrowScore = (props) => {
    const [quickPoint, setQuickPoint] = useState(null);

    const updateScore = (val, getsQuickPoint) => {
        let score = parseInt(val) || 0;
        if (getsQuickPoint) {
            score++;
        }
        return score;
    };
    
    const changeQuickPoint = (evt, whichPlayer) => {
        setQuickPoint(whichPlayer);
        const p1Score = evt.target.parentNode.previousSibling.value;
        const p2Score = evt.target.parentNode.nextSibling.value;
        const p1GetsQuickPoint = whichPlayer === "L";
        const p2GetsQuickPoint = whichPlayer === "R";
        props.setP1(updateScore(p1Score, p1GetsQuickPoint));
        props.setP2(updateScore(p2Score, p2GetsQuickPoint));
    };
    
    const changeP1Score = (val) => {
        props.setP1(updateScore(val, quickPoint === "L"));
    };
    
    const changeP2Score = (val) => {
        props.setP2(updateScore(val, quickPoint === "R"));
    };

    return (
        <>
            <InputGroup>
                <Input type="select" name="p1" onChange={(evt) => {changeP1Score(evt.target.value)}}>
                    <option value="" disabled defaultValue>Score</option>
                    <option value="D">Drop</option>
                    <option value="F">Fault</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="6">6</option>
                    <option value="12">12</option>
                </Input>
                <ButtonGroup>
                    <Button outline onClick={(evt) => changeQuickPoint(evt, "L")} active={quickPoint === "L"}>p1</Button>
                    <Button outline onClick={(evt) => changeQuickPoint(evt, null)} active={quickPoint === null}>No Quickpoint</Button>
                    <Button outline onClick={(evt) => changeQuickPoint(evt, "R")} active={quickPoint === "R"}>p2</Button>
                </ButtonGroup>
                <Input type="select" name="p2" onChange={(evt) => {changeP2Score(evt.target.value)}}>
                    <option value="" disabled defaultValue>Score</option>
                    <option value="D">Drop</option>
                    <option value="F">Fault</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="6">6</option>
                    <option value="12">12</option>
                </Input>
            </InputGroup>
        </>
    )
}

export default ThrowScore