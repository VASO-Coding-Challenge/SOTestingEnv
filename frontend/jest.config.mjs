export default {
    testEnvironment: 'jsdom',
    //transform: {
    //  '^.+\\.[jt]sx?$': 'babel-jest',
    //},
    transform: {
      "^.+\\.(js|jsx|ts|tsx)$": "babel-jest"
    },
    transformIgnorePatterns: [
      "/node_modules/(?!lucide-react)/"
    ],
    moduleNameMapper: {
      // optional: handle imports like "@/components/..."
      "^@/(.*)$": "<rootDir>/src/$1"
    },
    moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx'],

    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1', // Adjust as needed
    },

  };