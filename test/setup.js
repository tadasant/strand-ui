import Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import dotenv from 'dotenv'

// environment variables
dotenv.config();

// enzyme
configure({adapter: new Adapter()});

// sentry.io
global.Raven = {
  isSetup: jest.fn(() => false),
};
