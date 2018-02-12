import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {findDOMNode} from 'react-dom';
import 'typeface-roboto';
import consts from '../common/MenuConstants';
import ClippyLogo from '../common/ClippyLogo.react';
import AppBar from 'material-ui/AppBar/AppBar';
import Popover from "material-ui/Popover/Popover";
import MenuItem from 'material-ui/Menu/MenuItem';
import IconButton from 'material-ui/IconButton/IconButton';
import Toolbar from 'material-ui/Toolbar/Toolbar';
import MenuIcon from 'material-ui-icons/Menu';

const propTypes = {
  openPageGenerator: PropTypes.func.isRequired,
};

class ShellMobile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showNavMenu: false,
      menuIconAnchor: null,
    };
    this.menuButtonNode = null;
    this.openNavMenu = this.openNavMenu.bind(this);
    this.handleCloseNavMenu = this.handleCloseNavMenu.bind(this);
    this.generateHandleClickNavMenuItem = this.generateHandleClickNavMenuItem.bind(this);
  }

  openNavMenu() {
    this.setState(prevState => ({
      showNavMenu: !prevState.showNavMenu,
      menuIconAnchor: findDOMNode(this.menuButtonNode),
    }));
  }

  handleCloseNavMenu() {
    this.setState({showNavMenu: false});
  }

  generateHandleClickNavMenuItem(openPage) {
    return () => {
      this.handleCloseNavMenu();
      openPage();
    }
  }

  render() {
    return (
      <div>
        <AppBar position='fixed'>
          <Toolbar style={{margin: 'auto', height: '56px'}}>
            <ClippyLogo omitText style={{height: '75%'}}/>
            <IconButton
              ref={(node) => this.menuButtonNode = node}
              color='secondary'
              aria-label='Menu'
              onClick={this.openNavMenu}
              style={{width: 'unset'}}
              disableRipple>
              <MenuIcon/>
            </IconButton>
            <Popover
              open={this.state.showNavMenu}
              anchorEl={this.state.menuIconAnchor}
              anchorReference='anchorEl'
              onClose={this.handleCloseNavMenu}
              onExited={this.handleCloseNavMenu}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'center',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}>
              {Object.keys(consts.navigationLabelToPath).map(label => (
                <MenuItem
                  key={label}
                  onClick={
                    this.generateHandleClickNavMenuItem(this.props.openPageGenerator(consts.navigationLabelToPath[label]))
                  }>
                  {label}
                </MenuItem>
              ))}
            </Popover>
          </Toolbar>
        </AppBar>
        <div style={{paddingTop: '75px'}}/>
      </div>
    )
  }
}

ShellMobile.propTypes = propTypes;

export default ShellMobile;
