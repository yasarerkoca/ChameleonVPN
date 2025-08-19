import api, { setAuthTokens } from '../api';

export interface Verify2FAResponse {
  accessToken?: string;
  refreshToken?: string;
  [key: string]: any;
}

export async function verify2FA(code: string): Promise<Verify2FAResponse> {
  try {
    const { data } = await api.post<Verify2FAResponse>('/auth/verify-2fa', { code });
    if (data.accessToken && data.refreshToken) {
      setAuthTokens(data as any);
    }
    return data;
  } catch (error: any) {
    const message = error?.response?.data?.message || '2FA verification failed';
    throw new Error(message);
  }
}
