import * as React from 'react';
import {Component} from 'react';
import StrandTileDetail from './tile/StrandTileDetail';
import Grid from 'material-ui/Grid';
import StrandTileDetailMinimal from './tile/StrandTileDetailMinimal';
import {GetStrandListStrandsFragment} from '../../../../schema/graphql-types';

interface PropTypes {
  strands: GetStrandListStrandsFragment[]
  minimal?: boolean
}

class StrandTileList extends Component<PropTypes> {
  render() {
    return (
      <Grid container alignItems='stretch' direction='row'>
        {this.props.strands.map(strand => (
          <Grid item xs={6} key={`strand_${strand.id}`}>
            {this.props.minimal ? <StrandTileDetailMinimal strand={strand} /> : <StrandTileDetail strand={strand}/>}
          </Grid>
        ))}
      </Grid>
    );
  }
}

export default StrandTileList;
