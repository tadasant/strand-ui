import * as React from 'react';
import {Component} from 'react';
import {Redirect, Route, RouteComponentProps, Switch} from 'react-router';
import Shell from './components/shell/Shell';
import Install from './components/install/Install';
import StrandListViewContainer from './components/strands/StrandListViewContainer';
import {GET_REFERENCE_DATA_QUERY} from '../schema/graphql-queries';
import {
  GetReferenceDataQuery, ReferenceMeFragment, ReferenceTagsFragment,
  ReferenceUsersFragment
} from '../schema/graphql-types';
import {graphql} from 'react-apollo';
import {get} from 'lodash';
import {filterFalsey} from './components/common/utilities';
import 'react-select/dist/react-select.css';
import StrandDetailViewContainer from './components/strand/StrandDetailViewContainer';
import Login from './components/login/LoginContainer';
import {CookiesProvider} from 'react-cookie';

interface PropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
  currentUser?: ReferenceMeFragment,
}

class App extends Component<PropTypes> {
  render() {
    return (
      <CookiesProvider>
        <Shell currentUser={this.props.currentUser}/>
        <Switch>
          <Route exact path='/strands' render={() => <StrandListViewContainer tags={this.props.tags} users={this.props.users}/>} />
          <Route exact path='/strands/:id' render={(props: RouteComponentProps<{id: string}>) => <StrandDetailViewContainer strandId={props.match.params.id}/>}/>
          <Route exact path='/install' component={Install}/>
          <Route exact path='/login' component={Login}/>
          <Redirect from='/' to='/strands'/>
        </Switch>
      </CookiesProvider>
    )
  }
}

const withReferenceData = graphql<GetReferenceDataQuery>(GET_REFERENCE_DATA_QUERY);

export default withReferenceData(({data}) => {
  const tags = filterFalsey(get(data, 'tags') || []);
  const users = filterFalsey(get(data, 'users') || []);
  return <App tags={tags} users={users} currentUser={get(data, 'me') || undefined}/>
})
