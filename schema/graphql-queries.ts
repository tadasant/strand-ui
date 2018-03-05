import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files once that bug is resolved

export const GET_TOPICS_QUERY = gql`
    query GetTopics {
        topics {
            ...GetTopicsTopics
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

// Fragments

gql`
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
`;

gql`
    fragment GetTopicsTags on TagType {
        name
    }
`;

gql`
    fragment GetTopicsOriginalPoster on UserType {
        alias
    }
`;

gql`
    fragment GetTopicsDiscussion on DiscussionType {
        status
        participants {
            ...GetTopicsParticipants
        }
    }
`;

gql`
    fragment GetTopicsParticipants on UserType {
        alias
    }
`;
