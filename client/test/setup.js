import Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import dotenv from 'dotenv'
import {buildClientSchema} from 'graphql';
import * as graphqlIntrospectionResult from 'test/schema.json';
import {addMockFunctionsToSchema} from 'graphql-tools';
import {ApolloClient} from 'apollo-client';
import {SchemaLink} from 'apollo-link-schema';
import {InMemoryCache} from 'apollo-cache-inmemory';

// environment variables
dotenv.config();

// enzyme
configure({adapter: new Adapter()});

// graphql mocking
const schema = buildClientSchema(graphqlIntrospectionResult.data);
addMockFunctionsToSchema({schema, mocks: {}, preserveResolvers: true});
const apolloCache = new InMemoryCache(window.__APOLLO_STATE__);
const client = new ApolloClient({
  cache: apolloCache,
  link: new SchemaLink({schema}),
});

global.__MOCK_APOLLO_CLIENT__ = client;

// TODO figure out how to run these once instead of once before each test suite
