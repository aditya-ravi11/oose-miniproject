import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import NewRequest from '../pages/NewRequest';

describe('NewRequest wizard', () => {
  it('navigates between steps', () => {
    render(
      <MemoryRouter>
        <NewRequest />
      </MemoryRouter>
    );

    expect(screen.getByText(/Step 1 of 3/)).toBeInTheDocument();
    fireEvent.click(screen.getByText('Next'));
    expect(screen.getByText(/Step 2 of 3/)).toBeInTheDocument();
  });
});
