import * as React from 'react';
import {ChangeEvent, Component} from 'react';
import Login from './Login';
import {RouteComponentProps, withRouter} from 'react-router';
import {withCookies} from 'react-cookie';
import {CookieComponentProps} from 'react-cookie';
import {withApollo} from 'react-apollo';
import ApolloClient from 'apollo-client/ApolloClient';
import {AUTH_COOKIE_NAME} from '../../config';

// No explicit types available for withApollo at time of writing
interface ApolloProps {
  client: ApolloClient<any>
}

interface PropTypes extends RouteComponentProps<any>, CookieComponentProps, ApolloProps {
}

interface StateTypes {
  email: string,
  password: string,
  isLoggingIn: boolean,
}

class LoginContainer extends Component<PropTypes, StateTypes> {
  constructor(props: PropTypes) {
    super(props);

    this.state = {
      email: '',
      password: '',
      isLoggingIn: false,
    };

    this.handleLoginClick = this.handleLoginClick.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  handleLoginClick() {
    this.setState({isLoggingIn: true}, () => {
      if (!this.props.cookies) {
        // TODO abort and propogate error [UI-61]
      }
      global.strandApiClient.login(this.state.email, this.state.password)
        .then(response => {
          const token = response.data.token;
          console.log(token);
          this.props.cookies!.set(AUTH_COOKIE_NAME, token, {httpOnly: false});
          this.props.client.resetStore();
          this.setState({isLoggingIn: false});
          this.props.history.push('/strands')
        })
        .catch(errors => {
          console.log(errors);
          // TODO propogate errors [UI-61]
          this.setState({isLoggingIn: false});
        });
    });
  }

  handleEmailChange(event: ChangeEvent<HTMLInputElement>) {
    const email = event.target.value;
    this.setState({email});
  }

  handlePasswordChange(event: ChangeEvent<HTMLInputElement>) {
    const password = event.target.value;
    this.setState({password});
  }

  render() {
    return (
      <Login
        onEmailChange={this.handleEmailChange}
        onPasswordChange={this.handlePasswordChange}
        onLoginClick={this.handleLoginClick}
        {...this.state}
      />
    );
  }
}

export default withApollo(withRouter<PropTypes>(withCookies(LoginContainer)));
