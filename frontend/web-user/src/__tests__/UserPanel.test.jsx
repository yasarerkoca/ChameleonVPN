import { render, screen } from '@testing-library/react';
import UserPanel from '../components/UserPanel';

test('renders portal features', () => {
  render(<UserPanel />);
  expect(screen.getByText(/user panel/i)).toBeInTheDocument();
  expect(screen.getByText(/vpn & proxy settings/i)).toBeInTheDocument();
  expect(screen.getByText(/payment/i)).toBeInTheDocument();
});
