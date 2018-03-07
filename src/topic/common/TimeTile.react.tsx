import * as React from 'react';
import {Component} from 'react';
import ListItem from 'material-ui/List/ListItem';
import ListItemText from 'material-ui/List/ListItemText';
import * as moment from 'moment';
import {Moment} from 'moment';

interface PropTypes {
  timeStart: string
  timeEnd: string
}

class TimeTile extends Component<PropTypes> {
  static formatDuration(start: Moment, end: Moment): string {
    const minutes = end.diff(start, 'minutes');
    const seconds = end.diff(start, 'seconds') % 60;
    return `${minutes}m, ${seconds}s`;
  }

  render() {
    const start = moment(this.props.timeStart);
    const end = moment(this.props.timeEnd);
    return (
      <ListItem>
        <ListItemText
          primary='Start'
          secondary={start.format('YYYY-MM-DD')}
        />
        <ListItemText
          primary='End'
          secondary={end.format('YYYY-MM-DD')}

        />
        <ListItemText
          primary='Duration'
          secondary={TimeTile.formatDuration(start, end)}
        />
      </ListItem>
    );
  }
}

export default TimeTile;
