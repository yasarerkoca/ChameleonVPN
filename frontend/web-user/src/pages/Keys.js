import React, { useEffect, useState } from 'react';
import { fetchKeys } from '../api';

/**
 * Fetches and displays user access keys.
 */
function Keys() {
  const [keys, setKeys] = useState([]);

  useEffect(() => {
    fetchKeys().then(setKeys).catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Keys</h2>
      <ul>
        {keys.map((k) => (
          <li key={k.id || k}>{k.value || k}</li>
        ))}
      </ul>
    </div>
  );
}

export default Keys;
