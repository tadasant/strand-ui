import React from 'react';
import ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './src/Root.react';

// Last of config setup
let GraphQLURL = process.env.PORTAL_GRAPHQL_URL;
if (process.env.REALM === 'staging') {
  // Staging build should mirror production except...
  GraphQLURL = 'https://www.staging.codeclippy.com/graphql';
}

const client = new ApolloClient({
  link: new HttpLink({uri: GraphQLURL}),
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <Root/>
  </ApolloProvider>,
  document.getElementById('root'),
);
