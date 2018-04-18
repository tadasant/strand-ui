import * as HTMLPlugin from 'html-webpack-plugin';
import common from './webpack.common';
import * as merge from 'webpack-merge';
import * as webpack from 'webpack';

const Dotenv = require('dotenv-webpack');

const config: webpack.Configuration = {
  // Enable served source maps
  devtool: 'inline-source-map',
  // Webpack Dev Server for running locally
  devServer: {
    // Play nicely with react-router
    historyApiFallback: true,
    port: 3000,
    // Enable hot module reloading (HMR)
    hot: true,
    // Allow access via ngrok to local
    disableHostCheck: true,
  },
  plugins: [
    new Dotenv({
      path: './env/.env.development',
      safe: './env/.env.example',
    }),
    // Builds the .html file for entering into bundle. Need the publicPath for react-router
    // https://github.com/ReactTraining/react-router/issues/676#issuecomment-174073981
    new HTMLPlugin({
      template: 'INDEX_TEMPLATE.html',
      favicon: 'assets/favicon.ico',
      publicPath: '/',
    }),
    // HMR plugins
    new webpack.NamedModulesPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    // Prevents webpack watch from going into infinite loop (& stopping on retry) due to TS compilation
    new webpack.WatchIgnorePlugin([
      /\.js$/,
      /\.d\.ts$/,
    ]),
  ],
};

export default merge(common, config);
