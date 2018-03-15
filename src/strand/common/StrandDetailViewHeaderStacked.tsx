import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Paper from 'material-ui/Paper';
import StrandSummaryTile from '../../common/StrandSummaryTile';
import StrandTitle from "../../common/StrandTitle";
import {GetStrandDetailStrandFragment} from '../../../schema/graphql-types';


interface PropTypes {
  strand: GetStrandDetailStrandFragment
}

const style = {
  contentGrid: {
    padding: '1% 1% 1% 1%',
  },
};

class StrandDetailTopViewStacked extends Component<PropTypes> {
  render() {
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
                      {this.props.strand.title}
                    </Typography>
                    <Divider/>
                  </Grid>
                  <Grid item>
                    <StrandSummaryTile strand={this.props.strand}/>
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
                    <StrandTitle title={this.props.strand.title} strandId={this.props.strand.id} center/>
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

export default StrandDetailTopViewStacked;
