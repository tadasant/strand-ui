import {RavenStatic} from 'raven-js';

const Raven: RavenStatic = jest.genMockFromModule('raven-js');

Raven.isSetup = () => false;

module.exports = Raven;
