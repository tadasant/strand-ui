import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Paper from 'material-ui/Paper';
import ParticipantsTile from '../../common/ParticipantsTile.react';
import TopicSummaryTile from '../../common/TopicSummaryTile.react';
import TimeTile from './TimeTile.react';
import TopicTitle from "../../common/TopicTitle.react";
import {GetTopicTopicFragment} from '../../../schema/graphql-types';


interface PropTypes {
  topic: GetTopicTopicFragment
}

const style = {
  contentGrid: {
    padding: '1% 1% 1% 1%',
  },
};

class HelpSessionDetailTopView extends Component<PropTypes> {
  render() {
    const {originalPoster, id} = this.props.topic;
    const participants = this.props.topic.discussion ? this.props.topic.discussion.participants : [];
    return (
      <Grid
        container
        direction='row'
        alignItems='stretch'>
        <Grid item sm={1}/>
        <Grid item sm={4}>
          <Paper>
            <Grid
              container
              direction='column'
              justify='center'
              alignItems='stretch'
              style={style.contentGrid}>
              <Grid item>
                <TopicTitle title={this.props.topic.title} topicId={id}/>
                <Divider/>
              </Grid>
              <Grid item>
                <TopicSummaryTile topic={this.props.topic}/>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item sm={3}>
          <Paper>
            <Grid
              container
              direction='column'
              justify='center'
              alignItems='stretch'
              style={style.contentGrid}>
              <Grid item>
                <Typography
                  align='center'
                  variant='title'>
                  Participants
                </Typography>
              </Grid>
              <Grid item>
                <ParticipantsTile
                  originalPoster={originalPoster!}
                  participants={participants}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item sm={3}>
          <Paper>
            <Grid
              container
              direction='column'
              justify='center'
              alignItems='stretch'
              style={style.contentGrid}>
              <Grid item>
                <TimeTile
                  timeStart={this.props.topic.discussion!.timeStart!}
                  timeEnd={this.props.topic.discussion!.timeEnd!}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item sm={1}/>
      </Grid>
    );
  }
}

export default HelpSessionDetailTopView;
