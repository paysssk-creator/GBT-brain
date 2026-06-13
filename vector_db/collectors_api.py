import json, time, urllib.request, ssl
from datetime import datetime

def fetch_github_trending():
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "https://api.github.com/search/repositories?q=stars:%3E100+pushed:%3E2026-06-07&sort=stars&order=desc&per_page=10"
        req = urllib.request.Request(url, headers={"User-Agent": "GBT-MindSpace/1.0", "Accept": "application/vnd.github.v3+json"})
        data = json.loads(urllib.request.urlopen(req, timeout=15, context=ctx).read().decode())
        results = []
        for item in data.get("items", [])[:10]:
            results.append({
                "source": "github",
                "title": item["full_name"],
                "url": item["html_url"],
                "description": (item.get("description") or "")[:200],
                "stars": item.get("stargazers_count", 0),
                "language": item.get("language", ""),
                "type": "repo",
                "ts": datetime.now().isoformat()
            })
        return results
    except Exception as e:
        return [{"source": "github", "error": str(e)[:200]}]

def fetch_devto_trending():
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "https://dev.to/api/articles?top=7&per_page=10"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=10, context=ctx).read().decode())
        results = []
        for item in data[:10]:
            results.append({
                "source": "devto",
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": (item.get("description") or "")[:200],
                "tags": ", ".join(item.get("tag_list", [])),
                "reactions": item.get("positive_reactions_count", 0),
                "type": "article",
                "ts": datetime.now().isoformat()
            })
        return results
    except Exception as e:
        return [{"source": "devto", "error": str(e)[:200]}]

if __name__ == "__main__":
    gh = fetch_github_trending()
    print(f"GitHub: {len(gh)} repos")
    for r in gh[:3]:
        print(f"  {r.get('title')} ({r.get('stars')}*)")
    dv = fetch_devto_trending()
    print(f"Dev.to: {len(dv)} articles")
    for a in dv[:3]:
        print(f"  {a.get('title')}")
