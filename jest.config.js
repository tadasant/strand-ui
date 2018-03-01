module.exports = {
  'testMatch': [
    // e.g. some_test.test.js or some_ts_test.tsx
    '**/?(*.)(spec|test).(j|t)s?(x)',
  ],
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
  'setupTestFrameworkScriptFile': '<rootDir>/test/setup.ts',
  'moduleNameMapper': {
    // Mock all these filetypes
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/test/__mocks__/fileMock.ts',
  },
  // Helpers for ease of serializing snapshots
  'snapshotSerializers': ['enzyme-to-json/serializer'],
  'transform': {
    // Transpile & type all .ts(x) files
    '^.+\\.tsx?$': 'ts-jest',
  },
};
