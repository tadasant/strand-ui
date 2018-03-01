const merge = require('webpack-merge');
import common from './webpack.common';
import * as webpack from 'webpack';

const config: webpack.Configuration = {}

export default merge(common, config);
