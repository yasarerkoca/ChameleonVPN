import axios from 'axios';

// Basic axios instance for the user-facing app
const api = axios.create({
  baseURL: process.env.API_BASE_URL || '/api',
});

// Fetch available VPN servers
export const fetchServers = () =>
  api.get('/servers').then((res) => res.data);

// Retrieve the current user's profile
export const fetchProfile = () =>
  api.get('/profile').then((res) => res.data);

// Update the current user's profile
export const updateProfile = (profile) =>
  api.put('/profile', profile).then((res) => res.data);

// Retrieve the current user's keys
export const fetchKeys = () =>
  api.get('/keys').then((res) => res.data);

// Download VPN configuration
export const downloadConfig = () =>
  api.get('/config', { responseType: 'blob' }).then((res) => res.data);

export default api;
