import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import {topicFaker} from './viewingTopicDetail.data';
import {topicFaker as topicListTopicFaker} from './viewingTopicList.data';
import {MockList} from 'graphql-tools';
import TopicView from '../../src/topic/TopicView.react';
import TopicTiles from '../../src/topics/common/TopicTiles.react';
import * as faker from "faker";
import {flushPromises} from '../helper/utilities';

describe('viewing existing topic', () => {
  it('shows the user a filled out detail page when a topic detail page is opened', async () => {
    faker.seed(10);
    const graphQLMocks = {
      Query: () => ({
        topics: () => new MockList(1, () => topicListTopicFaker()),
        topic: () => topicFaker(),
      })
    };
    const wrapper = mountApplication('/', {graphQLMocks});

    // Navigate to topics page
    wrapper.find(`Button[id="${navigationLabelToPath.Topics}-button"]`).simulate('click');
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Navigate to the topic detail page
    wrapper.find(TopicTiles).find('a').simulate('click', {button: 0});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    // Assert that the Detail pages looks same as ever
    const topicViewComponent = wrapper.find(TopicView);
    expect(topicViewComponent).toHaveLength(1);
    expect(topicViewComponent).toMatchSnapshot();
  });
});
