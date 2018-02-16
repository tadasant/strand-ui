# CodeClippy Portal - UI

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Getting Started

We use [yarn](https://yarnpkg.com/en/) (rather than `npm`) as our package manager. Install `yarn` with `brew install yarn`.

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

`python manage.py graphql_schema --indent 2 --out client/test/schema.json`

Commit the schema. CCU-26 will automate this process.

We use [jest](https://github.com/facebook/jest) and [enzyme](https://github.com/airbnb/enzyme) for UI testing. 

While developing, using `yarn test-watch`. This will watch test files that are testing the production files to which you have made edits (based on git).

Otherwise, `yarn test` will run the whole test suite.

## Running eslint in PyCharm

To run on all files: `cd client && ./node_modules/eslint/bin/eslint.js --fix .`

To set up a single file hotkey:
1) Preference
2) Keymap
3) "Fix ESLint Problems"
4) Recommend ctrl + opt + L (similar to cmd + opt + L code reformat) 
