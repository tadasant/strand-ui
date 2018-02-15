import React from 'react';
import {mount} from 'enzyme/build/index';
import App from 'src/App.react';
import {MemoryRouter} from 'react-router';
import {ApolloProvider} from 'react-apollo';
import PropTypes from 'prop-types';
import {addMockFunctionsToSchema} from 'graphql-tools';
import {SchemaLink} from 'apollo-link-schema';
import * as graphqlIntrospectionResult from '../schema';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {buildClientSchema} from 'graphql';
import {ApolloClient} from 'apollo-client';
import get from 'lodash/get';


/*
  Mount the entire application (minus stuff in Root.react.js).

  (optional) options: {
    graphqlMocks: {
      <TypeName>: <Response>
    }
  }
 */
export const mountApplication = (endpoint, options) => {
  const mockApolloClient = generateMockApolloClient(get(options, 'graphqlMocks'));
  return mount(
    <ApolloProvider client={mockApolloClient}>
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

const generateMockApolloClient = (graphqlMocks) => {
  const schema = buildClientSchema(graphqlIntrospectionResult.data);
  addMockFunctionsToSchema({
    schema,
    mocks: graphqlMocks || {}
  });
  const apolloCache = new InMemoryCache(window.__APOLLO_STATE__);
  return new ApolloClient({
    cache: apolloCache,
    link: new SchemaLink({schema}),
  });
};
