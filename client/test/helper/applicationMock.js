import PropTypes from 'prop-types';
import React from 'react';
import {mount} from 'enzyme/build/index';
import App from 'src/App.react';
import {MemoryRouter} from 'react-router';
import {navigationLabelToPath} from 'src/shell/common/MenuConstants';


/*
  Mount the entire application (minus stuff in Root.react.js).
 */
export const mountApplication = (endpoint) => {
  const routingEntries = Object.keys(navigationLabelToPath).map(k => ({pathname: navigationLabelToPath[k], key: k}));
  return mount(
    <MemoryRouter initialEntries={[endpoint]} initialIndex={0} keyLength={0}>
      <App/>
    </MemoryRouter>,
    {
      context: {uiHost: 'localhost'},
      childContextTypes: {uiHost: PropTypes.string}
    }
  );
};