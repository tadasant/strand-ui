import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
// import Dialogue from '../common/Dialogue';
import TopicViewHeader from '../common/TopicViewHeader.react';
import {GetTopicTopicFragment} from '../../../schema/graphql-types';

interface PropTypes {
  topic: GetTopicTopicFragment
}

class TopicViewDesktop extends Component<PropTypes> {
  render() {
    return (
      <Grid item>
        <Grid item>
          <TopicViewHeader topic={this.props.topic}/>
          <Divider style={{marginTop: '2.5%', marginBottom: '2.5%'}}/>
        </Grid>
        <Grid item>
          <Grid item>
            <Typography
              align='center'
              variant='title'>
              Dialogue
            </Typography>
          </Grid>
          <Grid item>
            {/*<Dialogue discussion={this.props.topic.discussion}/>*/}
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default TopicViewDesktop;
