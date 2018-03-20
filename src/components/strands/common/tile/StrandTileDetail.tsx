import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import StrandSummaryTile from '../../../common/StrandSummaryTile';
import StrandTitle from '../../../common/StrandTitle';
import {GetStrandListStrandsFragment} from '../../../../../schema/graphql-types';

interface PropTypes {
  strand: GetStrandListStrandsFragment
}

const style = {
  content: {
    padding: '2% 2% 2% 2%',
  },
};

class StrandTileDetail extends Component<PropTypes> {
  render() {
    const {title, id, saver} = this.props.strand;
    return (
      <Paper>
        <Grid container spacing={8} style={style.content}>
          <Grid item xs={12}>
            <StrandTitle title={title} strandId={id} saver={saver!}/>
          </Grid>
          <Grid item xs={8}>
            <StrandSummaryTile strand={this.props.strand}/>
          </Grid>
        </Grid>
      </Paper>
    );
  }
}

export default StrandTileDetail;
