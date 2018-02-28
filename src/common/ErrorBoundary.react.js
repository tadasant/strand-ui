import {Component} from 'react';
import PropTypes from 'prop-types';
import * as Raven from 'raven-js';

class ErrorBoundary extends Component {
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

ErrorBoundary.propTypes = {
  children: PropTypes.object,
};

export default ErrorBoundary;
