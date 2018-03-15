import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import StrandSummaryTile from '../../../common/StrandSummaryTile';
import StrandTitle from '../../../common/StrandTitle';
import {GetStrandListStrandsFragment} from '../../../../../schema/graphql-types';
import {PropTypes} from 'material-ui';

interface PropTypes {
  strand: GetStrandListStrandsFragment
}

const style = {
  content: {
    padding: '1% 1% 1% 1%',
  },
};

class StrandTileMinimal extends Component<PropTypes> {

  render() {
    const {title, id} = this.props.strand;
    return (
      <Paper>
        <Grid
          container
          direction='column'
          style={style.content}>
          <Grid item>
            <StrandTitle title={title} strandId={id}/>
            <Divider/>
          </Grid>
          <Grid item>
            <StrandSummaryTile strand={this.props.strand}/>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}

export default StrandTileMinimal;
