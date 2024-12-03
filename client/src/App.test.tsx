import React from 'react';
import { test } from 'vitest';
import { render, screen } from '@testing-library/react';

import App from './App';

test('renders sample app landing page', () => {
  render(<App />);
  const linkElement = screen.getByText(/patient information/i);
  expect(linkElement).toBeInTheDocument();
});
