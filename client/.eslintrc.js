module.exports = {
  'extends': ['eslint:recommended', 'plugin:react/recommended'],
  'plugins': [
    'react',
    'jest'
  ],
  'parserOptions': {
    'sourceType': 'module',
    'ecmaVersion': 2017,
    'ecmaFeatures': {
      'jsx': true,
    }
  },
  'rules': {
    'quotes': ['error', 'single'],
    'indent': ['error', 2],
    'no-console': 'warn',
    'react/no-find-dom-node': 'warn',
    'jsx-quotes': ['error', 'prefer-single']
  },
  'env': {
    'jest/globals': true,
    'es6': true,
  },
  'globals': {
    'process': true,
    'module': true,
    'window': true,
    'console': true,
    'document': true,
    'setImmediate': true,
  }
};
