import * as React from 'react';
import {Component} from 'react';
import Typography from 'material-ui/Typography';
import {Link} from 'react-router-dom';

interface PropTypes {
  title: string | null
  strandId: string
  center?: boolean
}

class StrandTitle extends Component<PropTypes> {
  render() {
    return (
      <Typography
        variant='title'
        align={this.props.center ? 'center' : undefined}>
        <Link to={`/strands/${this.props.strandId}`} style={{textDecoration: 'unset'}}>
          {this.props.title || '[No Title]'}
        </Link>
      </Typography>
    );
  }
}

export default StrandTitle;
