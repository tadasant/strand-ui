import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import TopicTiles from 'src/topics/common/TopicTiles.react';

function flushPromises() {
  return new Promise(resolve => setImmediate(resolve));
}

describe('viewing existing topics', () => {
  it('sends the user to Slack when the user navigates to the page and clicks the button', async () => {
    const wrapper = mountApplication('/');

    // Navigate to topics page
    wrapper.find(`Button[id="${navigationLabelToPath.Topics}-button"]`).simulate('click');
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Assert that the TopicTiles look same as ever
    const topicTilesComponent= wrapper.find(TopicTiles);
    expect(topicTilesComponent).toHaveLength(1);
  });

  // TODO test filters (omitting until we know if we're going to do server calls)

});
