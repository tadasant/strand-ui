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

class HelpSessionDetailTopViewStacked extends Component<PropTypes> {
  render() {
    const {originalPoster, id} = this.props.topic;
    const participants = this.props.topic.discussion ? this.props.topic.discussion.participants : [];
    return (
      <Grid container>
        <Grid item xs={1}/>
        <Grid item xs={10}>
          <Grid
            container
            direction='column'
            spacing={8}
            alignItems='stretch'>
            <Grid item style={{paddingBottom: '5vmax'}}>
              <Paper>
                <Grid
                  container
                  direction='column'
                  justify='center'
                  alignItems='stretch'
                  style={style.contentGrid}>
                  <Grid item>
                    <Typography
                      variant='title'>
                      {this.props.topic.title}
                    </Typography>
                    <Divider/>
                  </Grid>
                  <Grid item>
                    <TopicSummaryTile topic={this.props.topic}/>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
            <Grid item style={{paddingBottom: '5vmax'}}>
              <Paper>
                <Grid
                  container
                  direction='column'
                  justify='center'
                  alignItems='stretch'
                  style={style.contentGrid}>
                  <Grid item>
                    <TopicTitle title={this.props.topic.title} topicId={this.props.topic.id} center/>
                  </Grid>
                  <Grid item>
                    {/*TODO [UI-50] no nulls in graphql to eliminate non-nulls*/}
                    <ParticipantsTile
                      originalPoster={originalPoster!}
                      participants={participants}
                    />
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
            <Grid item>
              <Paper>
                <Grid
                  container
                  direction='column'
                  justify='center'
                  alignItems='stretch'
                  style={style.contentGrid}>
                  <Grid item>
                    {/*TODO [UI-50] no nulls in graphql to eliminate non-nulls*/}
                    <TimeTile
                      timeStart={this.props.topic.discussion!.timeStart!}
                      timeEnd={this.props.topic.discussion!.timeEnd!}
                    />
                    <Divider/>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={1}/>
      </Grid>
    );
  }
}

export default HelpSessionDetailTopViewStacked;
