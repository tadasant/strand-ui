import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Hidden from 'material-ui/Hidden';
import {GetTopicTopicFragment} from '../../schema/graphql-types';
import TopicViewDesktop from './rwd/TopicViewDesktop.react';
import TopicViewMobile from './rwd/TopicViewMobile.react';


interface PropTypes {
  topic: GetTopicTopicFragment
}

class TopicView extends Component<PropTypes> {
  renderBody() {
    return (
      <div>
        <Hidden mdUp>
          <TopicViewMobile
            {...this.props}
          />
        </Hidden>
        <Hidden smDown>
          <TopicViewDesktop
            {...this.props}
          />
        </Hidden>
      </div>
    )
  }

  render() {
    return (
      <Grid
        container
        alignItems='stretch'
        direction='column'
        justify='space-around'>
        {this.renderBody()}
      </Grid>
    );
  }
}

export default TopicView;
