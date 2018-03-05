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
import 'react-select/dist/react-select.css';

interface PropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

class App extends Component<PropTypes> {
  generateTopicsViewContainer(): React.ComponentType<any> {
    return (routeProps: RouteProps) => {
      return (
        <TopicsViewContainer
          {...routeProps}
          tags={this.props.tags}
          users={this.props.users}
        />
      )
    }
  }

  render() {
    return (
      <Fragment>
        <Shell/>
        <Switch>
          <Route path='/topics' component={this.generateTopicsViewContainer()}/>
          <Route path='/install' component={Install}/>
          <Redirect from='/' to='/topics'/>
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
