// src/pages/__tests__/LoginPage.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import LoginPage from '../Login';

describe('LoginPage', () => {
  beforeEach(() => {
    fetch.resetMocks();
  });
  test('renders the login page title and subtitle', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    expect(screen.getByText('Virginia Science Olympiad')).toBeInTheDocument();
    expect(screen.getByText('Please Sign in')).toBeInTheDocument();
    expect(screen.getByText('Team Number')).toBeInTheDocument();
  });
  test('clicking the button triggers the expected action', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ success: true }),
      })
    );
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    const switchButton = screen.getByRole('button', { name: /switch/i });
    fireEvent.click(switchButton);
    expect(screen.getByText('Event Supervisor')).toBeInTheDocument();
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });
    // Error: Incorrect credentials. Please try again
  });
});

//notes
// npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest jest-environment-jsdom
// npm install --save-dev @babel/core @babel/preset-env @babel/preset-react


