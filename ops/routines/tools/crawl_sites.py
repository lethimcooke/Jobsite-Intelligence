"""Crawl4AI site reader for the Jobsite replenish (hauler home, services and contact pages). Run with the isolated venv:
D:\\Workspace\\austin-signage-repo\\local\\tools\\crawl4ai-venv\\Scripts\\python.exe crawl_sites.py <out dir> <url> [<url> ...]
Saves one Markdown file per page and prints emails, phones and elapsed seconds per page."""
import asyncio, json, os, re, sys, time
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
OUT, URLS = sys.argv[1], sys.argv[2:]
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PH = re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")
async def main():
    os.makedirs(OUT, exist_ok=True); res, t0 = {}, time.time()
    async with AsyncWebCrawler(config=BrowserConfig(headless=True, verbose=False)) as c:
        for u in URLS:
            t = time.time()
            r = await c.arun(url=u, config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS, verbose=False))
            md = (getattr(r.markdown, "raw_markdown", None) or str(r.markdown or "")) if r.success else ""
            open(os.path.join(OUT, re.sub(r"[^A-Za-z0-9.]+", "_", u.split("://", 1)[-1]) + ".md"), "w", encoding="utf-8").write(md)
            res[u] = {"ok": r.success, "secs": round(time.time() - t, 1),
                      "emails": sorted({e.lower() for e in EM.findall(md) if not re.search(r"sentry|wix|\.(png|jpg|webp)$", e)})[:5],
                      "phones": sorted(set(PH.findall(md)))[:3]}
    res["_total_secs"] = round(time.time() - t0, 1)
    print(json.dumps(res, indent=1))
asyncio.run(main())
