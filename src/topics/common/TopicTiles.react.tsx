import * as React from 'react';
import {Component} from 'react';
import TopicTile from './tile/TopicTile.react';
import Grid from 'material-ui/Grid';
import TopicTileMinimal from './tile/TopicTileMinimal.react';
import {GetTopicsTopicsFragment} from '../../../schema/graphql-types';

interface PropTypes {
  topics: GetTopicsTopicsFragment[]
  minimal?: boolean
}

class TopicTiles extends Component<PropTypes> {
  render() {
    return (
      <Grid container alignItems='stretch' direction='column'>
        {this.props.topics.map(topic => (
          <Grid item key={topic.id}>
            {this.props.minimal ? <TopicTileMinimal topic={topic} /> : <TopicTile topic={topic}/>}
          </Grid>
        ))}
      </Grid>
    );
  }
}

export default TopicTiles;
