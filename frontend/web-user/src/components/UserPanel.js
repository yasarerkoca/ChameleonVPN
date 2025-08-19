import React from 'react';
import { Link } from 'react-router-dom';
import VPNProxySettings from './VPNProxySettings';
import PaymentFlow from './PaymentFlow';

/**
 * UserPanel aggregates user specific features such as
 * configuring VPN/Proxy settings and handling payments.
 * It also provides navigation to other user tools.
 */
function UserPanel() {
  return (
    <section>
      <h2>User Panel</h2>
      <nav>
        <ul>
          <li><Link to="/servers">Select Server</Link></li>
          <li><Link to="/profile">Profile</Link></li>
          <li><Link to="/keys">Keys</Link></li>
          <li><Link to="/downloads">Downloads</Link></li>
        </ul>
      </nav>
      <VPNProxySettings />
      <PaymentFlow />
    </section>
  );
}

export default UserPanel;
