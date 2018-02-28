const HTMLPlugin = require('html-webpack-plugin');
const Dotenv = require('dotenv-webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');

const config = {
  // Root JS file for bundling
  entry: './index.js',
  module: {
    rules: [
      // Use babel for transpiling ES6 (only needed for non-typescript)
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
      // Transpile & type check with babel/typescript loader
      {
        test: /\.tsx?$/,
        use: [
          {
            // Need babel for React HMR support (otherwise could drop babel and use just typescript)
            loader: 'babel-loader',
            options: {
              babelrc: true,
              plugins: ['react-hot-loader/babel'],
            },
          },
          'ts-loader',
        ],
      },
    ],
  },
  // Enable served source maps
  devtool: 'inline-source-map',
  resolve: {
    // Include all these extensions in processing
    extensions: ['.ts', '.tsx', '.js'],
  },
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
    // Integrate .env files
    new Dotenv(),
    // HMR plugins
    new webpack.NamedModulesPlugin(),
    new webpack.HotModuleReplacementPlugin(),
  ],
};

module.exports = config;