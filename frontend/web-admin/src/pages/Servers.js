import React, { useEffect, useState } from 'react';
import { fetchServers } from '../lib/api';

export default function Servers() {
  const [servers, setServers] = useState([]);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ title: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchServers()
      .then(setServers)
      .catch((e) => setError(e.message));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await updateServer(editingId, form);
        setServers((prev) =>
          prev.map((s) => (s.id === editingId ? { ...s, ...updated } : s))
        );
      } else {
        const created = await createServer(form);
        setServers((prev) => [...prev, created]);
      }
      setForm({ title: '' });
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (server) => {
    setEditingId(server.id);
    setForm({ title: server.title || '' });
  };

  const handleDelete = async (id) => {
    try {
      await deleteServer(id);
      setServers((prev) => prev.filter((s) => s.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm({ title: '' });
  };


  return (
    <div>
      <h1>Servers</h1>
      {error && <p>Error: {error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Server name"
        />
        <button type="submit">{editingId ? 'Update' : 'Create'}</button>
        {editingId && (
          <button type="button" onClick={cancelEdit}>
            Cancel
          </button>
        )}
      </form>
      <ul>
        {servers.map((s) => (
          <li key={s.id}>
            {s.title}
            <button onClick={() => startEdit(s)}>Edit</button>
            <button onClick={() => handleDelete(s.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
