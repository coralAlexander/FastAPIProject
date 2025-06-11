import { test, expect } from '@playwright/test';

test('Login with valid credentials', async ({ page }) => {
  await page.goto('/login');

  await page.fill('input[placeholder="Enter username"]', 'admin');
  await page.fill('input[placeholder="Enter password"]', '123456');

  await page.click('button[type="submit"]');

  await expect(page.locator('.notification')).toHaveText(/Login successful/i);

  await page.waitForURL('**/adduser');
});
