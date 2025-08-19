import React, { useState } from 'react';
import { post } from '../lib/api';

/**
 * Mock payment flow demonstrating how a user might submit
 * a payment amount and method. In a real application this
 * would integrate with a payment provider.
 */
function PaymentFlow() {
  const [amount, setAmount] = useState('');
  const [method, setMethod] = useState('credit');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitted(true);
    try {
      await post('/payments', { amount, method });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Payment</h3>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <select value={method} onChange={(e) => setMethod(e.target.value)}>
        <option value="credit">Credit Card</option>
        <option value="paypal">PayPal</option>
      </select>
      <button type="submit">Pay</button>
      {submitted && <div>Payment submitted</div>}
    </form>
  );
}

export default PaymentFlow;
