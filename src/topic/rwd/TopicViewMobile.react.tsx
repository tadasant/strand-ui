import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Dialogue from '../common/Dialogue.react';
import TopicViewHeaderStacked from '../common/TopicViewHeaderStacked.react';
import {GetTopicMessageFragment, GetTopicTopicFragment} from '../../../schema/graphql-types';

interface PropTypes {
  topic: GetTopicTopicFragment
}


class HelpSessionDetailMobile extends Component<PropTypes> {
  render() {
    return (
      <Grid item>
        <Grid item>
          <TopicViewHeaderStacked topic={this.props.topic}/>
          <Divider style={{marginTop: '5vh', marginBottom: '5vh'}}/>
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
            {/*TODO [UI-50] no nulls in graphql to eliminate non-nulls*/}
            <Dialogue messages={this.props.topic.discussion!.messages as GetTopicMessageFragment[]} minimal/>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default HelpSessionDetailMobile;
