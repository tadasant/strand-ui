import * as React from 'react';
import TopicView from './TopicView.react';
import {GET_TOPIC_QUERY} from '../../schema/graphql-queries';
import {graphql} from 'react-apollo';
import {GetTopicQuery} from '../../schema/graphql-types';
import CircularProgress from 'material-ui/Progress/CircularProgress';

interface PropTypes {
  topicId: string,
}

const withTopic = graphql<GetTopicQuery, PropTypes>(GET_TOPIC_QUERY, {
  options: (props) => ({
    variables: {id: props.topicId},
    'errorPolicy': 'all', // Returns partial data
  } as any) // TODO Apollo types bug. Should be fixed with next npm release of react-apollo (>2.0.4).
});

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
// Right now we're just ignoring any graphql errors
const TopicViewContainer = withTopic(({data}) => {
  if (data && data.loading) return <CircularProgress/>;
  if (!data || !data.topic) {
    return <h1>{`ERROR ${data && data.error && data.error.message || ''}`}</h1>
  }
  return <TopicView topic={data.topic}/>
});

export default TopicViewContainer;
