import * as React from 'react';
import StrandsView from './StrandListView';
import {GET_STRAND_LIST_QUERY} from '../../../schema/graphql-queries';
import {GetStrandListQuery, ReferenceTagsFragment, ReferenceUsersFragment} from '../../../schema/graphql-types';
import {graphql} from 'react-apollo';
import {filterFalsey} from '../common/utilities';
import CircularProgress from 'material-ui/Progress/CircularProgress';

interface StaticPropTypes {
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

const withStrands = graphql<GetStrandListQuery, StaticPropTypes>(GET_STRAND_LIST_QUERY, {
  options: {
    'errorPolicy': 'all', // Returns partial data
  } as any // TODO Apollo types bug. Should be fixed with next npm release of react-apollo (>2.0.4).
});

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
// Right now we're just ignoring any graphql errors
const StrandsViewContainer = withStrands(({data, tags, users}) => {
  if (data && data.loading) return <CircularProgress/>;
  if (!data || !data.strands) {
    return <h1>{`ERROR ${data && data.error && data.error.message || ''}`}</h1>
  }
  const nonNullStrands = filterFalsey(data.strands);
  return <StrandsView strands={nonNullStrands} tags={tags} users={users}/>
});

export default StrandsViewContainer;
