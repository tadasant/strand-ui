import * as React from 'react';
import {Component, Fragment} from 'react';
import {Redirect, Route, RouteProps, Switch} from 'react-router';
import Shell from './shell/Shell.react';
import Install from './install/Install.react';
import TopicsViewContainer from './topics/TopicsViewContainer.react';
import {GET_REFERENCE_DATA_QUERY} from '../schema/graphql-queries';
import {GetReferenceDataQuery, ReferenceTagsFragment, ReferenceUsersFragment} from '../schema/graphql-types';
import {graphql} from 'react-apollo';
import {get} from 'lodash';
import {filterFalsey} from './common/utilities';

interface PropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

class App extends Component<PropTypes> {
  generateTopicsViewContainer(tags: ReferenceTagsFragment[]) {
    return (routeProps: RouteProps) => {
      return (
        <TopicsViewContainer
          {...routeProps}
          tags={tags}
          users={this.props.users}
        />
      )
    }
  }

  render() {
    const tags = this.props.tags;
    return (
      <Fragment>
        <Shell/>
        <Switch>
          <Route path='/topics' component={this.generateTopicsViewContainer(tags)}/>
          <Route path='/install' component={Install}/>
          <Redirect from='/' to='/topics'/>
        </Switch>
      </Fragment>
    )
  }
}

const withReferenceData = graphql<GetReferenceDataQuery>(GET_REFERENCE_DATA_QUERY);

export default withReferenceData(({data}) => {
  const tags = filterFalsey(get(data, 'tags', [])!);
  const users = filterFalsey(get(data, 'users', [])!);
  return <App tags={tags} users={users}/>
})
