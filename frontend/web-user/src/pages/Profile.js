import React, { useEffect, useState } from 'react';
import { fetchProfile, updateProfile } from '../api';

/**
 * Allows the user to view and update basic profile information.
 */
function Profile() {
  const [profile, setProfile] = useState({ name: '', email: '' });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetchProfile().then(setProfile).catch((err) => console.error(err));
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    updateProfile(profile)
      .then(() => setSaved(true))
      .catch((err) => console.error(err));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Profile</h2>
      <input
        name="name"
        placeholder="Name"
        value={profile.name}
        onChange={handleChange}
      />
      <input
        name="email"
        placeholder="Email"
        value={profile.email}
        onChange={handleChange}
      />
      <button type="submit">Save</button>
      {saved && <div>Profile saved</div>}
    </form>
  );
}

export default Profile;
