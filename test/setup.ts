import * as Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import * as dotenv from 'dotenv';
import TestStrandSlackClient from './clients/TestStrandSlackClient';
import TestStrandApiClient from './clients/TestStrandApiClient';
import * as faker from "faker";

// environment variables
dotenv.config({path: 'env/.env.test'});

// enzyme
configure({adapter: new Adapter()});

// lock in the timing that moment uses
jest.mock('moment', () => {
  const moment = require.requireActual('moment');
  return moment.utc;
});

afterEach(() => {
  const strandSlackClient = global.strandSlackClient as TestStrandSlackClient;
  const strandApiClient = global.strandApiClient as TestStrandApiClient;
  strandSlackClient.clearState();
  strandApiClient.clearState();
});
