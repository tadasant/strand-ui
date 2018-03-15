import * as React from 'react';
import {Component} from 'react';
import StrandTile from './tile/StrandTile';
import Grid from 'material-ui/Grid';
import StrandTileMinimal from './tile/StrandTileMinimal';
import {GetStrandListStrandsFragment} from '../../../schema/graphql-types';

interface PropTypes {
  strands: GetStrandListStrandsFragment[]
  minimal?: boolean
}

class StrandTiles extends Component<PropTypes> {
  render() {
    return (
      <Grid container alignItems='stretch' direction='column'>
        {this.props.strands.map(strand => (
          <Grid item key={`strand_${strand.id}`}>
            {this.props.minimal ? <StrandTileMinimal strand={strand} /> : <StrandTile strand={strand}/>}
          </Grid>
        ))}
      </Grid>
    );
  }
}

export default StrandTiles;
