import api from '../api';

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
  [key: string]: any;
}

export async function register(payload: RegisterPayload): Promise<any> {
  try {
    const { data } = await api.post('/auth/register', payload);
    return data;
  } catch (error: any) {
    const message = error?.response?.data?.message || 'Registration failed';
    throw new Error(message);
  }
}
