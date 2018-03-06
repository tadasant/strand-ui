import * as HTMLPlugin from 'html-webpack-plugin';
import common from './webpack.common';
import * as merge from 'webpack-merge';
import * as webpack from 'webpack';

const Dotenv = require('dotenv-webpack');

const config: webpack.Configuration = {
  plugins: [
    new Dotenv({
      path: './env/.env.development',
      safe: './env/.env.example',
    }),
    // Builds the .html file for entering into bundle. Need the publicPath for react-router
    // https://github.com/ReactTraining/react-router/issues/676#issuecomment-174073981
    new HTMLPlugin({
      template: 'INDEX_TEMPLATE.html',
      publicPath: '/',
    }),
  ],
};

export default merge(common, config);
