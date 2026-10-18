#!/usr/bin/env python3
"""AI-powered multi-language translation engine for Nova Hart video titles and descriptions.

Uses OpenRouter (Gemini 2.5 Flash) with persistent disk caching.
"""

import json
import os
import re
import time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
CACHE_DIR = os.path.join(STATE, "translations_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash"

WEB_RING_LINE = re.compile(r"^\s*(▶\s*)?Web Ring\s*:.*stardust-archive\.net.*\n*", re.M)


def clean_desc(desc):
    """Strip any existing webring headers or boilerplate markers."""
    if not desc:
        return ""
    d = WEB_RING_LINE.sub("", desc).strip()
    return d


def get_cached_translation(vid):
    path = os.path.join(CACHE_DIR, f"{vid}.json")
    if os.path.exists(path):
        try:
            with open(path) as fh:
                return json.load(fh)
        except Exception:
            pass
    return None


def save_cached_translation(vid, data):
    path = os.path.join(CACHE_DIR, f"{vid}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def translate_video(vid, title, raw_desc, target_langs):
    """Translates title and body description into target_langs using OpenRouter.
    
    Returns a dict: {lang_code: {'title': str, 'description': str}}
    """
    cached = get_cached_translation(vid)
    if cached:
        # Verify that all requested langs are in cache
        if all(l in cached for l in target_langs):
            return cached

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[!] No OPENROUTER_API_KEY found in environment. Skipping AI translation.")
        return {}

    body = clean_desc(raw_desc)
    # If body is tiny or empty, use title as context
    body_context = body[:1200] if body else title

    prompt = f"""You are a professional music localizer and translator specializing in 80s/90s synthwave, cyberpunk, and ARG lore.
Translate the following YouTube video Title and Description into these {len(target_langs)} languages:
{', '.join(target_langs)}

Guidelines:
1. Preserve the dramatic synthwave / cyberpunk lore tone.
2. Keep artist branding recognizable. Use canonical localized names for artist:
   - ja: ノヴァ・ハート (Nova Hart)
   - ko: 노바 하트 (Nova Hart)
   - ru: Нова Харт (Nova Hart)
   - zh-CN / zh-TW: 诺瓦·哈特 / 諾瓦·哈特
   - other latin-script languages: keep "Nova Hart"
3. Song titles in quotes or dashes should be translated naturally (e.g. "Asset Loss" -> 「アセット・ロス」 in ja, "Pérdida de Activos" in es).
4. Title MUST be under 100 characters in all languages.
5. Translate lyrics, story paragraphs, and credits (e.g. "Written & Produced by" -> "作詞・作曲", "Mezclado por", etc.).
6. Do NOT include any hashtags in the translated body.

Input Title:
{title}

Input Description Body:
{body_context}

Return ONLY a JSON object with this exact structure:
{{
  "translations": {{
    "<lang_code>": {{
      "title": "translated title under 100 chars",
      "description": "translated description body text"
    }}
  }}
}}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://stardust-archive.net",
        "X-Title": "Nova Hart Video Localizer",
    }
    payload = {
        "model": MODEL,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": prompt}],
    }

    for attempt in range(3):
        try:
            r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=40)
            if r.status_code == 200:
                raw_json = r.json()["choices"][0]["message"]["content"].strip()
                if raw_json.startswith("```"):
                    raw_json = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_json, flags=re.S).strip()
                res = None
                for candidate in (
                    raw_json,
                    re.sub(r'\\(?![/"\\bfnrtu])', r"\\\\", raw_json),
                ):
                    try:
                        res = json.loads(candidate, strict=False)
                        break
                    except Exception:
                        pass
                if res is None:
                    # Regex fallback extractor per language block if unescaped quotes broke JSON
                    translations = {}
                    for lang_code in target_langs:
                        m = re.search(
                            rf'"{re.escape(lang_code)}"\s*:\s*\{{[^{{}}]*?"title"\s*:\s*"([^\n\r"]+)"[^{{}}]*?"description"\s*:\s*"(.*?)"\s*\}}',
                            raw_json,
                            flags=re.S,
                        )
                        if m:
                            translations[lang_code] = {
                                "title": m.group(1).strip(),
                                "description": m.group(2).replace('\\n', '\n').strip(),
                            }
                    if not translations:
                        raise ValueError("Could not parse JSON or fallback regex from LLM response")
                else:
                    translations = res.get("translations", {})

                # Sanitize lengths
                for l, val in translations.items():
                    if "title" in val:
                        val["title"] = val["title"].strip()[:100]
                    if "description" in val:
                        val["description"] = val["description"].strip()[:4000]

                # Merge with existing cache if any
                merged = cached or {}
                merged.update(translations)
                save_cached_translation(vid, merged)
                return merged
            elif r.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            else:
                print(f"[!] OpenRouter error {r.status_code}: {r.text[:200]}")
                break
        except Exception as e:
            print(f"[!] Translation attempt {attempt+1} failed: {e}")
            time.sleep(1)

    return cached or {}


if __name__ == "__main__":
    # Self-test on a sample
    sample_title = "Nova Hart — Burning Oath | 80s Anthemic Cyberpunk"
    sample_body = "The fire refuses to die. Nova makes a pact with the underground."
    langs = ["ja", "es", "ko", "de", "fr"]
    print("Testing translation engine...")
    res = translate_video("test_vid_001", sample_title, sample_body, langs)
    print(json.dumps(res, indent=2, ensure_ascii=False))
