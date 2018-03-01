import * as React from 'react';
import {mount} from 'enzyme';
import App from 'src/App.react';
import {MemoryRouter} from 'react-router';
import {ApolloProvider} from 'react-apollo';
import {addMockFunctionsToSchema} from 'graphql-tools';
import {SchemaLink} from 'apollo-link-schema';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {buildClientSchema} from 'graphql';
import {ApolloClient} from 'apollo-client';
import {get} from 'lodash';
import * as graphqlIntrospectionResult from '../schema.json';


/*
  Mount the entire application (minus stuff in Root.react.tsx).

  (optional) options: {
    graphqlMocks: {
      <TypeName>: <Response>
    }
  }
 */
export const mountApplication = (endpoint: string, options?: {}) => {
  const mockApolloClient = generateMockApolloClient(get(options, 'graphqlMocks'));
  return mount(
    <ApolloProvider client={mockApolloClient}>
      <MemoryRouter initialEntries={[endpoint]} initialIndex={0} keyLength={0}>
        {/*keyLength is 0 so keys aren't generated (they break jest snapshots)*/}
        <App/>
      </MemoryRouter>
    </ApolloProvider>,
  );
};

const generateMockApolloClient = (graphqlMocks: {}) => {
  const schema = buildClientSchema(graphqlIntrospectionResult.data);
  addMockFunctionsToSchema({
    schema,
    mocks: graphqlMocks || {},
  });
  const apolloCache = new InMemoryCache();
  return new ApolloClient({
    cache: apolloCache,
    link: new SchemaLink({schema}),
  });
};