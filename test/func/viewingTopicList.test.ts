import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import TopicTiles from 'src/topics/common/TopicTiles.react';
import {fakeTopic} from './viewingTopicList.data';
import {MockList} from 'graphql-tools';

function flushPromises() {
  return new Promise(resolve => setImmediate(resolve));
}

describe('viewing existing topics', () => {
  it('sends the user to Slack when the user navigates to the page and clicks the button', async () => {
    const graphQLMocks = {
      Query: () => ({
        topics: () => new MockList(2, () => fakeTopic()),
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
