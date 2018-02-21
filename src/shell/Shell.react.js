import React, {Component} from 'react';
import PropTypes from 'prop-types';

import ShellDesktop from './rwd/ShellDesktop.react';
import ShellMobile from './rwd/ShellMobile.react';
import withRouter from 'react-router-dom/withRouter';
import Hidden from 'material-ui/Hidden/Hidden';

const propTypes = {
  // from withRouter
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
};

class Shell extends Component {
  constructor(props) {
    super(props);

    this.openPageGenerator = this.openPageGenerator.bind(this);
  }

  openPageGenerator(endpoint) {
    return () => {
      this.props.history.push(endpoint);
    }
  }

  render() {
    return (
      <div>
        <Hidden mdUp>
          <ShellMobile openPageGenerator={this.openPageGenerator}/>
        </Hidden>
        <Hidden smDown>
          <ShellDesktop openPageGenerator={this.openPageGenerator}/>
        </Hidden>
      </div>
    );
  }
}

Shell.propTypes = propTypes;

export default withRouter(Shell);
