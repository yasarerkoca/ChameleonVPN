import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

describe('API token refresh', () => {
  beforeEach(() => {
    process.env.API_BASE_URL = 'https://example.com';
    localStorage.clear();
    localStorage.setItem('accessToken', 'old');
    localStorage.setItem('refreshToken', 'refresh');
    jest.resetModules();
  });

  test('refreshes token on 401 and retries request', async () => {
    const { default: api, fetchTodo } = await import('../api.js');
    const mockApi = new MockAdapter(api);
    const mockBase = new MockAdapter(axios);

    mockApi.onGet('/todos/1').replyOnce(401);
    mockApi.onGet('/todos/1').replyOnce(200, { id: 1 });
    mockBase.onPost('https://example.com/refresh').reply(200, { accessToken: 'new' });

    const data = await fetchTodo();

    expect(data).toEqual({ id: 1 });
    expect(localStorage.getItem('accessToken')).toBe('new');
  });
});
