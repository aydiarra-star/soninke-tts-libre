const { test, expect } = require("@playwright/test");

test("le lexique charge les entrées et un WAV est décodable par WebKit", async ({ page }) => {
  const failedRequests = [];
  page.on("requestfailed", request => failedRequests.push(request.url() + " — " + request.failure()?.errorText));
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("http://127.0.0.1:4173/lexique.html");
  await expect(page.locator("#lexicon-count")).toContainText("entrées", { timeout: 15000 });
  await expect(page.locator(".corpus-card").first()).toBeVisible();

  const audio = page.locator("audio.lexicon-audio-player").first();
  await expect(audio).toBeAttached();
  await audio.evaluate(element => {
    element.preload = "auto";
    element.load();
  });
  await expect.poll(
    () => audio.evaluate(element => ({
      source: element.currentSrc,
      readyState: element.readyState,
      duration: element.duration,
      error: element.error ? element.error.code : null
    })),
    { timeout: 15000, message: "Le navigateur doit décoder le WAV et obtenir sa durée." }
  ).toMatchObject({ readyState: expect.any(Number), error: null });

  const media = await audio.evaluate(element => ({
    source: element.currentSrc,
    readyState: element.readyState,
    duration: element.duration,
    error: element.error ? element.error.code : null
  }));
  expect(media.source).toContain("/audio/snk-");
  expect(media.readyState).toBeGreaterThanOrEqual(1);
  expect(Number.isFinite(media.duration)).toBeTruthy();
  expect(media.duration).toBeGreaterThan(0);
  expect(failedRequests).toEqual([]);
});

test("la page d’apprentissage et ses ressources statiques se chargent", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("http://127.0.0.1:4173/apprendre.html");
  await expect(page.getByRole("heading", { name: /Explorer les mots/i })).toBeVisible();
  await expect(page.locator("#results")).toBeAttached();
  await expect(page.locator("#sentence-results")).toBeAttached();
});
