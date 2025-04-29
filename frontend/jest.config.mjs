export default {
    testEnvironment: 'jsdom',
    transform: {
      '^.+\\.[jt]sx?$': 'babel-jest',
    },
    moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx'],

    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1', // Adjust as needed
    },

  };