module.exports = {
  // Allow absolute imports from the following bases
  'moduleDirectories': [
    'node_modules',
    './',
    'src/',
  ],
  // Consider only files with these extensions
  'moduleFileExtensions': [
    'ts',
    'tsx',
    'js',
    'json',
  ],
  'setupTestFrameworkScriptFile': '<rootDir>/test/setup.js',
  'moduleNameMapper': {
    // Mock all these filetypes
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/test/__mocks__/fileMock.js',
  },
  // Helpers for ease of serializing snapshots
  'snapshotSerializers': ['enzyme-to-json/serializer'],
  'transform': {
    // Transpile & type all .ts(x) files
    '^.+\\.tsx?$': 'ts-jest',
    // Transpile all .js files
    '^.+\\.js$': 'babel-jest',
  },
};
