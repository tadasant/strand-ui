const merge = require('webpack-merge');
const deployment = require('./webpack.deployment.ts');
const Dotenv = require('dotenv-webpack');

export default merge(deployment, {
  plugins: [
    new Dotenv({
      path: './env/.env.staging',
      safe: './env/.env.example',
    }),
  ],
});
