import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {AppBar, Button, Toolbar} from 'material-ui';
import 'typeface-roboto';
import consts from '../common/MenuConstants';
import ClippyLogo from '../common/ClippyLogo.react';

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
