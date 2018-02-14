import React, {Component} from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  size: PropTypes.string,
  redirectUri: PropTypes.string.isRequired,
};

class AddToSlackButton extends Component {
  render() {
    const src = `https://platform.slack-edge.com/img/add_to_slack${this.props.size === 'large' ? '@2x' : null}.png`;
    const queryParams = [
      `client_id=${process.env.SLACK_CLIENT_ID}`,
      `scope=${process.env.SLACK_SCOPES}`,
      `redirect_uri=${this.props.redirectUri}`,
    ];
    const button_url = `https://slack.com/oauth/authorize?${queryParams.join('&')}`;
    return (
      <a id='add-to-slack-button' href={button_url}>
        <img alt="Add to Slack" height="40" width="139" src={src}/>
      </a>
    );
  }
}

AddToSlackButton.defaultProps = {
  size: 'large',
};

AddToSlackButton.propTypes = propTypes;

export default AddToSlackButton;
