import { test, expect } from '@playwright/test';

test('user toggles vpn and submits payment', async ({ page }) => {
  await page.setContent(`
    <div>
      <label><input id="vpn" type="checkbox" />Enable VPN</label>
      <form id="pay">
        <input id="amount" />
        <button>Pay</button>
      </form>
      <div id="msg"></div>
    </div>
    <script>
      document.getElementById('pay').addEventListener('submit', e => {
        e.preventDefault();
        document.getElementById('msg').textContent = 'Payment submitted';
      });
    </script>
  `);
  await page.check('#vpn');
  await expect(page.locator('#vpn')).toBeChecked();
  await page.fill('#amount', '10');
  await page.click('button');
  await expect(page.locator('#msg')).toHaveText('Payment submitted');
});
