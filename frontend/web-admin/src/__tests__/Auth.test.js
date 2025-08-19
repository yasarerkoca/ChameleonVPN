import { login, setAuthTokens } from '../api';

describe('authentication helpers', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('login stores tokens', async () => {
    await login('admin', 'secret');
    expect(localStorage.getItem('accessToken')).toBe('admin-token');
    expect(localStorage.getItem('refreshToken')).toBe('admin-refresh');
  });

  test('setAuthTokens persists tokens', () => {
    setAuthTokens({ accessToken: 'a', refreshToken: 'b' });
    expect(localStorage.getItem('accessToken')).toBe('a');
    expect(localStorage.getItem('refreshToken')).toBe('b');
  });
});
