# test_login.py
import requests
from playwright.sync_api import sync_playwright


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://localhost:3000/login")

        page.fill('input[placeholder="Enter username"]', 'admin')
        page.fill('input[placeholder="Enter password"]', '123456')

        page.click('button[type="submit"]')

        page.wait_for_url('**/adduser')

        assert "adduser" in page.url


        # Проверяем что notification появился
        notification = page.locator(".notification").inner_text()
        assert "User created" in notification or "Login successful! Redirecting..." in notification

        browser.close()



def delete_by_username(username):
    # Пример API → ты должен сделать такой endpoint
    # DELETE /users/by-username/{username}
    response = requests.delete(f"{"http://localhost:8000"}/users/remove/{username}")
    print(f"Cleanup delete user {username} → status {response.status_code}")

def test_add_user():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Переход на страницу логина
        page.goto("http://localhost:3000/login")

        # Логин
        page.fill('input[placeholder="Username"]', 'admin')
        page.fill('input[placeholder="Password"]', '123456')

        page.click('button[type="submit"]')

        # Ждем переход на /adduser
        page.wait_for_url('**/home')

        # Проверяем что заголовок Add User есть
        page.wait_for_selector('h2', timeout=5000)
        add_user_header = page.locator('h2').inner_text()
        assert add_user_header.strip() == 'Add User'

        # Заполняем форму
        random_username = f"pythontest_{page.evaluate('Date.now()')}"
        random_email = f"pythontest_{random_username}@test.com"

        page.fill('input[placeholder="Enter username"]', random_username)
        page.fill('input[placeholder="Enter email"]', random_email)
        page.fill('input[placeholder="Enter password"]', 'TestPassword123')

        page.select_option('select', 'user')

        # Отправляем форму
        page.click('button[type="submit"]')

        # Ждем появления notification
        page.wait_for_selector(".notification", timeout=5000)

        # Проверяем текст notification
        notification = page.locator(".notification").inner_text()
        assert "User created" in notification or "Login successful" in notification

        delete_by_username(random_username)


        browser.close()