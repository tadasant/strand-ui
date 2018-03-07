import * as Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import * as dotenv from 'dotenv';

// environment variables
dotenv.config({path: 'env/.env.test'});

// enzyme
configure({adapter: new Adapter()});

// lock in the timing that moment uses
jest.mock('moment', () => {
  const moment = require.requireActual('moment');
  return moment.utc;
});