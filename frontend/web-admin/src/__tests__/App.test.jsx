import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MockAdapter from 'axios-mock-adapter';
import api from '../api.js';
import App from '../App';

test('shows dashboard after login', async () => {
  const mock = new MockAdapter(api);
  mock.onPost('/auth/login').reply(200, {
    accessToken: 'token',
    refreshToken: 'refresh',
  });
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
