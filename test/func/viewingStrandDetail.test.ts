import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import {strandFaker} from './viewingStrandDetail.data';
import {strandFaker as strandListStrandFaker} from './viewingStrandList.data';
import {MockList} from 'graphql-tools';
import StrandView from '../../src/components/strand/StrandDetailView';
import StrandTiles from '../../src/components/strands/common/StrandTiles';
import * as faker from "faker";
import {flushPromises} from '../helper/utilities';

describe('viewing existing strand', () => {
  it('shows the user a filled out detail page when a strand detail page is opened', async () => {
    faker.seed(10);
    const graphQLMocks = {
      Query: () => ({
        strands: () => new MockList(1, () => strandListStrandFaker()),
        strand: () => strandFaker(),
      })
    };
    const wrapper = mountApplication('/', {graphQLMocks});

    // Navigate to strands page
    wrapper.find(`Button[id="${navigationLabelToPath.Strands}-button"]`).simulate('click');
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Navigate to the strand detail page
    wrapper.find(StrandTiles).find('a').simulate('click', {button: 0});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Assert that the Detail pages looks same as ever
    const strandViewComponent = wrapper.find(StrandView);
    expect(strandViewComponent).toHaveLength(1);
    expect(strandViewComponent).toMatchSnapshot();
  });
});
