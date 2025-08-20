import React, { useEffect, useState } from 'react';
import { fetchServers } from '../api';

/**
 * Displays a list of available VPN servers for the user to choose from.
 */
function ServerSelect() {
  const [servers, setServers] = useState([]);

  useEffect(() => {
    fetchServers().then(setServers).catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Select Server</h2>
      <ul>
        {servers.map((server) => (
          <li key={server.id || server.name}>{server.name || JSON.stringify(server)}</li>
        ))}
      </ul>
    </div>
  );
}

export default ServerSelect;
