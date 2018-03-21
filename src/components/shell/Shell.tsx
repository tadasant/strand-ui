import * as React from 'react';
import {Component} from 'react';

import ShellDesktop from './rwd/ShellDesktop';
import ShellMobile from './rwd/ShellMobile';
import {RouteComponentProps, withRouter} from 'react-router-dom';
import Hidden from 'material-ui/Hidden/Hidden';
import {ReferenceMeFragment} from '../../../schema/graphql-types';

interface PropTypes extends RouteComponentProps<any> {
  currentUser?: ReferenceMeFragment
}

class Shell extends Component<PropTypes> {
  constructor(props: PropTypes) {
    super(props);

    this.openPageGenerator = this.openPageGenerator.bind(this);
  }

  openPageGenerator(endpoint: string) {
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
          <ShellDesktop openPageGenerator={this.openPageGenerator} currentUser={this.props.currentUser}/>
        </Hidden>
      </div>
    );
  }
}

export default withRouter<PropTypes>(Shell);