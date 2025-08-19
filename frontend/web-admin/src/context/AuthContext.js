import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);

  const login = async (username, password) => {
    // Simulate login; in real world this would call an API
    const fakeToken = `${username}-token`;
    setToken(fakeToken);
    return fakeToken;
  };

  const value = { token, login };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
