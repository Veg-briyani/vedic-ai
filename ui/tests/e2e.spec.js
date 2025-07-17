import { test, expect } from '@playwright/test';

test('receive rules → rate thumbs-up', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.waitForSelector('.rule-card');
  const cards = await page.locator('.rule-card').count();
  expect(cards).toBeGreaterThan(0);
  // Simulate rating the first rule
  const firstCard = page.locator('.rule-card').first();
  await firstCard.locator('input[type=range]').fill('5');
  await firstCard.locator('button').click();
  // Accept alert
  await page.waitForEvent('dialog').then(dialog => dialog.accept());
}); 