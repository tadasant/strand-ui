import * as React from 'react';
import {StatelessComponent} from 'react';
import Grid from 'material-ui/Grid/Grid';
import Paper from 'material-ui/Paper';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import CircularProgress from 'material-ui/Progress/CircularProgress';

interface PropTypes {
  onEmailChange: React.ChangeEventHandler<HTMLInputElement>
  onPasswordChange: React.ChangeEventHandler<HTMLInputElement>
  onLoginClick: () => void
  email: string
  password: string
  isLoggingIn: boolean
}

const Login: StatelessComponent<PropTypes> = props => (
  <Grid container>
    <Grid item xs/>
    <Grid item xs={6}>
      <Paper>
        <Grid container>
          <Grid item xs/>
          <Grid item xs={8}>
            <Grid container>
              <TextField
                id='email-field'
                label='Email'
                autoFocus
                onChange={props.onEmailChange}
                required
                fullWidth
                value={props.email}
                margin='normal'
                type='email'
              />
              <TextField
                id='password-field'
                label='Password'
                type='password'
                fullWidth
                onChange={props.onPasswordChange}
                required
                value={props.password}
                margin='normal'
              />
              <Grid container>
                <Grid item xs/>
                <Grid item xs={12} sm={8}>
                  <Button
                    id='login-button'
                    onClick={props.onLoginClick}
                    color='inherit'
                    variant='raised'
                    disabled={props.isLoggingIn}
                    style={{margin: '10% 0 10% 0'}}
                    fullWidth>
                    Login
                    {props.isLoggingIn ? <CircularProgress /> : null}
                  </Button>
                </Grid>
                <Grid item xs/>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs/>
        </Grid>
      </Paper>
    </Grid>
    <Grid item xs/>
  </Grid>
);

export default Login;
