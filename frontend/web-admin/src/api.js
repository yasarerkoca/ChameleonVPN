// frontend/web-admin/src/api.js
import axios from 'axios';
import { notifyError } from './middleware.js';

// ==========================
// Axios Instance
// ==========================
const api = axios.create({
  baseURL: process.env.API_BASE_URL || '/api',
});

// ==========================
// Request Interceptor
// ==========================
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ==========================
// Response Interceptor
// ==========================
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error;

    if (response && response.status === 401 && !config._retry) {
      config._retry = true;
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) throw new Error('No refresh token');

        const { data } = await axios.post(
          `${process.env.API_BASE_URL || '/api'}/refresh`,
          { refreshToken }
        );

        localStorage.setItem('accessToken', data.accessToken);
        config.headers.Authorization = `Bearer ${data.accessToken}`;
        return api(config);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    if (response && (response.status === 429 || response.status >= 500)) {
      notifyError(response);
    }
    return Promise.reject(error);
  }
);

// ==========================
// Auth Functions
// ==========================
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

export const fetchSubscriptions = () =>
  api.get('/posts').then((res) => res.data);

export const fetchServers = () =>
  api.get('/albums').then((res) => res.data);

export const fetchLogs = () =>
  api.get('/comments').then((res) => res.data);

export default api;
