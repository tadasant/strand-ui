const merge = require('webpack-merge');
const deployment = require('./webpack.deployment.ts');
const Dotenv = require('dotenv-webpack');

export default merge(deployment, {
  plugins: [
    new Dotenv({
      path: './env/.env.production',
      safe: './env/.env.example',
    }),
  ],
});
