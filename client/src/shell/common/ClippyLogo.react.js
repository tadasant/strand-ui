import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import 'typeface-roboto';
import logoWithText from '../../../assets/codeclippy_lighttext.png';
import logo from '../../../assets/codeclippy.png';
import PropTypes from 'prop-types';

const propTypes = {
  omitText: PropTypes.bool,
  style: PropTypes.object,
};

class ClippyLogo extends Component {
  render() {
    return (
      <Link to='/' style={this.props.style}>
        <img
          alt='clippy-logo'
          src={this.props.omitText ? logo : logoWithText}
          style={{height: '100%', verticalAlign: 'middle'}}
        />
      </Link>
    )
  }
}

ClippyLogo.propTypes = propTypes;

export default ClippyLogo;
