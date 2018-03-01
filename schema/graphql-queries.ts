import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files once that bug is resolved

export const TOPICS_QUERY = gql`
    query Topics {
        topics {
            title
            description
            tags {
                name
            }
            originalPoster {
                alias
            }
            discussion {
                status
                participants {
                    alias
                }
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
