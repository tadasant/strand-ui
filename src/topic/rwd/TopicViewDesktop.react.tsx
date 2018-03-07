import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Dialogue from '../common/Dialogue.react';
import TopicViewHeader from '../common/TopicViewHeader.react';
import {GetTopicMessageFragment, GetTopicTopicFragment} from '../../../schema/graphql-types';

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
          <Grid item style={{padding: '2% 2% 2% 2%', overflow: 'hidden'}}>
            {/*TODO [UI-50] no nulls in graphql to eliminate non-nulls*/}
            <Dialogue messages={this.props.topic.discussion!.messages as GetTopicMessageFragment[]}/>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default TopicViewDesktop;
