# This project is retired. No further development or maintenance is planned. Feel free to fork and re-use.

## Overview

This web application was built using:
* React 16.2
* TypeScript 2.7
* Webpack 4.0
* Apollo (GraphQL)
* Material UI 1.0 beta
* Jest 22.3

It was hosted on an Amazon S3 bucket, gated by Amazon CloudFront as the CDN.

[strand-slack](https://github.com/tadasant/strand-slack) was the companion Slack Integration

[strand-api](https://github.com/tadasant/strand-api) was the companion backend API

Contributors: [@tadasant](https://github.com/tadasant) and [@Audace](https://github.com/audace)

![screenshot](https://raw.githubusercontent.com/tadasant/strand-ui/master/media/strand-ui.png)

## Getting Started

It is recommended that you use WebStorm (not PyCharm) for development.

We use [yarn](https://yarnpkg.com/en/) (rather than `npm`) as our package manager. Install `yarn` with `brew install yarn`.

Run `yarn install` to set up your `node_modules`.

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

## Running tests

It's important to make sure you're running on the up-to-date GraphQL schema. See section below on GraphQL schemas.

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

## Webpack, TypeScript, .env files, babel, oh my...

Webpack - our bundler. Manages the flow of steps that need to be done in going from raw source code to performant
application in the browser.

TypeScript - compiles and transpiles our code. Takes TypeScript code, which is a superset of ES6-compliant (?) JavaScript.

.env files - used for configuring primitive values (e.g. feature toggles, endpoints) across realms.

Babel - not really needed anymore due to introduction of TypeScript. Previously used to be used for transpiling ES6 -> ES5.
.babelrc and babel-loader, etc, remain because react-hot-loader depends on it.

package.json - contains a tiny bit of config (stagingcdn, productioncdn) because there's a known html-webpack-plugin
issue ([UI-46](https://solutionloft.atlassian.net/browse/UI-46)) that prevents us from using a workaround for it. 

## GraphQL schemas, testing, and TypeScript

Recommended that you install the JS GraphQL plugin for IntelliJ so you get features for playing with gql queries with ease.
IntelliJ uses `graphql.config.json` is ONLY used for local IntelliJ development. Nothing to do with the source code itself.
 

Extract and updated GraphQL schema from API by going to its project root and doing:

`python3 manage.py graphql_schema --indent 2 --out graphql.schema.json`

Commit the schema to `schema.json` in UI. UI-26 will automate this process.

An alternative to consider; can use `apollo-codegen` over the wire:

`node_modules/.bin/apollo-codegen introspect-schema http://localhost:8000/graphql --output graphql.schema.json`
 
Generate up-to-date TypeScript definitions with:

`node_modules/.bin/apollo-codegen generate schema/graphql-queries.ts --schema schema/graphql.schema.json --target typescript --output schema/graphql-types.ts`
