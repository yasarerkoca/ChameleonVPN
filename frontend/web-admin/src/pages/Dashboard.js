import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchTodo } from '../api';

export default function Dashboard() {
  const { token } = useAuth();
  const [todo, setTodo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodo(token)
      .then(setTodo)
      .catch((e) => setError(e.message));
  }, [token]);

  return (
    <div>
      <h1>Dashboard</h1>
      {error && <p>Error: {error}</p>}
      {todo && <p>{todo.title}</p>}
    </div>
  );
}
