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
  },
  'secondary': {
    '50': '#fcfcfc',
    '100': '#f8f8f8',
    '200': '#f3f4f4',
    '300': '#eeeff0',
    '400': '#eaebec',
    '500': '#e6e8e9',
    '600': '#e3e5e6',
    '700': '#dfe2e3',
    '800': '#dbdedf',
    '900': '#d5d8d9',
    'A100': '#ffffff',
    'A200': '#ffffff',
    'A400': '#ffffff',
    'A700': '#ffffff',
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
