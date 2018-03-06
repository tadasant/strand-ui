import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files

export const GET_TOPICS_QUERY = gql`
    query GetTopics {
        topics {
            ...GetTopicsTopics
        }
    }

    fragment GetTopicsTopics on TopicType {
        id
        title
        description
        tags {
            ...GetTopicsTags
        }
        originalPoster {
            ...GetTopicsUser
        }
        discussion {
            ...GetTopicsDiscussion
        }
    }

    fragment GetTopicsTags on TagType {
        name
    }

    fragment GetTopicsUser on UserType {
        id
        alias
    }

    fragment GetTopicsDiscussion on DiscussionType {
        status
        participants {
            ...GetTopicsUser
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

export const GET_TOPIC_QUERY = gql`
    query GetTopic($id: Int!) {
        topic(id: $id) {
            ...GetTopicTopic
        }
    }
    
    fragment GetTopicTopic on TopicType {
        id
        title
        description
        tags {
            ...GetTopicTags
        }
        originalPoster {
            ...GetTopicUser
        }
        discussion {
            ...GetTopicDiscussion
        }
    }
  
    fragment GetTopicTags on TagType {
        name
    }
  
    fragment GetTopicUser on UserType {
        id
        alias
    }
  
    fragment GetTopicDiscussion on DiscussionType {
        timeStart
        timeEnd
        status
        participants {
            ...GetTopicUser
        }
    }
`;
