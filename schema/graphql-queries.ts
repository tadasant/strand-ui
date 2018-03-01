import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files once that bug is resolved

const TOPICS_QUERY_PARTICIPANTS = gql`
    fragment TopicsParticipants on UserType {
        alias
    }
`;

const TOPICS_QUERY_DISCUSSION = gql`
  fragment TopicsDiscussions on DiscussionType {
      status
      participants {
          ...TopicsParticipants
      }
  }
`;

const TOPICS_QUERY_ORIGINAL_POSTER = gql`
  fragment TopicsOriginalPoster on UserType {
      alias
  }
`;

const TOPICS_QUERY_TAGS = gql`
  fragment TopicsTags on TagType {
      name
  }
`

export const TOPICS_QUERY = gql`
    query Topics {
        topics {
            title
            description
            tags {
                ...TopicsTags
            }
            originalPoster {
                ...TopicsOriginalPoster
            }
            discussion {
                ...TopicsDiscussions
            }
        }
    }
`;

export const ATTEMPT_SLACK_INSTALLATION_MUTATION = gql`
    mutation AttemptInstall ($code: String!, $clientId: String!, $redirectUri: String!) {
        attemptSlackInstallation(input: {code: $code, clientId: $clientId, redirectUri: $redirectUri}) {
            slackTeam {
                name
            }
        }
    }
`;
