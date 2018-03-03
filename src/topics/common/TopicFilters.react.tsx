import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Select, {OptionValues} from 'react-select';
import {get} from 'lodash';
import {FiltersType, FilterTypes, FilterValuesType} from '../TopicsView.react';
import {ReferenceTagsFragment, ReferenceUsersFragment} from '../../../schema/graphql-types';

interface PropTypes {
  filters: FilterTypes
  tags: ReferenceTagsFragment[],
  users: ReferenceUsersFragment[],
  onChangeFilter: (name: FiltersType, values: FilterValuesType) => void
}

const style = {
  content: {
    padding: '2% 2% 2% 2%',
  },
};

// TODO contribute to @types/react-select
interface ReactSelectSelection {
  value?: OptionValues,
  label?: string
}

class TopicFilters extends Component<PropTypes> {
  constructor(props: PropTypes) {
    super(props);

    this.generateHandleChangeFilter = this.generateHandleChangeFilter.bind(this);
  }

  generateHandleChangeFilter(filterName: FiltersType) {
    return (selection: Array<ReactSelectSelection> | ReactSelectSelection | null) => {
      const value = Array.isArray(selection) ? selection.map(option => option.value) : get(selection, 'value');
      this.props.onChangeFilter(filterName, value as FilterValuesType);
    }
  }

  render() {
    const tagOptions = this.props.tags.map(tag => ({
      value: tag.name,
      label: tag.name,
    }));
    const userOptions = this.props.users.map(user => ({
      value: user.id,
      label: user.alias,
    }));
    return (
      <Grid
        style={style.content}
        container
        direction='column'
        alignItems='stretch'>
        <Grid item>
          <Typography variant='headline'>Filters</Typography>
        </Grid>
        <Grid item style={{marginTop: '3%'}}>
          <Divider style={{marginBottom: '2%'}} />
          <Typography variant='body2'>Tags</Typography>
          <Select
            value={this.props.filters.tagNames}
            onChange={this.generateHandleChangeFilter('tagNames')}
            options={tagOptions}
            multi
          />
          <Divider style={{marginTop: '2%'}}/>
        </Grid>
        <Grid item style={{marginTop: '1%'}}>
          <Typography variant='body2'>Participants</Typography>
          <Select
            value={this.props.filters.participantIds}
            onChange={this.generateHandleChangeFilter('participantIds')}
            options={userOptions}
            multi
          />
          <Divider style={{marginTop: '2%'}}/>
        </Grid>
        <Grid item style={{marginTop: '1%'}}>
          <Typography variant='body2'>Original Poster</Typography>
          <Select
            value={this.props.filters.originalPosterId}
            onChange={this.generateHandleChangeFilter('originalPosterId')}
            options={userOptions}
          />
          <Divider style={{marginTop: '2%'}}/>
        </Grid>
      </Grid>
    );
  }
}

export default TopicFilters;
