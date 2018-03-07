import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import ParticipantsTile from '../../../common/ParticipantsTile.react';
import TopicSummaryTile from '../../../common/TopicSummaryTile.react';
import TopicTitle from '../../../common/TopicTitle.react';
import {GetTopicsTopicsFragment, GetTopicsUserFragment} from '../../../../schema/graphql-types';

interface PropTypes {
  topic: GetTopicsTopicsFragment
}

const style = {
  content: {
    padding: '2% 2% 2% 2%',
  },
};

class TopicTile extends Component<PropTypes> {
  render() {
    const {title, originalPoster, discussion, id} = this.props.topic;
    const participants = discussion ? discussion.participants : [];
    return (
      <Paper>
        <Grid container spacing={8} style={style.content}>
          <Grid item xs={12}>
            <TopicTitle title={title} topicId={id}/>
            <Divider/>
          </Grid>
          <Grid item xs={8}>
            <TopicSummaryTile topic={this.props.topic}/>
          </Grid>
          <Grid item xs={4}>
            <Grid
              container
              direction='column'
              alignItems='stretch'>
              <Grid item>
                <Paper>
                  <ParticipantsTile
                    // TODO [UI-50]: Eliminate as's with non-nullable arrays
                    originalPoster={originalPoster as GetTopicsUserFragment}
                    participants={participants as GetTopicsUserFragment[]}
                  />
                </Paper>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}

export default TopicTile;
