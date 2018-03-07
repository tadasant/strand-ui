import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import List from 'material-ui/List';
import UserListItem from './UserListItem.react';
import {filter} from 'lodash';
import {GetTopicUserFragment} from '../../schema/graphql-types';

interface PropTypes {
  originalPoster: GetTopicUserFragment
  // TODO [UI-50] No nullable arrays
  participants: (GetTopicUserFragment | null)[] | null
}

class ParticipantsTile extends Component<PropTypes> {
  nonOriginalPosterParticipants(participants: (GetTopicUserFragment | null)[]) {
    return filter(participants, participant => this.props.originalPoster.id !== participant!.id);
  }

  render() {
    const participants = this.props.participants || [];
    const otherParticipants = this.nonOriginalPosterParticipants(participants);
    return (
      <List dense>
        <UserListItem user={this.props.originalPoster} isOriginalPoster/>
        <Divider inset/>
        {otherParticipants.map(participant => (
          <div key={`participant_${participant!.id}`}>
            <Divider inset/>
            <UserListItem user={participant!}/>
          </div>
        ))}
      </List>
    );
  }
}

export default ParticipantsTile;
