import React from 'react';
import ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './src/Root.react';
import ErrorBoundary from './src/common/ErrorBoundary.react';
import * as Raven from 'raven-js';

// TODO can get rid of these consts/contexts, just use the ENV vars as needed directly
const graphQLUrl = process.env.PORTAL_GRAPHQL_URL;
const uiHost = process.env.UI_HOST;
const slackClientId = process.env.SLACK_CLIENT_ID;

// sentry.io
if (process.env.NODE_ENV === 'production' || process.env.NODE_ENV === 'staging') {
  const sentryioKey = process.env.SENTRY_IO_KEY;
  const sentryioProject = process.env.SENTRY_IO_PROJECT;
  Raven.config(`https://${sentryioKey}@sentry.io/${sentryioProject}`, {
    environment: process.env.NODE_ENV,
    tags: {release: process.env.VERSION},
  }).install();
}

const client = new ApolloClient({
  link: new HttpLink({uri: graphQLUrl}),
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ErrorBoundary>
    <ApolloProvider client={client}>
      <Root uiHost={uiHost} slackClientId={slackClientId}/>
    </ApolloProvider>
  </ErrorBoundary>,
  document.getElementById('root'),
);