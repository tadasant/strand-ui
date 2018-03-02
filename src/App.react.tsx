import * as React from 'react';
import {Fragment, StatelessComponent} from 'react';
import {Redirect, Route, Switch} from 'react-router';
import Shell from './shell/Shell.react';
import Install from './install/Install.react';
import TopicsViewContainer from './topics/TopicsViewContainer.react';

const App: StatelessComponent = () => (
  <Fragment>
    <Shell/>
    <Switch>
      <Route path='/topics' component={TopicsViewContainer}/>
      <Route path='/install' component={Install}/>
      <Redirect from='/' to='/topics'/>
    </Switch>
  </Fragment>
);

export default App;