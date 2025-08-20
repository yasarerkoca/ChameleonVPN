import React, { useEffect, useState } from 'react';
import { fetchLogs } from '../lib/api';

export default function Logs() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ body: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchLogs()
      .then(setLogs)
      .catch((e) => setError(e.message));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await updateLog(editingId, form);
        setLogs((prev) =>
          prev.map((l) => (l.id === editingId ? { ...l, ...updated } : l))
        );
      } else {
        const created = await createLog(form);
        setLogs((prev) => [...prev, created]);
      }
      setForm({ body: '' });
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (log) => {
    setEditingId(log.id);
    setForm({ body: log.body || '' });
  };

  const handleDelete = async (id) => {
    try {
      await deleteLog(id);
      setLogs((prev) => prev.filter((l) => l.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm({ body: '' });
  };

  return (
    <div>
      <h1>Logs</h1>
      {error && <p>Error: {error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="body"
          value={form.body}
          onChange={handleChange}
          placeholder="Log body"
        />
        <button type="submit">{editingId ? 'Update' : 'Create'}</button>
        {editingId && (
          <button type="button" onClick={cancelEdit}>
            Cancel
          </button>
        )}
      </form>
      <ul>
        {logs.map((l) => (
          <li key={l.id}>
            {l.body || l.title}
            <button onClick={() => startEdit(l)}>Edit</button>
            <button onClick={() => handleDelete(l.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
