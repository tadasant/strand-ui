import * as React from 'react';
import {Fragment, SFC} from 'react';
import {Route, Redirect, Switch} from 'react-router';
import Shell from './shell/Shell.react';
import Install from './install/Install.react';

const App: SFC = () => (
  <Fragment>
    <Shell/>
    <Switch>
      <Route path='/install' component={Install}/>
      <Redirect from='/' to='/install'/>
    </Switch>
  </Fragment>
);

export default App;