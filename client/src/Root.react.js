import React, {Component} from 'react';
import createMuiTheme from 'material-ui/styles/createMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import BrowserRouter from 'react-router-dom/BrowserRouter';
import App from './App.react';
import 'typeface-roboto'
import 'typeface-rajdhani'
import 'typeface-montserrat'

export const themePallete = {
  'primary': {
    '50': '#e6e8e9',
    '100': '#c2c6c9',
    '200': '#99a1a5',
    '300': '#707b80',
    '400': '#515e65',
    '500': '#32424a',
    '600': '#2d3c43',
    '700': '#26333a',
    '800': '#1f2b32',
    '900': '#131d22',
    'A100': '#66ccff',
    'A200': '#33bbff',
    'A400': '#00aaff',
    'A700': '#0099e6',
    'contrastDefaultColor': 'light',
    'contrastDarkColors': [
      '50',
      '100',
      '200',
      'A100',
      'A200',
      'A400',
    ],
    'contrastLightColors': [
      '300',
      '400',
      '500',
      '600',
      '700',
      '800',
      '900',
      'A700',
    ],
  },
  'secondary': {
    '50': '#f5ebe6',
    '100': '#e6cec0',
    '200': '#d5ae96',
    '300': '#c48d6c',
    '400': '#b7744d',
    '500': '#aa5c2d',
    '600': '#a35428',
    '700': '#994a22',
    '800': '#90411c',
    '900': '#7f3011',
    'A100': '#ffc5b3',
    'A200': '#ff9f80',
    'A400': '#ff784d',
    'A700': '#ff6533',
    'contrastDefaultColor': 'light',
    'contrastDarkColors': [
      '50',
      '100',
      '200',
      '300',
      '400',
      'A100',
      'A200',
      'A400',
      'A700',
    ],
    'contrastLightColors': [
      '500',
      '600',
      '700',
      '800',
      '900',
    ],
  },
};

const codeClippyTheme = createMuiTheme({
  typography: {
    fontFamily: 'Montserrat',
    // for some headers, use '\'Rajdhani\', sans-serif',
  },
  'palette': themePallete,
});

class Root extends Component {
  render() {
    return (
      <MuiThemeProvider theme={codeClippyTheme}>
        <BrowserRouter>
          <App/>
        </BrowserRouter>
      </MuiThemeProvider>
    )
  }
}

export default Root;
