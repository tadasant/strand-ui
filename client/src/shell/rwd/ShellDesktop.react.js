import React, {Component} from 'react';
import PropTypes from 'prop-types';
import consts from '../common/MenuConstants';
import ClippyLogo from '../common/ClippyLogo.react';
import AppBar from 'material-ui/AppBar/AppBar';
import Toolbar from 'material-ui/Toolbar/Toolbar';
import Button from 'material-ui/Button/Button';

const propTypes = {
  openPageGenerator: PropTypes.func.isRequired,
};

class ShellDesktop extends Component {
  render() {
    return (
      <div>
        <AppBar position='fixed'>
          <Toolbar style={{height: '56px'}}>
            <ClippyLogo style={{height: '75%'}}/>
            {Object.keys(consts.navigationLabelToPath).map(label => (
              <Button
                style={{marginLeft: 'auto'}}
                key={label}
                color='secondary'
                onClick={this.props.openPageGenerator(consts.navigationLabelToPath[label])}>
                {label}
              </Button>
            ))}
          </Toolbar>
        </AppBar>
        <div style={{paddingTop: '100px'}}/>
      </div>
    )
  }
}

ShellDesktop.propTypes = propTypes;

export default ShellDesktop;
