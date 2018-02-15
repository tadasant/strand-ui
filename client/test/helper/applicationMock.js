import React from 'react';
import {mount} from 'enzyme/build/index';
import App from 'src/App.react';
import {MemoryRouter} from 'react-router';
import {ApolloProvider} from 'react-apollo';
import PropTypes from 'prop-types';


/*
  Mount the entire application (minus stuff in Root.react.js).
 */
export const mountApplication = (endpoint) => {
  return mount(
    <ApolloProvider client={global.__MOCK_APOLLO_CLIENT__}>
      <MemoryRouter initialEntries={[endpoint]} initialIndex={0} keyLength={0}>
        {/*keyLength is 0 so keys aren't generated (they break jest snapshots)*/}
        <App/>
      </MemoryRouter>
    </ApolloProvider>,
    {
      context: {uiHost: 'localhost'},
      childContextTypes: {uiHost: PropTypes.string}
    }
  );
};