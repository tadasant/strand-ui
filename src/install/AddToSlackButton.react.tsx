import * as React from 'react';
import {Component} from 'react';
import * as CONFIG from '../config';

interface PropTypes {
  size?: string,
  redirectUri: string,
}

class AddToSlackButton extends Component<PropTypes> {
  public static defaultProps: Partial<PropTypes> = {
    size: 'large',
  };

  render() {
    const src = `https://platform.slack-edge.com/img/add_to_slack${this.props.size === 'large' ? '@2x' : null}.png`;
    const queryParams = [
      `client_id=${CONFIG.SLACK_CLIENT_ID}`,
      `scope=${CONFIG.SLACK_SCOPES}`,
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

export default AddToSlackButton;
