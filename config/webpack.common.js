const HTMLPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');

const config = {
  // Root JS file for bundling
  entry: './index.js',
  module: {
    rules: [
      // Use babel for transpiling ES6
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      // Bundle files (e.g. images)
      {
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {},
          },
        ],
      },
    ],
  },
  // Enable served source maps
  devtool: 'inline-source-map',
  // Webpack Dev Server for running locally
  devServer: {
    // Play nicely with react-router
    historyApiFallback: true,
    port: 3000,
    // Enable hot module reloading (HMR)
    hot: true,
  },
  plugins: [
    // Cleans the build folder per-build/reload
    new CleanWebpackPlugin(['dist']),
    // Builds the .html file for entering into bundle
    new HTMLPlugin({
      template: 'index.html',
    }),
    // HMR plugins
    new webpack.NamedModulesPlugin(),
    new webpack.HotModuleReplacementPlugin(),
  ],
};

module.exports = config;