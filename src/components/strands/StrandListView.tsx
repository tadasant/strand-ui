import * as React from 'react';
import {Component} from 'react';
import {GetStrandListStrandsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../../schema/graphql-types';
import {intersection} from 'lodash';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Hidden from 'material-ui/Hidden';
import StrandsViewDesktop from './rwd/StrandListViewDesktop';
import StrandsViewMobile from './rwd/StrandListViewMobile';
import {ApolloQueryResult} from 'apollo-client';

export interface fetchableVariables {
  query: string,
  page?: number,
  size?: number,
}

interface PropTypes {
  strands: GetStrandListStrandsFragment[],
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
  refetch: (variables?: fetchableVariables) => Promise<ApolloQueryResult<any>>,
}

export type FiltersType = 'tagNames' | 'saverId';
export type FilterValuesType = string[] | number | number[] | void;

export interface FilterTypes {
  tagNames: string[],
  saverId?: string,
}

interface StateTypes {
  filteredStrands: GetStrandListStrandsFragment[],
  filters: FilterTypes,
}

class StrandListView extends Component<PropTypes, StateTypes> {
  constructor(props: PropTypes) {
    super(props);
    // At scale, filters can't be in-memory
    this.state = {
      filteredStrands: [],
      filters: {
        tagNames: [],
        saverId: undefined,
      },
    };

    this.handleChangeFilter = this.handleChangeFilter.bind(this);
    this.handleSearchStrands = this.handleSearchStrands.bind(this);
  }

  componentWillMount() {
    this.updateStateWithProps(this.props);
  }

  updateStateWithProps(props: PropTypes) {
    const filteredStrands = this.applyFiltersToStrands(this.state.filters, props.strands);
    this.setState({filteredStrands});
  }

  // TODO is there a way to re-use this method type?
  handleChangeFilter(name: FiltersType, values: FilterValuesType): void {
    const newFilters = {
      ...this.state.filters,
      [name]: values,
    };
    const filteredStrands = this.applyFiltersToStrands(newFilters, this.props.strands);
    this.setState({filters: newFilters, filteredStrands})
  }

  applyFiltersToStrands(filters: FilterTypes, strands: GetStrandListStrandsFragment[]): GetStrandListStrandsFragment[] {
    const {tagNames, saverId} = filters;
    // TODO [UI-50]: Eliminate !'s with non-nullable arrays
    return strands
      .filter(strand => intersection((strand!.tags || []).map(tag => tag!.name), tagNames).length === tagNames.length)
      .filter(strand => !saverId || strand.saver!.id === saverId)
  }

  handleSearchStrands(query: string) {
    // TODO smooth over UX by handling this promise
    this.props.refetch({query});
  }

  render() {
    return (
      <div>
        <Grid
          container
          alignItems='center'
          direction='column'
          justify='space-around'>
          <Grid item>
            <Typography variant='display2' align='center'>Strands</Typography>
          </Grid>
        </Grid>
        <Hidden mdUp>
          <StrandsViewMobile
            {...this.props}
            {...this.state}
            handleChangeFilter={this.handleChangeFilter}
            handleSearchStrands={this.handleSearchStrands}
          />
        </Hidden>
        <Hidden smDown>
          <StrandsViewDesktop
            {...this.props}
            {...this.state}
            handleChangeFilter={this.handleChangeFilter}
            handleSearchStrands={this.handleSearchStrands}
          />
        </Hidden>
      </div>
    );
  }
}

export default StrandListView;
