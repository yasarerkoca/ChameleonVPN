import axios from 'axios';
import { notifyError } from './middleware.js';

const API_BASE = process.env.API_BASE_URL || '/api';

let accessToken = localStorage.getItem('accessToken');
let refreshToken = localStorage.getItem('refreshToken');

export function setAuthTokens(tokens) {
  accessToken = tokens.accessToken;
  refreshToken = tokens.refreshToken;
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
}

export function clearAuthTokens() {
  accessToken = null;
  refreshToken = null;
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  // Refresh token'ı kara listeye eklemek için backend'de
  // /auth/logout endpoint'ini çağırın.
}
const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error;
    if (response && response.status === 401 && !config._retry) {
      config._retry = true;
      try {
        if (!refreshToken) throw new Error('No refresh token');
        const { data } = await axios.post(`${API_BASE}/auth/refresh`, { refresh_token: refreshToken });
        setAuthTokens({ accessToken: data.access_token, refreshToken: data.refresh_token ?? refreshToken });
        config.headers.Authorization = `Bearer ${data.access_token}`;
        return api(config);
      } catch (refreshError) {
        clearAuthTokens();
        return Promise.reject(refreshError);
      }
    }
    if (response && (response.status === 429 || response.status >= 500)) {
      notifyError(response);
    }
    return Promise.reject(error);
  }
);
export async function login(username, password) {
  const { data } = await api.post('/auth/login', { email: username, password });
  const tokens = {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
  };
  setAuthTokens(tokens);
  return tokens;
}

// ==========================
// API Calls
// ==========================
export const fetchTodo = () =>
  api.get('/admin/status-management/health').then((res) => res.data);

export const fetchUsers = () =>
  api.get('/admin/user-management/users').then((res) => res.data);

// CRUD helpers for user management used in admin flows
export const createUser = (user) =>
  api.post('/admin/user-management/users', user).then((res) => res.data);

export const updateUser = (id, user) =>
  api.put(`/admin/user-management/users/${id}`, user).then((res) => res.data);

export const deleteUser = (id) =>
  api.delete(`/admin/user-management/users/${id}`).then((res) => res.status === 200);

export const fetchSubscriptions = () =>
  api.get('/membership/plan-list').then((res) => res.data);

export const fetchServers = () =>
  api.get('/vpn/server').then((res) => res.data);

export const fetchLogs = () =>
  api.get('/admin/ai-selection-log').then((res) => res.data);

export default api;
