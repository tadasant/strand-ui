import React from 'react';
import ReactDOM from 'react-dom';
import {ApolloClient} from 'apollo-client';
import {HttpLink} from 'apollo-link-http';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import Root from './src/Root.react';

// Last of config setup (used because parcel.js sets $NODE_ENV to production for all `parcel build` ops)
let graphQLUrl = process.env.PORTAL_GRAPHQL_URL;
let uiHost = process.env.UI_HOST;
if (process.env.REALM === 'staging') {
  // Staging build should mirror production except...
  graphQLUrl = 'https://www.staging.codeclippy.com/graphql';
  uiHost = 'https://www.staging.codeclippy.com/';
}

// sentry.io
if (process.env.REALM in ['production', 'staging']) {
  const sentryioKey = process.env.SENTRY_IO_KEY;
  const sentryioProject = process.env.SENTRY_IO_PROJECT;
  Raven.config(`http://${sentryioKey}@sentry.io/${sentryioProject}`, {
    environment: process.env.REALM,
    tags: {release: process.env.VERSION},
  }).install();
}


const client = new ApolloClient({
  link: new HttpLink({uri: graphQLUrl}),
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <Root uiHost={uiHost}/>
  </ApolloProvider>,
  document.getElementById('root'),
);
