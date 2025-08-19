import axios from 'axios';
import { notifyError } from '../middleware.js';

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
        const { data } = await axios.post(
          `${API_BASE}/refresh`,
          { refreshToken }
        );
        setAuthTokens({ accessToken: data.accessToken, refreshToken: data.refreshToken ?? refreshToken });
        config.headers.Authorization = `Bearer ${data.accessToken}`;
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

async function request(config) {
  const response = await api(config);
  return response.data;
}

export const get = (url, config) => request({ ...config, method: 'get', url });

export const post = (url, data, config) =>
  request({ ...config, method: 'post', url, data });

export const fetchTodo = () => get('/todos/1');
export const fetchUsers = () => get('/users');
export const fetchSubscriptions = () => get('/posts');
export const fetchServers = () => get('/albums');
export const fetchLogs = () => get('/comments');

export async function login(username, password) {
  const tokens = {
    accessToken: `${username}-token`,
    refreshToken: `${username}-refresh`,
  };
  setAuthTokens(tokens);
  return tokens;
}

export default api;
