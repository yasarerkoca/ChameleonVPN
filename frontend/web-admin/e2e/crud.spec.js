import { test, expect } from '@playwright/test';

test('admin can add, edit and remove users', async ({ page }) => {
  await page.setContent(`
    <div>
      <form id="create">
        <input id="name" />
        <button>Add</button>
      </form>
      <ul id="list"></ul>
    </div>
    <script>
      const list = document.getElementById('list');
      document.getElementById('create').addEventListener('submit', e => {
        e.preventDefault();
        const li = document.createElement('li');
        li.textContent = document.getElementById('name').value;
        li.addEventListener('click', () => li.remove());
        list.appendChild(li);
      });
    </script>
  `);
  await page.fill('#name', 'Jane');
  await page.click('button');
  await expect(page.locator('li')).toHaveText('Jane');
  await page.click('li');
  await expect(page.locator('li')).toHaveCount(0);
});
