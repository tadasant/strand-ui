const Dotenv = require('dotenv-webpack');
import common from './webpack.common';
import * as merge from 'webpack-merge';
import * as webpack from 'webpack';

const config: webpack.Configuration = {
  plugins: [
    new Dotenv({
      path: './env/.env.staging',
      safe: './env/.env.example',
    }),
  ],
};

export default merge(common, config);
