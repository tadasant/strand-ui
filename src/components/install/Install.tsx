import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid/Grid';
import Typography from 'material-ui/Typography/Typography';
import withStyles from 'material-ui/styles/withStyles';
import * as queryString from 'query-string';
import {RouteComponentProps, withRouter} from 'react-router-dom';
import * as Raven from 'raven-js';
import InstallationStatus from './InstallationStatus';
import AddToSlackButton from './AddToSlackButton';
import * as CONFIG from '../../config';

import {StyleRules, Theme, WithStyles} from 'material-ui/styles';
import {InstallationResponseData} from '../../clients/StrandSlackClient';

const styles = (theme: Theme): StyleRules => ({
  body1: theme.typography.body1,
});

interface PropTypes extends WithStyles, RouteComponentProps<any> {
  attemptInstall: Function,
  classes: {
    body1: string,
  },
}

interface StateTypes {
  installingSlackApplication: boolean,
  successInstallationSlackApplication?: boolean,
  error?: string,
}

class Install extends Component<PropTypes, StateTypes> {
  private redirectUri: string;

  constructor(props: PropTypes) {
    super(props);

    this.redirectUri = `${CONFIG.UI_HOST}${props.location.pathname}`;

    this.state = {
      installingSlackApplication: false,
      successInstallationSlackApplication: undefined, // true/false after attempt
      error: undefined,
    }
  }

  componentDidMount() {
    const params = queryString.parse(this.props.location.search);
    if (params.code) {
      this.setState(() => ({installingSlackApplication: true}), () => {
        global.strand_slack_client.installApplication(params.code)
          .then(() => {
            this.setState(() => ({
              installingSlackApplication: false,
              successInstallationSlackApplication: true,
            }));
          })
          .catch((response: InstallationResponseData) => {
            // TODO refactor this out as we start using it in other places
            debugger;
            if (Raven.isSetup()) {
              Raven.captureException(Error(`Installation error: ${JSON.stringify(response)}`));
            }
            this.setState(() => ({
              installingSlackApplication: false,
              successInstallationSlackApplication: false,
              error: response.error,
            }));
          })
      })
    }
  }

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
                Installing Strand in Your Slack Workspace
              </Typography>
            </Grid>
            <Grid item>
              <Typography variant='body1'>
                Use Strand to have more productive discussions in Slack. Strand makes discussions more focused&nbsp;
                and easier to share with your team. Please be aware that:
              </Typography>
              <div className={this.props.classes.body1}>
                <ul>
                  <li>You need to be an <u>admin</u> in your Workspace to add Strand</li>
                  <li>
                    Strand will soon be able to store your transcripts online to make them easier to search and&nbsp;
                    share with your teammates. Therefore, Strand stores the conversations that it participates in.&nbsp;
                    These are never reviewed by a human and the feature will be opt-in once released, but we&nbsp;
                    prefer to be transparent about it.
                  </li>
                </ul>
              </div>
            </Grid>
            <Grid item>
              <AddToSlackButton redirectUri={this.redirectUri}/>
              {this.state.successInstallationSlackApplication === undefined && !this.state.installingSlackApplication
                ? null
                : <InstallationStatus
                  installingSlackApplication={this.state.installingSlackApplication}
                  successInstallationSlackApplication={this.state.successInstallationSlackApplication}
                  error={this.state.error}
                />}
            </Grid>
            <Grid item>
              <Typography variant='caption'>
                Not an admin in your workspace?
                Join <a target='_blank' rel='noopener noreferrer' href='https://www.trystrand.com/get-started'>our
                community</a> instead.
              </Typography>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={1}/>
      </Grid>
    );
  }
}

const InstallStyledRouted = withRouter(withStyles(styles)(Install));

export default InstallStyledRouted;
