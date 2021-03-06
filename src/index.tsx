// Triple slash directive to grab our global types for the project (needs to be above imports)
/// <reference path="index.d.ts" />

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {setContext} from 'apollo-link-context';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './Root';
import ErrorBoundary from './components/common/ErrorBoundary';
import * as CONFIG from './config';
import * as Raven from 'raven-js';
import * as Cookies from 'js-cookie';

// sentry.io setup
if (CONFIG.NODE_ENV === 'production' || CONFIG.NODE_ENV === 'staging') {
  Raven.config(`https://${CONFIG.SENTRY_KEY}@sentry.io/${CONFIG.SENTRY_PROJECT_ID}`, {
    environment: CONFIG.NODE_ENV,
    release: CONFIG.VERSION,
  }).install();
}

// GraphQL auth
// https://www.apollographql.com/docs/react/recipes/authentication.html
const authLink = setContext((_, {headers}) => {
  const token = Cookies.get(CONFIG.AUTH_COOKIE_NAME);
  return {
    headers: {
      ...headers,
      authorization: token ? `Token ${token}` : '',
    },
  };
});

// GraphQL client setup
const httpLink = new HttpLink({uri: CONFIG.GRAPHQL_URL});
const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ErrorBoundary>
    <ApolloProvider client={client}>
      <Root/>
    </ApolloProvider>
  </ErrorBoundary>,
  document.getElementById('root'),
);