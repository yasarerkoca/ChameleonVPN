import api from '../api';

export async function verifyEmail(token: string): Promise<any> {
  try {
    const { data } = await api.post('/auth/verify-email', { token });
    return data;
  } catch (error: any) {
    const message = error?.response?.data?.message || 'Email verification failed';
    throw new Error(message);
  }
}
