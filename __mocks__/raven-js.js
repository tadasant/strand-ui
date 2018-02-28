const Raven = jest.genMockFromModule('fs');

Raven.isSetup = () => false;

module.exports = Raven;
