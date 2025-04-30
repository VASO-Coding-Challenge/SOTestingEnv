
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import TeamManager from '../TeamManager';

describe('TeamManager', () => {
    beforeEach(() => {
        fetch.resetMocks();

        jest.spyOn(console, 'error').mockImplementation(() => {});

          
   
    });
    test('renders the team manager', () => {
        render(
            <MemoryRouter>
                <TeamManager />
            </MemoryRouter>
        );


        expect(screen.getByText('Team Name')).toBeInTheDocument(); //no loaded data

        expect(screen.getByText('Manage all competition teams')).toBeInTheDocument();
        expect(screen.getByText('Download Scores')).toBeInTheDocument();
        const switchButton = screen.getByRole('button', { name: /Delete All Teams/i });
        fireEvent.click(switchButton);
        expect(screen.getByText('Are you sure you want to delete all teams?')).toBeInTheDocument();

    });


});

//notes
// npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest jest-environment-jsdom
// npm install --save-dev @babel/core @babel/preset-env @babel/preset-react


