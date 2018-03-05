import * as React from 'react';
import {Component} from 'react';
import consts from '../common/MenuConstants';
import StrandLogo from '../common/StrandLogo.react';
import AppBar from 'material-ui/AppBar/AppBar';
import Toolbar from 'material-ui/Toolbar/Toolbar';
import Button from 'material-ui/Button/Button';

interface PropTypes {
  openPageGenerator: Function,
}

class ShellDesktop extends Component<PropTypes> {
  render() {
    return (
      <div>
        <AppBar position='fixed'>
          <Toolbar style={{height: '56px'}}>
            <StrandLogo style={{height: '75%'}}/>
            {Object.keys(consts.navigationLabelToPath).map((label, i) => (
              <Button
                id={`${consts.navigationLabelToPath[label]}-button`}
                style={i == 0 ? {marginLeft: 'auto'} : undefined}
                key={label}
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

export default ShellDesktop;
