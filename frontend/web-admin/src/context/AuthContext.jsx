import React, { createContext, useContext, useState } from 'react';
import { login as apiLogin } from '../lib/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [isRegistered, setIsRegistered] = useState(false);
  const [emailVerified, setEmailVerified] = useState(false);
  const [twoFAVerified, setTwoFAVerified] = useState(false);

  const login = async (username, password) => {
    const { accessToken } = await apiLogin(username, password);
    setToken(accessToken);
    return accessToken;
  };

  const register = async (payload) => {
    await api.post('/auth/register', payload);
    setIsRegistered(true);
  };

  const verifyEmail = async (tokenValue) => {
    await api.post('/auth/verify-email', { token: tokenValue });
    setEmailVerified(true);
  };

  const verify2FA = async (code) => {
    const { data } = await api.post('/auth/verify-2fa', { code });
    if (data.accessToken) {
      setToken(data.accessToken);
    }
    setTwoFAVerified(true);
    return data;
  };

  const value = {
    token,
    login,
    register,
    verifyEmail,
    verify2FA,
    isRegistered,
    emailVerified,
    twoFAVerified,
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
export function useRegister() {
  return useContext(AuthContext).register;
}

export function useVerifyEmail() {
  return useContext(AuthContext).verifyEmail;
}

export function useVerify2FA() {
  return useContext(AuthContext).verify2FA;
}

