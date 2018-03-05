import * as React from 'react';
import {Component} from 'react';
import {GetTopicsTopicsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../schema/graphql-types';
import {intersection} from 'lodash';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Hidden from 'material-ui/Hidden';
import TopicsViewDesktop from './rwd/TopicsViewDesktop.react';
import TopicsViewMobile from './rwd/TopicsViewMobile.react';

interface PropTypes {
  topics: GetTopicsTopicsFragment[],
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
}

export type FiltersType = 'tagNames' | 'originalPosterId' | 'participantIds';
export type FilterValuesType = string[] | number | number[] | void;

export interface FilterTypes {
  tagNames: string[],
  originalPosterId?: string,
  participantIds: string[],
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

  componentWillMount() {
    this.updateStateWithProps(this.props);
  }

  updateStateWithProps(props: PropTypes) {
    const filteredTopics = this.applyFiltersToTopics(this.state.filters, props.topics);
    this.setState({filteredTopics});
  }

  // TODO is there a way to re-use this method type?
  handleChangeFilter(name: FiltersType, values: FilterValuesType): void {
    const newFilters = {
      ...this.state.filters,
      [name]: values,
    };
    const filteredTopics = this.applyFiltersToTopics(newFilters, this.props.topics);
    this.setState({filters: newFilters, filteredTopics})
  }

  applyFiltersToTopics(filters: FilterTypes, topics: GetTopicsTopicsFragment[]): GetTopicsTopicsFragment[] {
    const {tagNames, originalPosterId, participantIds} = filters;
    // TODO [UI-50]: Eliminate !'s with non-nullable arrays
    return topics
      .filter(topic => intersection((topic!.tags || []).map(tag => tag!.name), tagNames).length === tagNames.length)
      .filter(topic => !originalPosterId || topic.originalPoster!.id === originalPosterId)
      .filter(topic => intersection((topic!.discussion ? topic!.discussion!.participants || [] : []).map(user => user!.id), participantIds).length === participantIds.length)
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
          <TopicsViewMobile
            {...this.props}
            {...this.state}
            handleChangeFilter={this.handleChangeFilter}
          />
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
