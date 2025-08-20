import React, { useEffect, useState } from 'react';
import { fetchSubscriptions } from '../lib/api';

export default function Subscriptions() {
  const [subs, setSubs] = useState([]);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ title: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchSubscriptions()
      .then(setSubs)
      .catch((e) => setError(e.message));
  }, []);
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await updateSubscription(editingId, form);
        setSubs((prev) =>
          prev.map((s) => (s.id === editingId ? { ...s, ...updated } : s))
        );
      } else {
        const created = await createSubscription(form);
        setSubs((prev) => [...prev, created]);
      }
      setForm({ title: '' });
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const startEdit = (sub) => {
    setEditingId(sub.id);
    setForm({ title: sub.title || '' });
  };

  const handleDelete = async (id) => {
    try {
      await deleteSubscription(id);
      setSubs((prev) => prev.filter((s) => s.id !== id));
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
      <h1>Subscriptions</h1>
      {error && <p>Error: {error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Subscription title"
        />
        <button type="submit">{editingId ? 'Update' : 'Create'}</button>
        {editingId && (
          <button type="button" onClick={cancelEdit}>
            Cancel
          </button>
        )}
      </form>
      <ul>
        {subs.map((s) => (
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
