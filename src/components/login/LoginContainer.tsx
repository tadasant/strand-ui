import * as React from 'react';
import {ChangeEvent, Component} from 'react';
import Login from './Login';
import {RouteComponentProps, withRouter} from 'react-router';

interface PropTypes extends RouteComponentProps<any> {
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
          // TODO store token in cookies [UI-56]
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

export default withRouter<PropTypes>(LoginContainer);
