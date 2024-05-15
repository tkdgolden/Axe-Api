import { createTheme } from '@g-loot/react-tournament-brackets';

const GlootTheme = createTheme({
  textColor: { main: '#000000', highlighted: '#ffffff', dark: '#707582' },
  matchBackground: { wonColor: '#2D2D59', lostColor: '#1B1D2D' },
  score: {
    background: {
      wonColor: `#1B1D2D`,
      lostColor: '#10131C',
    },
    text: { highlightedWonColor: '#00f2c3', highlightedLostColor: '#fd5d93' },
  },
  border: {
    color: '#292B43',
    highlightedColor: '#1d8cf8',
  },
  roundHeaders: { background: 'rgb(39, 41, 61)', fontColor: '#707582' },
  connectorColor: '#292B43',
  connectorColorHighlight: '#1d8cf8',
  svgBackground: '#0F121C',
});

export default GlootTheme;