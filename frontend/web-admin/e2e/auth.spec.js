import { test, expect } from '@playwright/test';

test('login with 2FA displays dashboard', async ({ page }) => {
  await page.setContent(`
    <form id="login">
      <input id="user" />
      <input id="pass" type="password" />
      <input id="code" />
      <button>Login</button>
    </form>
    <div id="result"></div>
    <script>
      document.getElementById('login').addEventListener('submit', e => {
        e.preventDefault();
        const code = document.getElementById('code').value;
        document.getElementById('result').textContent =
          code === '123456' ? 'Dashboard' : 'Invalid 2FA';
      });
    </script>
  `);
  await page.fill('#user', 'admin');
  await page.fill('#pass', 'secret');
  await page.fill('#code', '123456');
  await page.click('button');
  await expect(page.locator('#result')).toHaveText('Dashboard');
});
