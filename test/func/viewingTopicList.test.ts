import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import TopicTiles from 'src/topics/common/TopicTiles.react';
import {topicFaker} from './viewingTopicList.data';
import {MockList} from 'graphql-tools';
import * as faker from "faker";

function flushPromises() {
  return new Promise(resolve => setImmediate(resolve));
}

describe('viewing existing topics', () => {
  it('shows the user a list of two topics when clicking into the topic page', async () => {
    faker.seed(10);
    const graphQLMocks = {
      Query: () => ({
        topics: () => new MockList(2, () => topicFaker()),
      })
    };
    const wrapper = mountApplication('/', {graphQLMocks});

    // Navigate to topics page
    wrapper.find(`Button[id="${navigationLabelToPath.Topics}-button"]`).simulate('click');
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Assert that the TopicTiles look same as ever
    const topicTilesComponent = wrapper.find(TopicTiles);
    expect(topicTilesComponent).toHaveLength(1);
    expect(topicTilesComponent).toMatchSnapshot();
  });

  // TODO test filters (omitting until we know if we're going to do server calls)

});
