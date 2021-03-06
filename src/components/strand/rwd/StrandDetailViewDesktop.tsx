import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import StrandViewHeader from '../common/StrandDetailViewHeader';
import {GetStrandDetailStrandFragment} from '../../../../schema/graphql-types';
import * as ReactMarkdown from 'react-markdown';
import renderers from '../common/markdownRenderers';


interface PropTypes {
  strand: GetStrandDetailStrandFragment
}

class StrandViewDesktop extends Component<PropTypes> {
  render() {
    return (
      <Grid item>
        <Grid item>
          <StrandViewHeader strand={this.props.strand}/>
          <Divider style={{marginTop: '2.5%', marginBottom: '2.5%'}}/>
        </Grid>
        <Grid item style={{padding: '2% 2% 2% 2%', overflow: 'hidden'}}>
          <ReactMarkdown source={this.props.strand.body} renderers={renderers}/>
        </Grid>
      </Grid>
    );
  }
}

export default StrandViewDesktop;
