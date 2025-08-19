import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Verify2FA() {
  const { verify2FA } = useAuth();
  const [code, setCode] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await verify2FA(code);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="2FA Code"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <button type="submit">Verify</button>
      {error && <p>{error}</p>}
    </form>
  );
}
