import * as React from 'react';
import {mount, ReactWrapper} from 'enzyme';
import App from 'src/App';
import {MemoryRouter} from 'react-router';
import {ApolloProvider} from 'react-apollo';
import {addMockFunctionsToSchema} from 'graphql-tools';
import {SchemaLink} from 'apollo-link-schema';
import {InMemoryCache, NormalizedCacheObject} from 'apollo-cache-inmemory';
import {buildClientSchema} from 'graphql';
import {ApolloClient} from 'apollo-client';
import * as graphqlIntrospectionResult from '../../schema/graphql.schema.json';
import TestStrandSlackClient from '../clients/TestStrandSlackClient';
import TestStrandApiClient from '../clients/TestStrandApiClient';


/*
  Mount the entire application (minus stuff in Root.tsx).

  (optional) options: {
    graphqlMocks: {
      <TypeName>: <Response>
    }
  }
 */
export const mountApplication = (endpoint: string, options?: { graphQLMocks: {} }): ReactWrapper<any, any> => {
  const mockApolloClient = generateMockApolloClient(options ? options.graphQLMocks : {});
  const wrapper = mount(
    <ApolloProvider client={mockApolloClient}>
      <MemoryRouter initialEntries={[endpoint]} initialIndex={0} keyLength={0}>
        {/*keyLength is 0 so keys aren't generated (they break jest snapshots)*/}
        <App/>
      </MemoryRouter>
    </ApolloProvider>,
  );
  setUpTestClients();
  return wrapper;
};

const generateMockApolloClient = (graphqlMocks: {}): ApolloClient<NormalizedCacheObject> => {
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

const setUpTestClients = () => {
  // TODO [UI-59] replace with React 16.3 new context API
  global.strandSlackClient = new TestStrandSlackClient();
  global.strandApiClient = new TestStrandApiClient();
};
