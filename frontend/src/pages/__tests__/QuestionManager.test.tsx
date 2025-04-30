
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import QuestionManager from '../QuestionManager';

describe('QuestionManager', () => {
    beforeEach(() => {
        fetch.resetMocks();

        jest.spyOn(console, 'error').mockImplementation(() => {});

          
   
    });
    test('renders the question manager', () => {
        render(
            <MemoryRouter>
                <QuestionManager />
            </MemoryRouter>
        );


        expect(screen.getByText('Problem undefined')).toBeInTheDocument(); //no loaded data

        expect(screen.getByText('Create')).toBeInTheDocument();
        expect(screen.getByText('Docs')).toBeInTheDocument();
        const switchButton = screen.getByRole('button', { name: /Starter/i });
        fireEvent.click(switchButton);
        expect(screen.getByText('Starter')).toHaveClass(
            'w-1/4 py-2 font-bold border-b-4 border-red-500 text-red-500'
          );

    });


});

//notes
// npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest jest-environment-jsdom
// npm install --save-dev @babel/core @babel/preset-env @babel/preset-react


