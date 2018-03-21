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
  resolve: {
    // Include all these extensions in processing (note we need .js because not all node_modules are .ts)
    extensions: ['.ts', '.tsx', '.js', '.css'],
  },
  plugins: [
    // Cleans the build folder per-build/reload
    new CleanWebpackPlugin(['dist']),
  ],
};

export default config;
