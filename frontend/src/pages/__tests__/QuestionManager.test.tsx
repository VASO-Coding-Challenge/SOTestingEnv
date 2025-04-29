
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import QuestionManager from '../QuestionManager';

describe('QuestionManager', () => {
    beforeEach(() => {
        fetch.resetMocks();
    });
    test('renders the question manager', () => {
        //render(
        //    <MemoryRouter>
        //        <QuestionManager />
        //    </MemoryRouter>
        //);

        //expect(screen.getByText('Problem')).toBeInTheDocument();

    });


});

//notes
// npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest jest-environment-jsdom
// npm install --save-dev @babel/core @babel/preset-env @babel/preset-react


