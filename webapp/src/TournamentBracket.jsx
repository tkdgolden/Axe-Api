import { DoubleEliminationBracket, Match, MATCH_STATES, SVGViewer } from '@g-loot/react-tournament-brackets';
import dataDoublePlayoffs from './dataDoublePlayoffs';
import useComponentSize from '@rehooks/component-size';
import { useWindowSize } from "@uidotdev/usehooks";
import GlootTheme from './GlootTheme';


const TournamentBracket = (props) => {
    const size = useComponentSize(props.parentReference);
    const window = useWindowSize();
    let width;
    let height;
    const fullScreen = props.fullScreen;
    if (!fullScreen) {
        width = size.width - 310;
        height = size.height - 190;
    }
    else {
        width = window.width;
        height = window.height - 40;
    }

    return (
        <>
            <DoubleEliminationBracket
                matches={dataDoublePlayoffs}
                matchComponent={Match}
                theme={GlootTheme}
                options={{
                    style: {
                      roundHeader: {
                        backgroundColor: GlootTheme.roundHeaders.background,
                        fontColor: GlootTheme.roundHeaders.fontColor,
                      },
                      connectorColor: GlootTheme.connectorColor,
                      connectorColorHighlight: GlootTheme.connectorColorHighlight,
                    },
                  }}
                svgWrapper={({ children, ...props }) => (
                    <SVGViewer
                        width={width}
                        height={height} {...props}
                        background={GlootTheme.svgBackground}
                        SVGBackground={GlootTheme.svgBackground}
                    >
                        {children}
                    </SVGViewer>
                )}
            />
        </>
    );
};

export default TournamentBracket