import { render, screen } from '@testing-library/react';
import App from '../web-user/src/App';

test('renders Ana Sayfa', () => {
  render(<App />);
  expect(screen.getByText(/VPN’e Hoşgeldin/i)).toBeInTheDocument();
});
