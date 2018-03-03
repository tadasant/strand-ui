import * as React from 'react';
import {Component} from 'react';
import Chip from 'material-ui/Chip';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import {PropTypes} from 'material-ui';

interface PropTypes {
  topic: {
    description: string,
    tags:  Array< {
      name: string,
    } | null > | null,
  }
}

class TopicSummaryTile extends Component<PropTypes> {
  render() {
    const {description, tags} = this.props.topic;
    return (
      <Grid container alignItems='stretch' direction='column'>
        <Grid item>
          <Typography variant='body2'>
            {description}
          </Typography>
        </Grid>
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

export default TopicSummaryTile;
