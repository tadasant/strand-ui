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

## .env file management

[Parcel.js commit](https://github.com/parcel-bundler/parcel/pull/258/files/bb4f1e62b4948c59983a730262d6938497e4c365) that added dotenv support

[Breakdown](https://github.com/bkeepers/dotenv#what-other-env-files-can-i-use) of intended implementation 

Basically the hierarchy is:
1) .env.${NODE_ENV}.local
2) .env.${NODE_ENV}
3) .env.local (excluded if NODE_ENV == 'test')
4) .env

1 takes priority over 2, etc.

Note that `parcel build` overrides `NODE_ENV` to be `production`, hence our leveraging `REALM` in the script & in `index.js`.

## Running tests

It's important to make sure you're running on the up-to-date GraphQL schema. Extract from CCP by going to project root and doing:

`python manage.py graphql_schema --out client/test/schema.json`

Commit the schema. CCU-26 will automate this process.