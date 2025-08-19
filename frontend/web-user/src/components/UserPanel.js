import React from 'react';
import VPNProxySettings from './VPNProxySettings';
import PaymentFlow from './PaymentFlow';

/**
 * UserPanel aggregates user specific features such as
 * configuring VPN/Proxy settings and handling payments.
 */
function UserPanel() {
  return (
    <section>
      <h2>User Panel</h2>
      <VPNProxySettings />
      <PaymentFlow />
    </section>
  );
}

export default UserPanel;
