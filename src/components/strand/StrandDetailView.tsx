import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Hidden from 'material-ui/Hidden';
import {GetStrandDetailStrandFragment} from '../../../schema/graphql-types';
import StrandViewDesktop from './rwd/StrandDetailViewDesktop';
import StrandViewMobile from './rwd/StrandDetailViewMobile';


interface PropTypes {
  strand: GetStrandDetailStrandFragment
}

class StrandView extends Component<PropTypes> {
  renderBody() {
    return (
      <div>
        <Hidden mdUp>
          <StrandViewMobile
            {...this.props}
          />
        </Hidden>
        <Hidden smDown>
          <StrandViewDesktop
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

export default StrandView;
