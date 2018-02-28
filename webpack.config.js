const HTMLPlugin = require('html-webpack-plugin');
const Dotenv = require('dotenv-webpack');

const config = {
  entry: './index.js',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
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
  devServer: {
    contentBase: './',
    port: 3000,
  },
  plugins: [
    new HTMLPlugin({
      template: 'index.html',
    }),
    new Dotenv(),
  ],
};

module.exports = config;