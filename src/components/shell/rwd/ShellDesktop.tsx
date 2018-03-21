import * as React from 'react';
import {Component} from 'react';
import consts from '../common/MenuConstants';
import StrandLogo from '../common/StrandLogo';
import AppBar from 'material-ui/AppBar/AppBar';
import Toolbar from 'material-ui/Toolbar/Toolbar';
import Button from 'material-ui/Button/Button';
import Typography from 'material-ui/Typography';
import {ReferenceMeFragment} from '../../../../schema/graphql-types';

interface PropTypes {
  openPageGenerator: Function,
  currentUser?: ReferenceMeFragment
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
            {
              this.props.currentUser
                ? <Typography align='right' variant='caption' style={{marginLeft: '1%'}}>
                    {this.props.currentUser.email}
                  </Typography>
                : null
            }
          </Toolbar>
        </AppBar>
        <div style={{paddingTop: '100px'}}/>
      </div>
    )
  }
}

export default ShellDesktop;
