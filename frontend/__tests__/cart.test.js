const { calculateCartTotal } = require('../cart');

test('calculates total for cart items', () => {
  const items = [
    { price: 10, qty: 2 },
    { price: 5, qty: 3 }
  ];
  expect(calculateCartTotal(items)).toBe(10 * 2 + 5 * 3);
});
