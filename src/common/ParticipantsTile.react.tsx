import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import List from 'material-ui/List';
import UserListItem from './UserListItem.react';
import {filter} from 'lodash';
import {GetTopicsOriginalPosterFragment, GetTopicsParticipantsFragment} from '../../schema/graphql-types';

interface PropTypes {
  originalPoster: GetTopicsOriginalPosterFragment
  participants: GetTopicsParticipantsFragment[]
}

class ParticipantsTile extends Component<PropTypes> {
  nonOriginalPosterParticipants() {
    return filter(this.props.participants, participant => this.props.originalPoster.id !== participant.id);
  }

  render() {
    const otherParticipants = this.nonOriginalPosterParticipants();
    return (
      <List dense>
        <UserListItem user={this.props.originalPoster} isOriginalPoster/>
        <Divider inset/>
        {otherParticipants.map(participant => (
          <div key={participant.id}>
            <Divider inset/>
            <UserListItem user={participant}/>
          </div>
        ))}
      </List>
    );
  }
}

export default ParticipantsTile;
