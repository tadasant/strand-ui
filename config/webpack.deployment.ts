import * as HTMLPlugin from 'html-webpack-plugin';
import common from './webpack.common';
import * as webpack from 'webpack';

const merge = require('webpack-merge');

const config: webpack.Configuration = {
  plugins: [
    // Builds the .html file for entering into bundle
    new HTMLPlugin({
      template: 'INDEX_TEMPLATE.html',
    }),
  ]
};

export default merge(common, config);
