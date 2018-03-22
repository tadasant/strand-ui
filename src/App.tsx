import * as React from 'react';
import {Component, Fragment} from 'react';
import {Redirect, Route, RouteComponentProps, Switch} from 'react-router';
import Shell from './components/shell/Shell';
import Install from './components/install/Install';
import StrandListViewContainer from './components/strands/StrandListViewContainer';
import {GET_REFERENCE_DATA_QUERY, GET_STRAND_LIST_QUERY} from '../schema/graphql-queries';
import {
  GetReferenceDataQuery, GetStrandListQuery, ReferenceMeFragment, ReferenceTagsFragment,
  ReferenceUsersFragment
} from '../schema/graphql-types';
import {graphql} from 'react-apollo';
import {get} from 'lodash';
import {filterFalsey} from './components/common/utilities';
import 'react-select/dist/react-select.css';
import StrandDetailViewContainer from './components/strand/StrandDetailViewContainer';
import Login from './components/login/LoginContainer';

interface PropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
  currentUser?: ReferenceMeFragment,
}

class App extends Component<PropTypes> {
  render() {
    return (
      <Fragment>
        <Shell currentUser={this.props.currentUser}/>
        <Switch>
          <Route exact path='/strands' render={() => <StrandListViewContainer tags={this.props.tags} users={this.props.users}/>} />
          <Route exact path='/strands/:id' render={(props: RouteComponentProps<{id: string}>) => <StrandDetailViewContainer strandId={props.match.params.id}/>}/>
          <Route exact path='/install' component={Install}/>
          <Route exact path='/login' component={Login}/>
          <Redirect from='/' to='/strands'/>
        </Switch>
      </Fragment>
    )
  }
}

const withReferenceData = graphql<GetReferenceDataQuery>(GET_REFERENCE_DATA_QUERY, {
  options: {
    errorPolicy: 'all',
  } as any // TODO Apollo types bug. Should be fixed with next npm release of react-apollo (>2.0.4).
});

export default withReferenceData(({data}) => {
  const tags = filterFalsey(get(data, 'tags') || []);
  const users = filterFalsey(get(data, 'users') || []);
  return <App tags={tags} users={users} currentUser={get(data, 'me') || undefined}/>
})
