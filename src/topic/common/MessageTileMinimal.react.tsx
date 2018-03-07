import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import {GetTopicMessageFragment} from '../../../schema/graphql-types';

interface PropTypes {
  message: GetTopicMessageFragment
}

class MessageTileMinimal extends Component<PropTypes> {
  render() {
    return (
      <Grid
        container
        direction='row'
        spacing={0}
        style={{padding: '2% 2% 2% 2%'}}
        alignItems='stretch'>
        <Grid item xs={2}>
          <Grid container>
            <Grid item style={{maxWidth: '100%'}}>
              <Typography
                variant='body1'
                style={{overflow: 'hidden', textOverflow: 'ellipsis'}}>
                {/*TODO [UI-50] no nulls in graphql to eliminate !'s*/}
                {this.props.message.author!.alias}
              </Typography>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={10}>
          <Typography
            variant='caption'>
            <div dangerouslySetInnerHTML={{__html: this.props.message.text}}/>
          </Typography>
        </Grid>
      </Grid>
    );
  }
}

export default MessageTileMinimal;
