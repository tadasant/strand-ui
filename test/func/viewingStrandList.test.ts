import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import StrandTiles from 'src/components/strands/common/StrandTiles';
import {strandFaker} from './viewingStrandList.data';
import {MockList} from 'graphql-tools';
import * as faker from "faker";
import {flushPromises} from '../helper/utilities';

describe('viewing existing strands', () => {
  it('shows the user a list of two strands when clicking into the strand page', async () => {
    faker.seed(10);
    const graphQLMocks = {
      Query: () => ({
        strands: () => new MockList(2, () => strandFaker()),
      })
    };
    const wrapper = mountApplication('/', {graphQLMocks});

    // Navigate to strands page
    wrapper.find(`Button[id="${navigationLabelToPath.Strands}-button"]`).simulate('click');
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Assert that the StrandTiles look same as ever
    const strandTilesComponent = wrapper.find(StrandTiles);
    expect(strandTilesComponent).toHaveLength(1);
    expect(strandTilesComponent).toMatchSnapshot();
  });

  // TODO test filters (omitting until we know if we're going to do server calls)

});
