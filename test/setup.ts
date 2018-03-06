import * as Adapter from 'enzyme-adapter-react-16';
import {configure} from 'enzyme';
import * as dotenv from 'dotenv';
import * as casual from 'casual';

// environment variables
dotenv.config({path: 'env/.env.test'});

// enzyme
configure({adapter: new Adapter()});

// set casual seed for predictable fake values
casual.seed(100);