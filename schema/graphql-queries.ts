import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files once that bug is resolved

export const GET_TOPICS_QUERY = gql`
    query GetTopics {
        topics {
            ...GetTopicsTopics
        }
    }

    fragment GetTopicsTopics on TopicType {
        title
        description
        tags {
            ...GetTopicsTags
        }
        originalPoster {
            ...GetTopicsOriginalPoster
        }
        discussion {
            ...GetTopicsDiscussion
        }
    }

    fragment GetTopicsTags on TagType {
        name
    }

    fragment GetTopicsOriginalPoster on UserType {
        id
        alias
    }

    fragment GetTopicsDiscussion on DiscussionType {
        status
        participants {
            ...GetTopicsParticipants
        }
    }

    fragment GetTopicsParticipants on UserType {
        id
        alias
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

export const GET_REFERENCE_DATA_QUERY = gql`
    query GetReferenceData {
        tags {
            ...ReferenceTags
        }
        users {
            ...ReferenceUsers
        }
    }
  
    fragment ReferenceTags on TagType {
        name
    }
  
    fragment ReferenceUsers on UserType {
        id
        alias
    }
`;
