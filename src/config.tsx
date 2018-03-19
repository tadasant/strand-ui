// dotenv-webpack ensures these all exist at build time via .env.example (hence the !'s)

export const GRAPHQL_URL = process.env.GRAPHQL_URL!;
export const SLACK_CLIENT_ID = process.env.SLACK_CLIENT_ID!;
export const UI_HOST = process.env.UI_HOST!;
export const SLACK_SCOPES = process.env.SLACK_SCOPES!;
export const NODE_ENV = process.env.NODE_ENV!;
export const VERSION = process.env.VERSION!;
export const SENTRY_KEY = process.env.SENTRY_KEY!;
export const SENTRY_PROJECT_ID = process.env.SENTRY_PROJECT_ID!;
export const STRAND_SLACK_HOST = process.env.STRAND_SLACK_HOST!!;
export const STRAND_API_HOST = process.env.STRAND_API_HOST!;
