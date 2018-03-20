import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import {GetStrandListStrandsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../../../schema/graphql-types';
import {FiltersType, FilterTypes, FilterValuesType} from '../StrandListView';
import StrandFilters from '../common/StrandFilters';
import StrandTiles from '../common/StrandTileList';
import SearchBox from '../common/SearchBox';

interface PropTypes {
  filteredStrands: GetStrandListStrandsFragment[]
  tags: ReferenceTagsFragment[]
  users: ReferenceUsersFragment[]
  filters: FilterTypes
  handleChangeFilter: (name: FiltersType, values: FilterValuesType) => void
  handleSearchStrands: (searchValue: string) => void
}

class StrandListViewDesktop extends Component<PropTypes> {
  render() {
    return (
      <Grid
        style={{marginTop: '1%'}}
        container
        alignItems='flex-start'
        direction='row'
        justify='center'>
        <Grid item xs={1}/>
        <Grid item xs={2}>
          <Paper>
            <StrandFilters
              filters={this.props.filters}
              onChangeFilter={this.props.handleChangeFilter}
              users={this.props.users}
              tags={this.props.tags}
            />
          </Paper>
        </Grid>
        <Grid item xs={8}>
          <Grid container direction='column' alignItems='stretch'>
            <Grid item xs={12}>
              <SearchBox onSearchStrands={this.props.handleSearchStrands}/>
            </Grid>
            <Grid item xs={12}>
              <StrandTiles strands={this.props.filteredStrands}/>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={1}/>
      </Grid>
    );
  }
}

export default StrandListViewDesktop;
