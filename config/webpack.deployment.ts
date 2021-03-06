import * as HTMLPlugin from 'html-webpack-plugin';
import common from './webpack.common';
import * as webpack from 'webpack';
import * as merge from 'webpack-merge';
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

const config: webpack.Configuration = {
  plugins: [
    // Builds the .html file for entering into bundle
    new HTMLPlugin({
      template: 'INDEX_TEMPLATE.html',
      favicon: 'assets/favicon.ico',
    }),
    new UglifyJSPlugin(),
  ]
};

export default merge(common, config);
