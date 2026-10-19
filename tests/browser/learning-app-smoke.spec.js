const { test, expect } = require("@playwright/test");

test.use({ browserName: "webkit" });

test("l’application charge les lexiques et le corpus de phrases", async ({ page }) => {
  const failedRequests = [];
  page.on("requestfailed", request => failedRequests.push(request.url() + " — " + request.failure()?.errorText));
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("http://127.0.0.1:4173/apprendre.html");
  await expect(page.getByRole("heading", { name: /Explorer les mots/i })).toBeVisible();
  await expect(page.locator("#results")).toBeAttached();
  await expect(page.locator("#sentence-results")).toBeAttached();
  await expect(page.locator("#entry-count")).toContainText("fiches", { timeout: 20000 });
  await expect.poll(() => page.locator("#results .word-card").count(), { timeout: 20000 }).toBeGreaterThan(0);
  await expect(page.locator("#sentence-count")).not.toContainText("Corpus indisponible");
  await expect.poll(() => page.locator("#sentence-results .sentence-card").count(), { timeout: 20000 }).toBeGreaterThan(0);

  const initialCards = await page.locator("#results .word-card").count();
  await page.locator("#search").fill("zzzxxyy-no-match");
  await expect(page.locator("#empty")).toBeVisible();
  await expect(page.locator("#results .word-card")).toHaveCount(0);
  await page.locator("#clear").click();
  await expect(page.locator("#results .word-card").first()).toBeVisible();
  expect(await page.locator("#results .word-card").count()).toBe(initialCards);
  expect(failedRequests).toEqual([]);
});

test("une fiche locale peut être ajoutée et retrouvée sans serveur", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("http://127.0.0.1:4173/apprendre.html");
  await expect(page.locator("#entry-count")).toContainText("fiches", { timeout: 20000 });
  await page.locator("#show-add-bottom").click();
  await page.locator("#entry-language").selectOption("soninke");
  await page.locator("#entry-word").fill("smoke-test-soninke");
  await page.locator("#entry-fr").fill("test navigateur");
  await page.locator("#entry-source").fill("Test automatisé local");
  await page.locator("#entry-form button[type='submit']").click();
  await expect(page.locator("#results .word-card h3").filter({ hasText: "smoke-test-soninke" })).toBeVisible();
  const stored = await page.evaluate(() => JSON.parse(localStorage.getItem("soninke-tts-libre-learning-v1") || "[]"));
  expect(stored.some(entry => entry.soninke?.word === "smoke-test-soninke" && entry.fr?.word === "test navigateur")).toBeTruthy();
});


test("le quiz de phrases propose une question et active la réponse", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("http://127.0.0.1:4173/apprendre.html");
  await expect(page.locator("#sentence-count")).toContainText("phrases", { timeout: 20000 });
  await page.locator("#quiz-mode").selectOption("sentence");
  await page.locator("#quiz-start").click();
  await expect(page.locator("#quiz-prompt")).not.toContainText("Préparation de la question", { timeout: 10000 });
  await expect(page.locator("#quiz-prompt")).not.toContainText("Appuyez sur", { timeout: 10000 });
  await expect(page.locator("#quiz-answer")).toBeEnabled();
  await expect(page.locator("#quiz-check")).toBeEnabled();
});
