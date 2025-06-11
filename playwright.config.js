// playwright.config.js

import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './playtest',
  timeout: 30000,
  retries: 0,
  use: {
    headless: false, // показывать браузер (можно поставить true на CI)
    viewport: { width: 1280, height: 720 },
    actionTimeout: 10000,
    ignoreHTTPSErrors: true,
    video: 'on-first-retry',
    baseURL: 'http://localhost:3000', // удобно — можно писать page.goto('/')
  },
});
