import * as React from 'react';
import {Component} from 'react'
import Typography from 'material-ui/Typography/Typography'

interface PropTypes {
  installingSlackApplication: boolean,
  successInstallationSlackApplication?: boolean,
  errors: string[],
}

class InstallationStatus extends Component<PropTypes> {
  renderSuccess() {
    return (
      <Typography variant='subheading' style={{color: 'green'}}>
        {'Successfully installed! The Strand bot should have DM\'d you with setup instructions.'}
      </Typography>
    )
  }

  renderFailure() {
    return (
      <Typography variant='subheading' style={{color: 'red'}}>
        Failed to install.<br/>Errors:&nbsp;
        {this.props.errors.length > 0 ? this.props.errors.join('; ') : 'Please contact support@solutionloft.com'}
      </Typography>
    )
  }

  renderInstalling() {
    return <Typography variant='subheading' style={{color: 'green'}}>Installing...</Typography>
  }

  render() {
    if (this.props.installingSlackApplication) {
      return this.renderInstalling()
    }
    return this.props.successInstallationSlackApplication ? this.renderSuccess() : this.renderFailure()
  }
}

export default InstallationStatus