import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import StrandSummaryTile from '../../common/StrandSummaryTile';
import StrandTitle from "../../common/StrandTitle";
import {GetStrandDetailStrandFragment} from '../../../../schema/graphql-types';


interface PropTypes {
  strand: GetStrandDetailStrandFragment
}

const style = {
  contentGrid: {
    padding: '1% 1% 1% 1%',
  },
};

class StrandDetailTopView extends Component<PropTypes> {
  render() {
    const {title, saver, id} = this.props.strand;
    return (
      <Grid
        container
        direction='row'
        alignItems='stretch'>
        <Grid item sm={4}/>
        <Grid item sm={4}>
          <Paper>
            <Grid
              container
              direction='column'
              justify='center'
              alignItems='stretch'
              style={style.contentGrid}>
              <Grid item>
                {/*// TODO [UI-50]: Eliminate !'s with non-nullables*/}
                <StrandTitle title={title} strandId={id} saver={saver!}/>
              </Grid>
              <Grid item>
                <StrandSummaryTile strand={this.props.strand}/>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid item sm={4}/>
      </Grid>
    );
  }
}

export default StrandDetailTopView;
