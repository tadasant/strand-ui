import React, {Component} from 'react';
import PropTypes from 'prop-types';

const propTypes = {
  size: PropTypes.string,
  redirectUri: PropTypes.string.isRequired,
};

class AddToSlackButton extends Component {
  render() {
    const src = `https://platform.slack-edge.com/img/add_to_slack${this.props.size === 'large' ? '@2x' : null}.png`;
    const slackClientId = this.context.slackClientId; // From config (see index.tsx)
    const queryParams = [
      `client_id=${slackClientId}`,
      `scope=${process.env.SLACK_SCOPES}`,
      `redirect_uri=${this.props.redirectUri}`,
    ];
    const button_url = `https://slack.com/oauth/authorize?${queryParams.join('&')}`;
    return (
      <a id='add-to-slack-button' href={button_url}>
        <img alt='Add to Slack' height='40' width='139' src={src}/>
      </a>
    );
  }
}

AddToSlackButton.defaultProps = {
  size: 'large',
};

AddToSlackButton.propTypes = propTypes;

AddToSlackButton.contextTypes = {
  slackClientId: PropTypes.string.isRequired,
};

export default AddToSlackButton;