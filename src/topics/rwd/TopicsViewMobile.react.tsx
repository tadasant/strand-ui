import * as React from 'react';
import {Component} from 'react';
import Grid from 'material-ui/Grid';
import {GetTopicsTopicsFragment, ReferenceTagsFragment, ReferenceUsersFragment} from '../../../schema/graphql-types';
import {FiltersType, FilterTypes, FilterValuesType} from '../TopicsView.react';
import TopicTiles from '../common/TopicTiles.react';

interface PropTypes {
  filteredTopics: GetTopicsTopicsFragment[]
  tags: ReferenceTagsFragment[]
  users: ReferenceUsersFragment[]
  filters: FilterTypes
  handleChangeFilter: (name: FiltersType, values: FilterValuesType) => void
}

class TopicsViewMobile extends Component<PropTypes> {
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
          <Grid item xs={10}>
            <Grid container direction='column' alignItems='stretch'>
              <Grid item xs={12}>
                <TopicTiles topics={this.props.filteredTopics} minimal/>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={1}/>
        </Grid>
      </div>
    );
  }
}

export default TopicsViewMobile;
