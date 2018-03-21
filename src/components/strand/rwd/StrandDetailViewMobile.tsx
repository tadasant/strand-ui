import * as React from 'react';
import {Component} from 'react';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import StrandViewHeaderStacked from '../common/StrandDetailViewHeaderStacked';
import {GetStrandDetailStrandFragment} from '../../../../schema/graphql-types';
import * as ReactMarkdown from 'react-markdown';
import renderers from '../common/markdownRenderers';

interface PropTypes {
  strand: GetStrandDetailStrandFragment
}


class StrandDetailMobile extends Component<PropTypes> {
  render() {
    return (
      <Grid item>
        <Grid item>
          <StrandViewHeaderStacked strand={this.props.strand}/>
          <Divider style={{marginTop: '5vh', marginBottom: '5vh'}}/>
        </Grid>
        <Grid item>
          <ReactMarkdown source={this.props.strand.body} renderers={renderers}/>
        </Grid>
      </Grid>
    );
  }
}

export default StrandDetailMobile;
