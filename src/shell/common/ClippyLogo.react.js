import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import logoWithText from '../../../assets/strand_darktext.png';
import logo from '../../../assets/strand.png';
import PropTypes from 'prop-types';

const propTypes = {
  omitText: PropTypes.bool,
  style: PropTypes.object,
};

class StrandLogo extends Component {
  render() {
    return (
      <Link to='/' style={this.props.style}>
        <img
          alt='strand-logo'
          src={this.props.omitText ? logo : logoWithText}
          style={{height: '100%', verticalAlign: 'middle'}}
        />
      </Link>
    )
  }
}

StrandLogo.propTypes = propTypes;

export default StrandLogo;