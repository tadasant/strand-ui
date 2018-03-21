import * as React from 'react';
import {Component} from 'react';
import Chip from 'material-ui/Chip';
import Grid from 'material-ui/Grid';

interface PropTypes {
  strand: {
    tags: Array<{
      name: string,
    } | null> | null,
  }
}

class StrandSummaryTile extends Component<PropTypes> {
  render() {
    const {tags} = this.props.strand;
    return (
      <Grid container alignItems='stretch' direction='column'>
        <Grid item>
          <Grid container spacing={8}>
            {/*// TODO [UI-50]: Eliminate !'s with non-nullable arrays*/}
            {tags!.map(tag => (
              <Grid item key={tag!.name}>
                <Chip label={tag!.name}/>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default StrandSummaryTile;
