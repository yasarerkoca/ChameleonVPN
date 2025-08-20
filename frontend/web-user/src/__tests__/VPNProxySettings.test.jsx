import { render, screen, fireEvent } from '@testing-library/react';
import VPNProxySettings from '../components/VPNProxySettings';

test('toggles vpn setting', () => {
  render(<VPNProxySettings />);
  const checkbox = screen.getByLabelText(/enable vpn/i);
  fireEvent.click(checkbox);
  expect(checkbox.checked).toBe(true);
});
