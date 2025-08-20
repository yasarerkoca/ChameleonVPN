import React, { useEffect, useState } from 'react';
import { fetchUsers } from '../lib/api';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ name: '', role: 'user' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch((e) => setError(e.message));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await updateUser(editingId, form);
        setUsers((prev) =>
          prev.map((u) => (u.id === editingId ? { ...u, ...updated } : u))
        );
      } else {
        const created = await createUser(form);
        setUsers((prev) => [...prev, created]);
      }
      setForm({ name: '', role: 'user' });
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (user) => {
    setEditingId(user.id);
    setForm({ name: user.name || '', role: user.role || 'user' });
  };

  const handleDelete = async (id) => {
    try {
      await deleteUser(id);
      setUsers((prev) => prev.filter((u) => u.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm({ name: '', role: 'user' });
  };

  return (
    <div>
      <h1>Users</h1>
      {error && <p>Error: {error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
        />
        <select name="role" value={form.role} onChange={handleChange}>
          <option value="user">user</option>
          <option value="admin">admin</option>
          <option value="moderator">moderator</option>
        </select>
        <button type="submit">{editingId ? 'Update' : 'Create'}</button>
        {editingId && (
          <button type="button" onClick={cancelEdit}>
            Cancel
          </button>
        )}
      </form>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.name} - {u.role || 'user'}
            <button onClick={() => startEdit(u)}>Edit</button>
            <button onClick={() => handleDelete(u.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
