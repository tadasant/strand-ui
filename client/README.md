# CodeClippy Portal - UI

## Getting Started

We use `yarn` (rather than `npm`) as our package manager. Install `yarn` with `brew install yarn`.

Run `cd client && yarn install` to set up your `node_modules`.

To run locally (with hot module replacement!), simply run `yarn start`.

## Deployment

Staging: `yarn build staging`
Production: `yarn build`

The output build files will be placed in `build/`.

Do not commit these built files.
