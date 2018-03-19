import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
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
    const {id} = this.props.strand;
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
                <StrandTitle title={this.props.strand.title} strandId={id}/>
                <Divider/>
              </Grid>
              <Grid item>
                <StrandSummaryTile strand={this.props.strand}/>
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
            </Grid>
          </Paper>
        </Grid>
        <Grid item sm={4}/>
      </Grid>
    );
  }
}

export default StrandDetailTopView;
