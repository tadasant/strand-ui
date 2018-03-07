import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import {GetTopicMessageFragment} from '../../../schema/graphql-types';

interface PropTypes {
  message: GetTopicMessageFragment
}

class MessageTile extends Component<PropTypes> {
  render() {
    return (
      <Grid
        container>
        <Grid
          item
          xs={1}>
          <img
            style={{display: 'block', margin: 'auto', maxWidth: '100%', maxHeight: '52px'}}
            src='https://ca.slack-edge.com/T9DLEEWCE-U9DLEEXHU-g99ef765ae07-512' // TODO hardcoded image
            alt='profile-pic'
          />
        </Grid>
        <Grid
          item
          xs={11}>
          <Grid
            container
            direction='column'
            alignItems='stretch'>
            <Grid item>
              <Grid container>
                <Grid item>
                  <Typography
                    variant='body1'>
                    {/*TODO [UI-50] no nulls in graphql to eliminate !'s*/}
                    {this.props.message.author!.alias}
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography
                    variant='body1'
                    style={{color: 'lightgrey'}}>
                    {this.props.message.time}
                  </Typography>
                </Grid>
              </Grid>
            </Grid>
            <Grid item>
              <Typography
                variant='caption'>
                <div dangerouslySetInnerHTML={{__html: this.props.message.text}}/>
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

export default MessageTile;
