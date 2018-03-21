import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import StrandTiles from 'src/components/strands/common/StrandTileList';
import {strandFaker} from './viewingStrandList.data';
import {MockList} from 'graphql-tools';
import * as faker from 'faker';
import {flushPromises} from '../helper/utilities';
import {fetchableVariables} from '../../src/components/strands/StrandListView';
import SearchBox from '../../src/components/strands/common/SearchBox';
import Input from 'material-ui/Input';
import StrandTileDetail from '../../src/components/strands/common/tile/StrandTileDetail';

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

  it('updates the list of strands when user adds a search query', async () => {
    faker.seed(10);
    const fakeQuery = faker.lorem.word();
    const graphQLMocks = {
      Query: () => ({
        strands: (_: any, {query}: fetchableVariables) => {
          return query === fakeQuery
            ? new MockList(5, () => strandFaker())
            : new MockList(2, () => strandFaker());
        }
      })
    };
    const wrapper = mountApplication('/strands', {graphQLMocks});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();
    expect(wrapper.find(StrandTileDetail).length).toEqual(2);

    const searchInputBox = wrapper.find(SearchBox).find(Input);
    searchInputBox.prop('onChange')({target: {value: fakeQuery}});
    searchInputBox.prop('onKeyDown')({key: 'Enter'});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    expect(wrapper.find(StrandTileDetail).length).toEqual(5);
  })

  // TODO test filters (omitting until we know if we're going to do server calls)

});
