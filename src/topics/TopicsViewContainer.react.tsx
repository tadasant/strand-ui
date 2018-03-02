import * as React from 'react';
import {StatelessComponent} from 'react';
import TopicsView from './TopicsView.react';
import {GET_TOPICS_QUERY} from '../../schema/graphql-queries';
import {GetTopicsQuery, GetTopicsTopicsFragment} from '../../schema/graphql-types';
import {graphql} from 'react-apollo';

interface PropTypes {
  topics: GetTopicsTopicsFragment[],
}

const TopicsViewContainer: StatelessComponent<PropTypes> = () => (
  <TopicsView/>
);

const withTopics = graphql<GetTopicsQuery>(GET_TOPICS_QUERY);

// Private topics will be null. For now this is expected, in the future it would probably be an error. TODO
const filterNullResults = (topics: (GetTopicsTopicsFragment | null)[]): GetTopicsTopicsFragment[] => {
  return topics.filter(x => x) as GetTopicsTopicsFragment[];
};

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
export default withTopics(({data}) => {
  if (!data || !data.topics || data.error) {
    return <h1>{data ? data.error ? data.error : 'ERROR' : 'ERROR'}</h1>
  }
  if (data.loading) return <div>Loading...</div>;
  const nonNullTopics = filterNullResults(data.topics);
  return <TopicsViewContainer topics={nonNullTopics}/>
});
