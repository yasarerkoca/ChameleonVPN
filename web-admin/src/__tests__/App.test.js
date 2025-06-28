import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders sidebar', () => {
  render(<App />);
  expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
});
