// src/pages/__tests__/LoginPage.test.jsx
import React from 'react';

import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import LoginPage from '../Login';

describe('LoginPage', () => {
  test('renders the login page title and subtitle', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    expect(screen.getByText('Virginia Science Olympiad')).toBeInTheDocument();
    expect(screen.getByText('Please Sign in')).toBeInTheDocument();
  });
});

