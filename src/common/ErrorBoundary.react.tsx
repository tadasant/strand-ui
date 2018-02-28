import {Component} from 'react';
import * as Raven from 'raven-js';

interface PropTypes {
  children: object,
}

class ErrorBoundary extends Component<PropTypes> {
  constructor(props) {
    super(props);
    this.state = {error: null};
  }

  componentDidCatch(error, errorInfo) {
    if (Raven.isSetup()) {
      this.setState({error});
      Raven.captureException(error, {extra: errorInfo});
    }
  }

  render() {
    // TODO could add a nice "there was an error, help us out" kind of screen here
    return this.props.children;
  }
}

export default ErrorBoundary;
