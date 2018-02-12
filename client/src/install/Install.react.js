import React, {Component} from 'react';
import Grid from 'material-ui/es/Grid/Grid';
import Typography from 'material-ui/es/Typography/Typography';
import AddToSlackButton from './AddToSlackButton.react';

class Install extends Component {
  render() {
    return (
      <Grid
        container
        direction='row'>
        <Grid item xs={1}/>
        <Grid item xs={10}>
          <Grid
            container
            direction='column'
            spacing={16}>
            <Grid item>
              <Typography variant='display1' style={{color: 'rgba(0, 0, 0, 0.87)'}}>
                Installing CodeClippy in Your Slack Workspace
              </Typography>
            </Grid>
            <Grid item>
              <Typography variant='body1'>
                Text bla bla use CodeClippy in your own team to do XYZ. Make sure you are:
              </Typography>
              <ul>
                <li>Something</li>
                <li>Admin</li>
                <li>Sensitive Info</li>
              </ul>
              <Typography variant='body1'>
                If all good, click below to install.
              </Typography>
            </Grid>
            <Grid item>
              <AddToSlackButton />
            </Grid>
            <Grid item>
              <Typography variant='caption'>
                Not an admin in your workspace?
                Join <a target='_blank' href='https://www.codeclippy.com/get-started'>our community</a> instead.
              </Typography>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={1}/>
      </Grid>
    );
  }
}

export default Install;
