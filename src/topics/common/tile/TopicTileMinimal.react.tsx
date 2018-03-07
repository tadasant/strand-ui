import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import ParticipantsTile from '../../../common/ParticipantsTile.react';
import TopicSummaryTile from '../../../common/TopicSummaryTile.react';
import TopicTitle from '../../../common/TopicTitle.react';
import {GetTopicsUserFragment, GetTopicsTopicsFragment} from '../../../../schema/graphql-types';
import {PropTypes} from 'material-ui';

interface PropTypes {
  topic: GetTopicsTopicsFragment
}

const style = {
  content: {
    padding: '1% 1% 1% 1%',
  },
};

class TopicTileMinimal extends Component<PropTypes> {

  render() {
    const {title, originalPoster, discussion, id} = this.props.topic;
    const participants = discussion ? discussion.participants : [];
    return (
      <Paper>
        <Grid
          container
          direction='column'
          style={style.content}>
          <Grid item>
            <TopicTitle title={title} topicId={id}/>
            <Divider/>
          </Grid>
          <Grid item>
            <TopicSummaryTile topic={this.props.topic}/>
          </Grid>
        </Grid>
        <Grid
          container
          direction='column'
          alignItems='center'
          spacing={8}
          style={style.content}>
          <Grid item xs={10}>
            <Paper>
              <ParticipantsTile
                // TODO [UI-50]: Eliminate as's with non-nullable arrays
                originalPoster={originalPoster as GetTopicsUserFragment}
                participants={participants as GetTopicsUserFragment[]}
              />
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}

export default TopicTileMinimal;
