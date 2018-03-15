import * as React from 'react';
import StrandView from './StrandDetailView';
import {GET_STRAND_DETAIL_QUERY} from '../../schema/graphql-queries';
import {graphql} from 'react-apollo';
import {GetStrandDetailQuery} from '../../schema/graphql-types';
import CircularProgress from 'material-ui/Progress/CircularProgress';

interface PropTypes {
  strandId: string,
}

const withStrand = graphql<GetStrandDetailQuery, PropTypes>(GET_STRAND_DETAIL_QUERY, {
  options: (props) => ({
    variables: {id: props.strandId},
    'errorPolicy': 'all', // Returns partial data
  } as any) // TODO Apollo types bug. Should be fixed with next npm release of react-apollo (>2.0.4).
});

// TODO consider splitting this larger query into smaller ones in subcomponents (what's best practice?)
// Right now we're just ignoring any graphql errors
const StrandViewContainer = withStrand(({data}) => {
  if (data && data.loading) return <CircularProgress/>;
  if (!data || !data.strand) {
    return <h1>{`ERROR ${data && data.error && data.error.message || ''}`}</h1>
  }
  return <StrandView strand={data.strand}/>
});

export default StrandViewContainer;
