// Submits all indexable story URLs to IndexNow (Bing, Yandex, Naver, Seznam, Yep) in batches of 5000.
// Usage: node deploy/indexnow.mjs
import STORY from "./story_paths.js";
import { publicUrl, APEX } from "./urlmap.js";

const KEY = "37feeed875722863fda484c68e6695e5";
const allUrls = STORY.map((sp) => publicUrl(sp)).filter((u) => u && u.startsWith("https://"));

console.log(`Submitting ${allUrls.length} indexable story URLs to IndexNow...`);

const BATCH_SIZE = 5000;
let accepted = 0;

for (let i = 0; i < allUrls.length; i += BATCH_SIZE) {
  const chunk = allUrls.slice(i, i + BATCH_SIZE);
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({
      host: APEX,
      key: KEY,
      keyLocation: `https://${APEX}/${KEY}.txt`,
      urlList: chunk,
    }),
  });
  if (res.status === 200 || res.status === 202) {
    accepted += chunk.length;
    console.log(`  Batch ${i + 1}..${i + chunk.length}: Accepted (${res.status})`);
  } else {
    console.error(`  Batch ${i + 1}..${i + chunk.length} Error:`, res.status, await res.text());
  }
}

console.log(`IndexNow complete: ${accepted}/${allUrls.length} URLs submitted successfully.`);
