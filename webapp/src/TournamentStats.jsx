import { DoubleEliminationBracket, Match, MATCH_STATES, SVGViewer } from '@g-loot/react-tournament-brackets';
import dataDoublePlayoffs from './dataDoublePlayoffs';
import useComponentSize from '@rehooks/component-size';
import { useRef, useState } from 'react';

/**
 * welcomes guest or user
 * @returns component
 */
const TournamentStats = () => {
    const ref = useRef(null);
    const size = useComponentSize(ref);
    console.log(size);
    const width = size.width;
    const height = size.height;
    const [fullScreen, setFullScreen] = useState(false);
    console.log(fullScreen);

    return (
        <>
            <div className='content' ref={ref}>
                <h1>Tournament Stats View</h1>
                <div>
                    <button onClick={() => setFullScreen(!fullScreen)}>Toggle Full Screen</button>
                    <div>
                        <DoubleEliminationBracket
                            matches={dataDoublePlayoffs}
                            matchComponent={Match}
                            svgWrapper={({ children, ...props }) => (
                                <SVGViewer width={width - 300} height={height - 100} {...props}>
                                    {children}
                                </SVGViewer>
                            )}
                        />
                    </div>
                </div>
            </div>
        </>
    );
};

export default TournamentStats