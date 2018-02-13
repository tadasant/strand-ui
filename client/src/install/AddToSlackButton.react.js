import React, {Component} from 'react';
import PropTypes from 'prop-types';
import withRouter from 'react-router-dom/es/withRouter';

const propTypes = {
  size: PropTypes.string,
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
};

class AddToSlackButton extends Component {
  render() {
    const redirectHost = this.context.uiHost; // From config (see index.js)
    const src = `https://platform.slack-edge.com/img/add_to_slack${this.props.size === 'large' ? '@2x' : null}.png`;
    const queryParams = [
      `client_id=${process.env.SLACK_CLIENT_ID}`,
      `scope=${process.env.SLACK_SCOPES}`,
      `redirect_uri=${redirectHost}${this.props.location.pathname}`,
    ];
    const button_url = `https://slack.com/oauth/authorize?${queryParams.join('&')}`;
    return (
      <a href={button_url}>
        <img alt="Add to Slack" height="40" width="139" src={src} />
      </a>
    );
  }
}

AddToSlackButton.defaultProps = {
  size: 'large',
};

AddToSlackButton.contextTypes = {
  uiHost: PropTypes.string.isRequired,
};

AddToSlackButton.propTypes = propTypes;

export default withRouter(AddToSlackButton);
