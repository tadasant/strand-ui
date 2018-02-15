import React, {Component} from 'react';
import PropTypes from 'prop-types';

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
    if (this.state.error && Raven.isSetup()) {
      return (
        <div
          className='snap'
          onClick={() => Raven.lastEventId() && Raven.showReportDialog()}>
          <p>Sorry! Something went wrong.</p>
          <p>Our team has been notified, but click here fill out a report.</p>
        </div>
      );
    } else {
      return this.props.children;
    }
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.object,
};

export default ErrorBoundary;
