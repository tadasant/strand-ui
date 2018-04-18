import * as React from 'react';
import {Component, ReactInstance} from 'react';
import {findDOMNode} from 'react-dom';
import consts from '../common/MenuConstants';
import StrandLogo from '../common/StrandLogo';
import AppBar from 'material-ui/AppBar/AppBar';
import Popover from 'material-ui/Popover/Popover';
import MenuItem from 'material-ui/Menu/MenuItem';
import IconButton from 'material-ui/IconButton/IconButton';
import Toolbar from 'material-ui/Toolbar/Toolbar';
import MenuIcon from 'material-ui-icons/Menu';
import {ReferenceMeFragment} from '../../../../schema/graphql-types';
import Typography from 'material-ui/Typography';

interface PropTypes {
  openPageGenerator: Function,
  currentUser?: ReferenceMeFragment
}

interface StateTypes {
  showNavMenu: boolean,
  menuIconAnchor?: HTMLElement,
}

class ShellMobile extends Component<PropTypes, StateTypes> {
  // Used to store a ref to the menu button
  private menuButtonNode?: ReactInstance;

  constructor(props: PropTypes) {
    super(props);

    this.state = {
      showNavMenu: false,
      menuIconAnchor: undefined,
    };
    this.menuButtonNode = undefined;
    this.openNavMenu = this.openNavMenu.bind(this);
    this.handleCloseNavMenu = this.handleCloseNavMenu.bind(this);
    this.generateHandleClickNavMenuItem = this.generateHandleClickNavMenuItem.bind(this);
  }

  openNavMenu() {
    this.setState(prevState => ({
      showNavMenu: !prevState.showNavMenu,
      menuIconAnchor: this.menuButtonNode ? findDOMNode(this.menuButtonNode) as HTMLElement : undefined,
    }));
  }

  handleCloseNavMenu() {
    this.setState({showNavMenu: false});
  }

  generateHandleClickNavMenuItem(openPage: Function) {
    return () => {
      this.handleCloseNavMenu();
      openPage();
    }
  }

  render() {
    const navigationLabelToPath = this.props.currentUser
      ? consts.loggedInNavigationLabelToPath
      : consts.navigationLabelToPath;
    return (
      <div>
        <AppBar position='fixed'>
          <Toolbar style={{margin: 'auto', height: '56px'}}>
            <StrandLogo omitText style={{height: '75%'}}/>
            {
              this.props.currentUser
                ? <Typography variant='caption' style={{marginLeft: '1%'}}>
                  {this.props.currentUser.email}
                </Typography>
                : null
            }
            <IconButton
              buttonRef={(node) => this.menuButtonNode = node as ReactInstance}
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
              {Object.keys(navigationLabelToPath).map(label => (
                <MenuItem
                  key={label}
                  onClick={
                    this.generateHandleClickNavMenuItem(this.props.openPageGenerator(navigationLabelToPath[label]))
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

export default ShellMobile;