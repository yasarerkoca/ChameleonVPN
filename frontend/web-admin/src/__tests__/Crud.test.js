import MockAdapter from 'axios-mock-adapter';
import api, { createUser, updateUser, deleteUser } from '../api';

describe('admin user CRUD operations', () => {
  let mock;
  beforeEach(() => {
    mock = new MockAdapter(api);
  });
  afterEach(() => {
    mock.restore();
  });

  test('creates a user', async () => {
    mock.onPost('/users').reply(200, { id: 1, name: 'Jane' });
    const data = await createUser({ name: 'Jane' });
    expect(data).toEqual({ id: 1, name: 'Jane' });
  });

  test('updates a user', async () => {
    mock.onPut('/users/1').reply(200, { id: 1, name: 'Janet' });
    const data = await updateUser(1, { name: 'Janet' });
    expect(data.name).toBe('Janet');
  });

  test('deletes a user', async () => {
    mock.onDelete('/users/1').reply(200);
    const ok = await deleteUser(1);
    expect(ok).toBe(true);
  });
});
