import * as CleanWebpackPlugin from 'clean-webpack-plugin';
import * as webpack from 'webpack';

const config: webpack.Configuration = {
  // Root TS file for bundling
  entry: './src/index.tsx',
  module: {
    rules: [
      // Bundle files (e.g. images)
      {
        test: /\.(png|jpg|gif)$/,
        use: ['file-loader'],
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
      // Handle .css files
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
    ],
  },
  // Enable served source maps
  devtool: 'inline-source-map',
  resolve: {
    // Include all these extensions in processing (note we need .js because not all node_modules are .ts)
    extensions: ['.ts', '.tsx', '.js', '.css'],
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

export default config;
