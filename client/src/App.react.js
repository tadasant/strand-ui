import React, {Fragment} from 'react';
import Shell from './shell/Shell.react';
import Route from 'react-router-dom/Route';
import Redirect from 'react-router-dom/Redirect';
import Switch from 'react-router-dom/Switch';

const App = () => (
  <Fragment>
    <Shell/>
    <Switch>
      <Route path='/install' component={Shell}/>
      <Redirect from='/' to='/install'/>
    </Switch>
  </Fragment>
);

export default App;
