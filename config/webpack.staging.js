const merge = require('webpack-merge');
const deployment = require('./webpack.deployment.js');
const Dotenv = require('dotenv-webpack');

module.exports = merge(deployment, {
  plugins: [
    new Dotenv({
      path: './.env.staging',
      sample: true,
    }),
  ],
});
