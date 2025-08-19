import React from 'react';
import UserPanel from './components/UserPanel';

/**
 * Root application component for the web user portal.
 * Renders the home page and provides access to the user panel
 * where VPN/Proxy settings and payment flows live.
 */
function App() {
  return (
    <div>
      <h1>Home</h1>
      <UserPanel />
    </div>
  );
}

export default App;
