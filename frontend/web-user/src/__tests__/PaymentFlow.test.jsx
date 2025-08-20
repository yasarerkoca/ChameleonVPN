import { render, screen, fireEvent } from '@testing-library/react';
import PaymentFlow from '../components/PaymentFlow';

test('submits payment and shows confirmation', () => {
  render(<PaymentFlow />);
  fireEvent.change(screen.getByPlaceholderText(/amount/i), { target: { value: '10' } });
  fireEvent.click(screen.getByText(/pay/i));
  expect(screen.getByText(/payment submitted/i)).toBeInTheDocument();
});
