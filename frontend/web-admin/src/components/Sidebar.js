import React from 'react';
import { Link } from 'react-router-dom';

export default function Sidebar() {
  return (
    <aside>
      <nav>
        <ul>
          <li>
            <Link to="/">Dashboard</Link>
          </li>
          <li>
            <Link to="/users">Users</Link>
          </li>
          <li>
            <Link to="/subscriptions">Subscriptions</Link>
          </li>
          <li>
            <Link to="/servers">Servers</Link>
          </li>
          <li>
            <Link to="/logs">Logs</Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
