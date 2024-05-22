import { useState, useEffect } from 'react';

const useGenerateRandom = () => {
    const [sequence, setSequence] = useState([]);

    const generateRandom = () => {
        var tempSequence = [];
        const options = [<span hidden style={{color: 'red'}}>RED (Top Left)</span>, <span hidden style={{color: 'green'}}>GREEN (Top Right)</span>, <span hidden style={{color: 'blue'}}>BLUE (Bottom Left)</span>, <span hidden style={{color: 'orange'}}>ORANGE (Bottom Right)</span>];

        let usedNumbers = [];
        for (let i = 0; i < 4; i++) {
            do {
                randomNumber = Math.floor(Math.random() * 4);
            }
            while (usedNumbers.includes(randomNumber));
            usedNumbers.push(randomNumber);
        }
        tempSequence = [options[usedNumbers[0]], options[usedNumbers[1]], options[usedNumbers[2]], options[usedNumbers[3]]];
        usedNumbers = [];
        for (var i = 0; i < 4; i++) {
            do {
                var randomNumber = Math.floor(Math.random() * 4);
            } while (usedNumbers.includes(randomNumber));
            usedNumbers.push(randomNumber);
        }
        tempSequence.push(options[usedNumbers[0]], options[usedNumbers[1]], options[usedNumbers[2]], options[usedNumbers[3]]);
        setSequence(tempSequence);
    }

    useEffect(function makeSequence() {
        generateRandom();
    }, []);

    return sequence;
}

export default useGenerateRandom