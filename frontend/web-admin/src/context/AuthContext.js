import React, { createContext, useContext, useState } from 'react';
import { login as apiLogin } from '../api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);

  const login = async (username, password) => {
    const { accessToken } = await apiLogin(username, password);
    setToken(accessToken);
    return accessToken;
  };

  const value = { token, login };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
