import * as React from 'react';
import {Component} from 'react';
import Typography from 'material-ui/Typography';
import {Link} from 'react-router-dom';
import {GetStrandListUserFragment} from '../../../schema/graphql-types';
import Avatar from 'material-ui/Avatar';
import Grid from 'material-ui/Grid';

interface PropTypes {
  title: string | null
  strandId: string
  center?: boolean
  saver: GetStrandListUserFragment
}

class StrandTitle extends Component<PropTypes> {
  render() {
    return (
      <Grid container>
        <Grid item xs={10}>
          <Typography
            variant='title'
            style={{float: 'left'}}
            align={this.props.center ? 'center' : undefined}>
            <Link to={`/strands/${this.props.strandId}`} style={{textDecoration: 'unset'}}>
              {this.props.title || '[No Title]'}
            </Link>
          </Typography>
        </Grid>
        <Grid item xs={2}>
          <Avatar style={{float: 'right'}}>
            {this.props.saver.firstName.charAt(0)}{this.props.saver.lastName.charAt(0)}
          </Avatar>
        </Grid>
      </Grid>
    );
  }
}

export default StrandTitle;
