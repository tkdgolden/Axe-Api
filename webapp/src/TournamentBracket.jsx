import { DoubleEliminationBracket, Match, MATCH_STATES, SVGViewer } from '@g-loot/react-tournament-brackets';
import dataDoublePlayoffs from './dataDoublePlayoffs';
import useComponentSize from '@rehooks/component-size';
import { useWindowSize } from "@uidotdev/usehooks"


const TournamentBracket = (props) => {
    const size = useComponentSize(props.parentReference);
    const window = useWindowSize();
    console.log(size);
    let width;
    let height;
    const fullScreen = props.fullScreen;
    if (!fullScreen) {
        width = size.width - 310;
        height = size.height - 190;
    }
    else {
        width = window.width;
        height = window.height;
    }

    return (
        <>
            <DoubleEliminationBracket
                matches={dataDoublePlayoffs}
                matchComponent={Match}
                svgWrapper={({ children, ...props }) => (
                    <SVGViewer width={width} height={height} {...props}>
                        {children}
                    </SVGViewer>
                )}
            />
        </>
    );
};

export default TournamentBracket