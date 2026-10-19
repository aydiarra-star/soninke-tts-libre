const { test, expect } = require("@playwright/test");

test.use({ browserName: "webkit" });

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
    () => audio.evaluate(element => element.readyState),
    { timeout: 15000, message: "WebKit doit charger les métadonnées du WAV." }
  ).toBeGreaterThanOrEqual(1);
  await expect.poll(
    () => audio.evaluate(element => Number.isFinite(element.duration) && element.duration > 0),
    { timeout: 15000, message: "WebKit doit décoder une durée audio positive." }
  ).toBeTruthy();

  const media = await audio.evaluate(element => ({
    source: element.currentSrc,
    readyState: element.readyState,
    duration: element.duration,
    error: element.error ? element.error.code : null
  }));
  expect(media.source).toContain("/audio/snk-");
  expect(media.readyState).toBeGreaterThanOrEqual(1);
  expect(media.duration).toBeGreaterThan(0);
  expect(media.error).toBeNull();
  expect(failedRequests).toEqual([]);
});
