const merge = require('webpack-merge');
const common = require('./webpack.common.ts');
const Dotenv = require('dotenv-webpack');

export default merge(common, {
  plugins: [
    new Dotenv({
      path: './env/.env.development',
      sample: true,
    }),
  ],
});
