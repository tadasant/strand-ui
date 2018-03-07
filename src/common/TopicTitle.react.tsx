import * as React from 'react';
import {Component} from 'react';
import Typography from 'material-ui/Typography';
import {Link} from 'react-router-dom';

interface PropTypes {
  title: string
  topicId: string
  center?: boolean
}

class TopicTitle extends Component<PropTypes> {
  render() {
    return (
      <Typography
        variant='title'
        align={this.props.center ? 'center' : undefined}>
        <Link to={`/topics/${this.props.topicId}`} style={{textDecoration: 'unset'}}>{this.props.title}</Link>
      </Typography>
    );
  }
}

export default TopicTitle;
