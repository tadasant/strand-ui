import * as React from 'react';
import {Component} from 'react';
import createMuiTheme from 'material-ui/styles/createMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {BrowserRouter} from 'react-router-dom';
import App from './App';
import {hot} from 'react-hot-loader';
import {STRAND_API_HOST, STRAND_SLACK_HOST} from './config';
import StrandSlackClient from './clients/StrandSlackClient';
import StrandApiClient from './clients/StrandApiClient';
import TestStrandSlackClient from '../test/clients/TestStrandSlackClient';
import TestStrandApiClient from '../test/clients/TestStrandApiClient';

// Use http://mcg.mbitson.com/ to generate a palette
// 2/21/18: http://mcg.mbitson.com/#!?strand1=%23e8ebe4&strand2=%2348466d&strand3=%23190b28&strand4=%237ca982&strand5=%23f1e9da&themename=Strand
export const themePalette = {
  // strand1
  'primary': {
    50: '#fcfdfc',
    100: '#f8f9f7',
    200: '#f4f5f2',
    300: '#eff1ec',
    400: '#ebeee8',
    500: '#e8ebe4',
    600: '#e5e9e1',
    700: '#e2e5dd',
    800: '#dee2d9',
    900: '#d8ddd1',
    A100: '#ffffff',
    A200: '#ffffff',
    A400: '#ffffff',
    A700: '#ffffff',
    'contrastDefaultColor': 'dark',
  },
  // strand2
  'secondary': {
    50: '#e9e9ed',
    100: '#c8c8d3',
    200: '#a4a3b6',
    300: '#7f7e99',
    400: '#636283',
    500: '#48466d',
    600: '#413f65',
    700: '#38375a',
    800: '#302f50',
    900: '#21203e',
    A100: '#8884ff',
    A200: '#5751ff',
    A400: '#261eff',
    A700: '#0e04ff',
    'contrastDefaultColor': 'light',
  },
};

const strandTheme = createMuiTheme({
  typography: {
    fontFamily: 'Montserrat',
    // for some headers, use '\'Rajdhani\', sans-serif',
  },
  'palette': themePalette,
});

interface PropTypes {
}

// TODO [UI-59] replace with React 16.3 new context API
// Would put the types in index.d.ts but seems to interfere with module declarations??
declare global {
  namespace NodeJS {
    interface Global {
      strandSlackClient: StrandSlackClient | TestStrandSlackClient
      strandApiClient: StrandApiClient | TestStrandApiClient
    }
  }
}
global.strandSlackClient = new StrandSlackClient(STRAND_SLACK_HOST);
global.strandApiClient = new StrandApiClient(STRAND_API_HOST);

class Root extends Component<PropTypes> {
  render() {
    return (
      <MuiThemeProvider theme={strandTheme}>
        <BrowserRouter>
          <App/>
        </BrowserRouter>
      </MuiThemeProvider>
    )
  }
}

export default hot(module)(Root);
