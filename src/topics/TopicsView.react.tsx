import * as React from 'react';
import {StatelessComponent} from 'react';
// import TopicsView from './TopicsView.react';


const TopicsView: StatelessComponent = () => <div />;

export default TopicsView;


// import * as React from 'react';
// import {Component} from 'react';
// import {Grid, Hidden, Typography} from 'material-ui';
// import isEqual from 'lodash/isEqual';
// import intersection from 'lodash/intersection';
// // import TopicsViewDesktop from './rwd/TopicsViewDesktop.react';
// // import TopicsViewMobile from './rwd/TopicsViewMobile.react';
//
// const propTypes = {
//   helpSessions: PropTypes.arrayOf(helpSessionPropType.isRequired).isRequired,
//   tags: PropTypes.arrayOf(tagPropType.isRequired).isRequired,
//   users: PropTypes.arrayOf(userPropType.isRequired).isRequired,
//   searchHelpSessions: PropTypes.func.isRequired,
// };
//
// interface PropTypes {
//   topics:
// }
//
// class HelpSessionDashboard extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       filteredHelpSessions: [],
//       filters: {
//         tagNames: [],
//         askerId: null,
//         answererId: null,
//         participantIds: [],
//       },
//     };
//
//     this.handleChangeFilter = this.handleChangeFilter.bind(this);
//   }
//
//   componentWillMount() {
//     this.updateStateWithProps(this.props);
//   }
//
//   componentDidMount() {
//     this.context.mixpanel.track('CC - Sessions - viewed');
//   }
//
//   componentWillReceiveProps(newProps) {
//     if (!isEqual(newProps.helpSessions, this.props.helpSessions)) {
//       this.updateStateWithProps(newProps);
//     }
//   }
//
//   updateStateWithProps(props) {
//     const filteredHelpSessions = this.applyFiltersToHelpSessions(this.state.filters, props.helpSessions);
//     this.setState({filteredHelpSessions});
//   }
//
//   handleChangeFilter(name, values) {
//     const newFilters = {
//       ...this.state.filters,
//       [name]: values,
//     };
//     this.context.mixpanel.track('CC - Sessions - set filter', {
//       'name': name,
//       'values': values,
//     });
//     const filteredHelpSessions = this.applyFiltersToHelpSessions(newFilters, this.props.helpSessions);
//     this.setState({filters: newFilters, filteredHelpSessions})
//   }
//
//   applyFiltersToHelpSessions(filters, helpSessions) {
//     const {tagNames, askerId, answererId, participantIds} = filters;
//     return helpSessions
//       .filter(session => intersection(session.tags.map(tag => tag.name), tagNames).length === tagNames.length)
//       .filter(session => !answererId || session.answerer.id === answererId)
//       .filter(session => !askerId || session.asker.id === askerId)
//       .filter(session => intersection(session.participants.map(user => user.id), participantIds).length === participantIds.length)
//   }
//
//   render() {
//     return (
//       <div>
//         <Grid
//           container
//           alignItems='center'
//           direction='column'
//           justify='space-around'>
//           <Grid item>
//             <Typography type='display2' align='center'>Answers</Typography>
//             <Typography type='aside' align='center'>Review all help sessions</Typography>
//           </Grid>
//         </Grid>
//         <Hidden mdUp>
//           <HelpSessionDashboardMobile
//             {...this.props}
//             {...this.state}
//             handleChangeFilter={this.handleChangeFilter}
//           />
//         </Hidden>
//         <Hidden smDown>
//           <HelpSessionDashboardDesktop
//             {...this.props}
//             {...this.state}
//             handleChangeFilter={this.handleChangeFilter}
//           />
//         </Hidden>
//       </div>
//     );
//   }
// }
//
// HelpSessionDashboard.contextTypes = {
//   mixpanel: PropTypes.object.isRequired,
// };
//
// HelpSessionDashboard.propTypes = propTypes;
//
// export default HelpSessionDashboard;