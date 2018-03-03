import * as React from 'react';
import {Component} from 'react';
import {GetTopicsTopicsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../schema/graphql-types';
import {intersection} from 'lodash';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Hidden from 'material-ui/Hidden';
import TopicsViewDesktop from './rwd/TopicsViewDesktop.react';

interface PropTypes {
  topics: GetTopicsTopicsFragment[],
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

export type FiltersType = 'tagNames' | 'originalPosterId' | 'participantIds';

export interface FilterTypes {
  tagNames: string[],
  originalPosterId?: number,
  participantIds: number[],
}

interface StateTypes {
  filteredTopics: GetTopicsTopicsFragment[],
  filters: FilterTypes,
}

class TopicsView extends Component<PropTypes, StateTypes> {
  constructor(props: PropTypes) {
    super(props);
    // TODO [UI-49]: At scale, filters can't be in-memory
    this.state = {
      filteredTopics: [],
      filters: {
        tagNames: [],
        originalPosterId: undefined,
        participantIds: [],
      },
    };

    this.handleChangeFilter = this.handleChangeFilter.bind(this);
  }

  handleChangeFilter(name: FiltersType, values: string[] | number | undefined): void {
    const newFilters = {
      ...this.state.filters,
      [name]: values,
    };
    const filteredTopics = this.applyFiltersToTopics(newFilters, this.props.topics);
    this.setState({filters: newFilters, filteredTopics})
  }

  applyFiltersToTopics(filters: FilterTypes, topics: GetTopicsTopicsFragment[]) {
    const {tagNames, originalPosterId, participantIds} = filters;
    // TODO [UI-50]: Eliminate !'s with non-nullable arrays
    return topics
      .filter(topic => intersection((topic!.tags || []).map(tag => tag!.name), tagNames).length === tagNames.length)
      .filter(topic => !originalPosterId || parseInt(topic.originalPoster!.id) === originalPosterId)
      .filter(topic => intersection((topic!.discussion!.participants || []).map(user => parseInt(user!.id)), participantIds).length === participantIds.length)
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
            <Typography variant='display2' align='center'>Topics</Typography>
            <Typography variant='caption' align='center'>Review all topics discussed</Typography>
          </Grid>
        </Grid>
        <Hidden mdUp>
          <div>small</div>
          {/*<HelpSessionDashboardMobile*/}
            {/*{...this.props}*/}
            {/*{...this.state}*/}
            {/*handleChangeFilter={this.handleChangeFilter}*/}
          {/*/>*/}
        </Hidden>
        <Hidden smDown>
          <TopicsViewDesktop
            {...this.props}
            {...this.state}
            handleChangeFilter={this.handleChangeFilter}
          />
        </Hidden>
      </div>
    );
  }
}

export default TopicsView;
