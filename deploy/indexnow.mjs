// Submits all indexable story URLs to IndexNow (Bing, Yandex, Naver, Seznam, Yep).
// Usage: node deploy/indexnow.mjs
import STORY from "./story_paths.js";
import { publicUrl } from "./urlmap.js";

const KEY = "37feeed875722863fda484c68e6695e5";
const byHost = new Map();
for (const sp of STORY) {
  const u = publicUrl(sp);
  if (!u || !u.startsWith("https://")) continue;
  const host = new URL(u).hostname;
  if (!byHost.has(host)) byHost.set(host, []);
  byHost.get(host).push(u);
}
let ok = 0;
for (const [host, urlList] of byHost) {
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host, key: KEY, keyLocation: `https://${host}/${KEY}.txt`, urlList }),
  });
  if (res.status === 200 || res.status === 202) ok++;
  else console.error(res.status, host, await res.text());
}
console.log(`IndexNow: ${ok}/${byHost.size} hosts accepted (${STORY.length} story pages)`);
