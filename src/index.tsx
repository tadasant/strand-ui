// Triple slash directive to grab our global types for the project (needs to be above imports)
/// <reference path="index.d.ts" />

import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './Root';
import ErrorBoundary from './components/common/ErrorBoundary';
import * as CONFIG from './config';
import * as Raven from 'raven-js';

// sentry.io setup
if (CONFIG.NODE_ENV === 'production' || CONFIG.NODE_ENV === 'staging') {
  Raven.config(`https://${CONFIG.SENTRY_KEY}@sentry.io/${CONFIG.SENTRY_PROJECT_ID}`, {
    environment: CONFIG.NODE_ENV,
    release: CONFIG.VERSION,
  }).install();
}

// GraphQL client setup
const client = new ApolloClient({
  link: new HttpLink({uri: CONFIG.GRAPHQL_URL}),
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