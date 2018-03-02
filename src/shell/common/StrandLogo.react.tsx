import * as React from 'react';
import {Component} from 'react';
import {Link} from 'react-router-dom';
import * as logoWithText from '../../../assets/strand_darktext.png';
import * as logo from '../../../assets/strand.png';

interface PropTypes {
  omitText?: boolean,
  style?: {}
}

class StrandLogo extends Component<PropTypes> {
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

export default StrandLogo;