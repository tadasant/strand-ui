import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import Paper from 'material-ui/Paper';
import {GetTopicsTopicsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../../schema/graphql-types';
import {FiltersType, FilterTypes, FilterValuesType} from '../TopicsView.react';
import TopicFilters from '../common/TopicFilters.react';

interface PropTypes {
  filteredTopics: GetTopicsTopicsFragment[]
  tags: ReferenceTagsFragment[]
  users: ReferenceUsersFragment[]
  filters: FilterTypes
  handleChangeFilter: (name: FiltersType, values: FilterValuesType) => void
}

class TopicsViewDesktop extends Component<PropTypes> {
  render() {
    return (
      <div>
        <Grid
          style={{marginTop: '1%'}}
          container
          alignItems='flex-start'
          direction='row'
          justify='center'>
          <Grid item xs={1}/>
          <Grid item xs={2}>
            <Paper>
              <TopicFilters
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
                {/*<TopicCards topics={this.props.filteredTopics}/>*/}
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={1}/>
        </Grid>
      </div>
    );
  }
}

export default TopicsViewDesktop;
