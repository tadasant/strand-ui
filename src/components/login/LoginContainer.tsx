import * as React from 'react';
import {ChangeEvent, Component} from 'react';
import Login from './Login';
import {RouteComponentProps, withRouter} from 'react-router';
import {withApollo} from 'react-apollo';
import ApolloClient from 'apollo-client/ApolloClient';
import {AUTH_COOKIE_NAME} from '../../config';
import * as Cookies from 'js-cookie';

// No explicit types available for withApollo at time of writing
interface ApolloProps {
  client: ApolloClient<any>
}

interface PropTypes extends RouteComponentProps<any>, ApolloProps {
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
      global.strandApiClient.login(this.state.email, this.state.password)
        .then(response => {
          const token = response.data.token;
          console.log(token);
          if (token) {
            Cookies.set(AUTH_COOKIE_NAME, token);
          }
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

export default withApollo(withRouter<PropTypes>(LoginContainer));
