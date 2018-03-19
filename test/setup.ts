import * as Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import * as dotenv from 'dotenv';
import TestStrandSlackClient from './clients/TestStrandSlackClient';

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
  const strand_slack_client = global.strand_slack_client as TestStrandSlackClient;
  strand_slack_client.clearState();
});
