// import React, {Component} from 'react';
// // import TopicsView from './TopicsView.react';
// import gql from 'graphql-tag';
//
//
//
// class TopicsViewContainer extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       isLoadingHelpSessions: false,
//       helpSessions: [],
//       isLoadingUsers: false,
//       users: [],
//       isLoadingTags: false,
//       tags: [],
//     };
//
//     this.pullHelpSessions = this.pullHelpSessions.bind(this);
//   }
//
//   componentWillMount() {
//     this.pullHelpSessions();
//     this.pullTagNames();
//     this.pullUserIds();
//   }
//
//   pullHelpSessions(searchQuery) {
//     this.setState({isLoadingHelpSessions: true}, () => {
//       const bare_url = '/api/help-sessions/';
//       const url = searchQuery ? `${bare_url}?search_query=${searchQuery}` : bare_url;
//       if (searchQuery) {
//         this.context.mixpanel.track('CC - Sessions - search', {'query': searchQuery})
//       }
//       axios.get(url).then((res) => {
//         this.setState({helpSessions: res.data, isLoadingHelpSessions: false});
//       }).catch((err) => {
//         this.setState({isLoadingHelpSessions: false});
//         if (err.response) {
//           console.log(err.response.status);
//         } else {
//           console.log('Error', err.message);
//         }
//         console.log(err.config);
//       });
//     });
//   };
//
//   pullTagNames() {
//     this.setState({isLoadingTags: true}, () => {
//       axios.get(`/api/tags/`).then((res) => {
//         this.setState({tags: res.data, isLoadingTags: false});
//       }).catch((err) => {
//         this.setState({isLoadingTags: false});
//         if (err.response) {
//           console.log(err.response.status);
//         } else {
//           console.log('Error', err.message);
//         }
//         console.log(err.config);
//       });
//     });
//   };
//
//   pullUserIds() {
//     this.setState({isLoadingUsers: true}, () => {
//       axios.get(`/api/community-users/`).then((res) => {
//         const users = res.data.map(communityUser => communityUser.user);
//         this.setState({users, isLoadingUsers: false});
//       }).catch((err) => {
//         this.setState({isLoadingUsers: false});
//         if (err.response) {
//           console.log(err.response.status);
//         } else {
//           console.log('Error', err.message);
//         }
//         console.log(err.config);
//       });
//     });
//   };
//
//   render() {
//     return (
//       <HelpSessionDashboard
//         helpSessions={this.state.helpSessions}
//         searchHelpSessions={this.pullHelpSessions}
//         users={this.state.users}
//         tags={this.state.tags}
//       />
//     );
//   }
// }
//
// export default TopicsViewContainer;
