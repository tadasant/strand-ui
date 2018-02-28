# Strand Portal - UI

[![CodeFactor](https://www.codefactor.io/repository/github/solutionloft/strand-ui/badge)](https://www.codefactor.io/repository/github/solutionloft/strand-ui)

## Getting Started

It is recommended that you use WebStorm (not PyCharm) for development.

We use [yarn](https://yarnpkg.com/en/) (rather than `npm`) as our package manager. Install `yarn` with `brew install yarn`.

Run `cd client && yarn install` to set up your `node_modules`.

To run locally (with hot module replacement!), simply run `yarn start`.

## Deploying to Staging

We host our UI as a static website on S3. Staging is at https://staging.app.trystrand.com/

Before deploying, ensure that the `package.json` entry for `config`, namely `stagingcdn`, is
set to the appropriate s3 bucket endpoint, and the `.env` files have the appropriate `VERSION` number set throughout.

Generally, use existing CircleCI workflows to deploy staging/production builds. Note that you probably want to bust
the CloudFront cache after deploying (otherwise the changes won't be live for up to half a day). Do this by:
1) Open CloudFront in [AWS Console](https://console.aws.amazon.com/cloudfront) 
2) Open the relevant Distribution
3) Go to Invalidations
4) Create a new Invalidation for `*` (all files)

If you need to do a manual deploy without using CircleCI:

`yarn build-staging`

The output build files will be placed in `build/`.

Do not commit these built files. Upload them to S3. Note that the bucket names must be set equal to the domain to make DNS work correctly:

Staging: `aws s3 rm s3://staging.app.trystrand.com/ --recursive && aws s3 cp build/ s3://staging.app.trystrand.com/ --recursive`

[HTTPS Configuration Reference](https://medium.com/@sbuckpesch/setup-aws-s3-static-website-hosting-using-ssl-acm-34d41d32e394)

## Releasing to Production

Production can be found at  https://app.trystrand.com/.

Same instructions as above apply: namely, check `package.json` for `productioncdn` and `.env` files for `VERSION`.

Merge to master and [create a release](https://help.github.com/articles/creating-releases/) on GitHub.

Using CircleCI, approve the deploy to production.

## .env file management

[Parcel.js commit](https://github.com/parcel-bundler/parcel/pull/258/files/bb4f1e62b4948c59983a730262d6938497e4c365) that added dotenv support

[Breakdown](https://github.com/bkeepers/dotenv#what-other-env-files-can-i-use) of intended implementation 

Basically the hierarchy is:
1) .env.${NODE_ENV}.local
2) .env.${NODE_ENV}
3) .env.local (excluded if NODE_ENV == 'test')
4) .env

1 takes priority over 2, etc.

Note that `parcel build` overrides `NODE_ENV` to be `production`, hence our leveraging `REALM` in the script & in `index.tsx`.

## Running tests

It's important to make sure you're running on the up-to-date GraphQL schema. Extract from API by going to its project root and doing:

`python manage.py graphql_schema --indent 2 --out schema.json`

Commit the schema to `test/schema.json` in UI. UI-26 will automate this process.

We use [jest](https://github.com/facebook/jest) and [enzyme](https://github.com/airbnb/enzyme) for UI testing. 

While developing, using `yarn test-watch`. This will watch test files that are testing the production files to which you have made edits (based on git).

Otherwise, `yarn test` will run the whole test suite.

Use `yarn test -u` if you need to update jest snapshots.

## Running eslint in WebStorm

To run on all files: `./node_modules/eslint/bin/eslint.js --fix .`

To set up a single file hotkey:
1) Preferences
2) Keymap
3) "Fix ESLint Problems"
4) Recommend ctrl + opt + L (similar to cmd + opt + L code reformat) 

## Webpack, TypeScript, .env files, oh my...

// TODO
