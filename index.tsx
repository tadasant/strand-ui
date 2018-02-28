import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './src/Root.react';
import ErrorBoundary from './src/common/ErrorBoundary.react';
import * as Raven from 'raven-js';
import * as CONFIG from './config';

// Environment variable check
console.assert(
  [CONFIG.GRAPHQL_URL, CONFIG.SLACK_CLIENT_ID, CONFIG.UI_HOST, CONFIG.SLACK_SCOPES, CONFIG.NODE_ENV]
    .every(x => x != undefined),
  'Missing required general environment variables'
);
console.assert(
  [CONFIG.VERSION, CONFIG.SENTRY_KEY, CONFIG.SENTRY_PROJECT_ID].every(x => x != undefined),
  'Missing required deployment environment variables'
);

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