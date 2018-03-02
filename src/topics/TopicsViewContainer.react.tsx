import * as React from 'react';
import {StatelessComponent} from 'react';
import TopicsView from './TopicsView.react';
import {GET_TOPICS_QUERY} from '../../schema/graphql-queries';
import {
  GetTopicsQuery, GetTopicsTopicsFragment, ReferenceTagsFragment,
  ReferenceUsersFragment
} from '../../schema/graphql-types';
import {graphql} from 'react-apollo';

interface StaticPropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

interface PropTypes extends StaticPropTypes {
  topics: GetTopicsTopicsFragment[],
}

const TopicsViewContainer: StatelessComponent<PropTypes> = props => (
  <TopicsView topics={props.topics}/>
);

const withTopics = graphql<GetTopicsQuery, StaticPropTypes>(GET_TOPICS_QUERY);

// Private topics will be null. For now this is expected, in the future it would probably be an error. TODO
const filterNullResults = (topics: (GetTopicsTopicsFragment | null)[]): GetTopicsTopicsFragment[] => {
  return topics.filter(x => x) as GetTopicsTopicsFragment[];
};

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
// Right now we're just ignoring any graphql errors
export default withTopics(({data, tags, users}) => {
  if (!data || !data.topics) {
    return <h1>{`ERROR ${data && data.error && data.error.message || ''}`}</h1>
  }
  if (data.loading) return <div>Loading...</div>;
  const nonNullTopics = filterNullResults(data.topics);
  return <TopicsViewContainer topics={nonNullTopics} tags={tags} users={users}/>
});
