import { render, screen, waitFor } from '@testing-library/react';
import Users from '../pages/Users';
import * as api from '../api';

afterEach(() => {
  jest.restoreAllMocks();
});

test('renders users from api', async () => {
  jest.spyOn(api, 'fetchUsers').mockResolvedValue([{ id: 1, name: 'Jane' }]);
  render(<Users />);
  expect(screen.getByText(/users/i)).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText('Jane')).toBeInTheDocument());
});
