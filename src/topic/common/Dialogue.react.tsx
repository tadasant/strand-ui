import * as React from 'react'
import {Component} from 'react';
import MessageTile from './MessageTile.react';
import GridList from 'material-ui/GridList';
import GridListTile from 'material-ui/GridList';
import Divider from 'material-ui/Divider';
import MessageTileMinimal from './MessageTileMinimal.react';
import {GetTopicMessageFragment} from '../../../schema/graphql-types';

interface PropTypes {
  messages: GetTopicMessageFragment[]
  minimal?: boolean
}

class Dialogue extends Component<PropTypes> {
  render() {
    const messageComponentType = this.props.minimal ? MessageTileMinimal : MessageTile;
    return (
      <GridList
        cellHeight='auto'
        cols={1}>
        {this.props.messages.map(((message, i) => (
          <GridListTile key={i} style={{overflow: 'hidden'}}>
            {React.createElement(messageComponentType, {message})}
            {i === this.props.messages.length - 1 ? <div /> : <Divider style={{margin: '0.5vh', width: 'unset', height: 'unset', padding: 'unset'}}/>}
          </GridListTile>
        )))}
      </GridList>
    );
  }
}

export default Dialogue;
