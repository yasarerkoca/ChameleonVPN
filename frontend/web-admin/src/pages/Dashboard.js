import React, { useEffect, useState } from 'react';
import { fetchTodo } from '../lib/api';

export default function Dashboard() {
  const [todo, setTodo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodo()
      .then(setTodo)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {error && <p>Error: {error}</p>}
      {todo && <p>{todo.title}</p>}
    </div>
  );
}
