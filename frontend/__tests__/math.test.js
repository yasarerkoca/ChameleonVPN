const { add, multiply } = require('../math');

test('add adds numbers', () => {
  expect(add(1, 2)).toBe(3);
});

test('multiply multiplies numbers', () => {
  expect(multiply(3, 4)).toBe(12);
});
