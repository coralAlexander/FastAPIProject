import { test, expect } from '@playwright/test';

test('Add new user after login', async ({ page }) => {
  // Переходим на страницу логина
  await page.goto('/login');

  // Выполняем логин
  await page.fill('input[placeholder="Enter username"]', 'admin');  // замени на свой рабочий username
  await page.fill('input[placeholder="Enter password"]', '123456');  // замени на свой password

  await page.click('button[type="submit"]');

  // Ждём переход на /adduser
  await page.waitForURL('**/adduser');

  // Теперь на странице Add User

  // Заполняем форму
  const randomUsername = `testuser_${Date.now()}`;
  const randomEmail = `testuser_${Date.now()}@test.com`;

  await page.fill('input[placeholder="Enter username"]', randomUsername);
  await page.fill('input[placeholder="Enter email"]', randomEmail);
  await page.fill('input[placeholder="Enter password"]', '123456');

  // Выбираем роль
  await page.selectOption('select', 'admin');

  // Кликаем Add User
  await page.click('button[type="submit"]');

  // Проверяем что notification с "User created!" появился
  await expect(page.locator('.notification')).toHaveText(/User created/i);
});
