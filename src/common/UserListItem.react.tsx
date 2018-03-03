import * as React from 'react';
import {Component} from 'react';
import {ListItem, ListItemIcon, ListItemText} from 'material-ui';
import AccountCircle from 'material-ui-icons/AccountCircle';
import QuestionAnswer from 'material-ui-icons/QuestionAnswer';

interface PropTypes {
  user: {
    alias: string
  }
  isOriginalPoster?: boolean
}

class UserListItem extends Component<PropTypes> {
  renderAppropriateIcon() {
    let icon = null;
    if (this.props.isOriginalPoster) {
      icon = <QuestionAnswer/>;
    }
    return icon ? <ListItemIcon>{icon}</ListItemIcon> : null;
  }

  render() {
    return (
      <ListItem>
        <ListItemIcon>
          <AccountCircle/>
        </ListItemIcon>
        <ListItemText
          primary={`${this.props.user.alias}`}
        />
        {this.renderAppropriateIcon()}
      </ListItem>
    );
  }
}

export default UserListItem;
