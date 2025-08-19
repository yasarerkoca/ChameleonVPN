import api, { setAuthTokens } from '../api';

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  [key: string]: any;
}

export async function login(username: string, password: string): Promise<LoginResponse> {
  try {
    const { data } = await api.post<LoginResponse>('/auth/login', { username, password });
    setAuthTokens(data);
    return data;
  } catch (error: any) {
    const message = error?.response?.data?.message || 'Login failed';
    throw new Error(message);
  }
}
