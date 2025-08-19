import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';

test('shows dashboard after login', async () => {
  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/username/i), {
    target: { value: 'admin' },
  });
  fireEvent.change(screen.getByPlaceholderText(/password/i), {
    target: { value: 'secret' },
  });
  fireEvent.click(screen.getByText(/login/i));
  await waitFor(() => {
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });
});
