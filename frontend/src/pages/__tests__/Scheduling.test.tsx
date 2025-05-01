
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import Scheduling from '../Scheduling';

describe('Scheduling', () => {
    beforeEach(() => {
        fetch.resetMocks();

        jest.spyOn(console, 'error').mockImplementation(() => {});

          
   
    });
    test('renders the scheduling',  () => {
        window.alert = jest.fn();
        render(
            <MemoryRouter>
                <Scheduling />
            </MemoryRouter>
        );


        expect(screen.getByText('View and manage all sessions')).toBeInTheDocument(); //no loaded data

        expect(screen.getByText('Teams')).toBeInTheDocument();
        expect(screen.getByText('Create Session')).toBeInTheDocument();
        //const switchButton = container.querySelector('.text-\\[\\#FE7A7A\\]')

        const submitButton = screen.getByRole('button', { name: /CREATE/i });
    
        fireEvent.click(submitButton);
        expect(window.alert).toHaveBeenCalledWith("Please fill out all fields");

    });


});

//notes
// npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest jest-environment-jsdom
// npm install --save-dev @babel/core @babel/preset-env @babel/preset-react


