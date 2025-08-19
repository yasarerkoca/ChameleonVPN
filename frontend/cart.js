const { add, multiply } = require('./math');

function calculateCartTotal(items) {
  return items.reduce((total, item) => add(total, multiply(item.price, item.qty)), 0);
}

module.exports = { calculateCartTotal };
