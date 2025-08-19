@@ -60,35 +60,45 @@ api.interceptors.response.use(
export function setAuthTokens(tokens) {
  localStorage.setItem('accessToken', tokens.accessToken);
  localStorage.setItem('refreshToken', tokens.refreshToken);
}

export async function login(username, password) {
  // Burayı gerçek backend login endpointine bağlamalısın.
  // Şimdilik dummy token üretiyoruz.
  const tokens = {
    accessToken: `${username}-token`,
    refreshToken: `${username}-refresh`,
  };
  setAuthTokens(tokens);
  return tokens;
}

// ==========================
// Example API Calls
// ==========================
export const fetchTodo = () =>
  api.get('/todos/1').then((res) => res.data);

export const fetchUsers = () =>
  api.get('/users').then((res) => res.data);

// CRUD helpers for user management used in admin flows
export const createUser = (user) =>
  api.post('/users', user).then((res) => res.data);

export const updateUser = (id, user) =>
  api.put(`/users/${id}`, user).then((res) => res.data);

export const deleteUser = (id) =>
  api.delete(`/users/${id}`).then((res) => res.status === 200);

export const fetchSubscriptions = () =>
  api.get('/posts').then((res) => res.data);

export const fetchServers = () =>
  api.get('/albums').then((res) => res.data);

export const fetchLogs = () =>
  api.get('/comments').then((res) => res.data);

export default api;
