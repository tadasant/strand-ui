import * as React from 'react';
import TopicsView from './TopicsView.react';
import {GET_TOPICS_QUERY} from '../../schema/graphql-queries';
import {GetTopicsQuery, ReferenceTagsFragment, ReferenceUsersFragment} from '../../schema/graphql-types';
import {graphql} from 'react-apollo';
import {filterFalsey} from '../common/utilities';
import CircularProgress from 'material-ui/Progress/CircularProgress';

interface StaticPropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

const withTopics = graphql<GetTopicsQuery, StaticPropTypes>(GET_TOPICS_QUERY, {
  options: {
    'errorPolicy': 'all', // Returns partial data
  } as any // TODO Apollo types bug. Should be fixed with next npm release of react-apollo (>2.0.4).
});

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
// Right now we're just ignoring any graphql errors
const TopicsViewContainer = withTopics(({data, tags, users}) => {
  if (data && data.loading) return <CircularProgress/>;
  if (!data || !data.topics) {
    return <h1>{`ERROR ${data && data.error && data.error.message || ''}`}</h1>
  }
  const nonNullTopics = filterFalsey(data.topics);
  return <TopicsView topics={nonNullTopics} tags={tags} users={users}/>
});

export default TopicsViewContainer;
