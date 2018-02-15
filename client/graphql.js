import {graphql} from 'react-apollo';

const reactApollo = jest.genMockFromModule('react-apollo');
const mockGraphQl = reactApollo.graphql;





module.exports = mockGraphql;