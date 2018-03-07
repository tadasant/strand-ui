import deployment from './webpack.deployment';
import * as merge from 'webpack-merge';
import * as webpack from 'webpack';

const Dotenv = require('dotenv-webpack');

const config: webpack.Configuration = {
  plugins: [
    new Dotenv({
      path: './env/.env.production',
      safe: './env/.env.example',
    }),
  ],
};

export default merge(deployment, config);
