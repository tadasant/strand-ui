import * as React from 'react';
import {Component, Fragment} from 'react';
import {Redirect, Route, RouteComponentProps, RouteProps, Switch} from 'react-router';
import Shell from './shell/Shell';
import Install from './install/Install';
import StrandsViewContainer from './strands/StrandListViewContainer';
import {GET_REFERENCE_DATA_QUERY} from '../schema/graphql-queries';
import {GetReferenceDataQuery, ReferenceTagsFragment, ReferenceUsersFragment} from '../schema/graphql-types';
import {graphql} from 'react-apollo';
import {get} from 'lodash';
import {filterFalsey} from './common/utilities';
import 'react-select/dist/react-select.css';
import StrandViewContainer from './strand/StrandDetailViewContainer';

interface PropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

class App extends Component<PropTypes> {
  render() {
    return (
      <Fragment>
        <Shell/>
        <Switch>
          <Route exact path='/strands' render={() => <StrandsViewContainer tags={this.props.tags} users={this.props.users}/>} />
          <Route exact path='/strands/:id' render={(props: RouteComponentProps<{id: string}>) => <StrandViewContainer strandId={props.match.params.id}/>}/>
          <Route exact path='/install' component={Install}/>
          <Redirect from='/' to='/strands'/>
        </Switch>
      </Fragment>
    )
  }
}

const withReferenceData = graphql<GetReferenceDataQuery>(GET_REFERENCE_DATA_QUERY);

export default withReferenceData(({data}) => {
  const tags = filterFalsey(get(data, 'tags') || []);
  const users = filterFalsey(get(data, 'users') || []);
  return <App tags={tags} users={users}/>
})
