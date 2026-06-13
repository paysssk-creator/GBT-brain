"""
GBT MindSpace Collectors v2 - API????????
"""
import json, time, urllib.request, ssl, re
from datetime import datetime

def _fetch(url, headers=None, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "GBT-MindSpace/1.0"})
    return urllib.request.urlopen(req, timeout=timeout, context=ctx)

class GitHubTrending:
    name = "github"
    def fetch(self):
        try:
            data = json.loads(_fetch(
                "https://api.github.com/search/repositories?q=stars:%3E100+pushed:%3E2026-06-07&sort=stars&order=desc&per_page=10",
                {"User-Agent": "GBT-MindSpace/1.0", "Accept": "application/vnd.github.v3+json"}
            ).read().decode())
            return [{"source":"github","title":r["full_name"],"url":r["html_url"],
                     "description":(r.get("description")or"")[:200],
                     "stars":r.get("stargazers_count",0),"language":r.get("language",""),
                     "type":"repo","ts":datetime.now().isoformat()} for r in data.get("items",[])[:10]]
        except Exception as e:
            return [{"source":"github","error":str(e)[:100]}]

class HackerNews:
    name = "hackernews"
    def fetch(self):
        try:
            ids = json.loads(_fetch("https://hacker-news.firebaseio.com/v0/topstories.json").read().decode())[:10]
            results = []
            for nid in ids:
                try:
                    item = json.loads(_fetch(f"https://hacker-news.firebaseio.com/v0/item/{nid}.json",timeout=5).read().decode())
                    results.append({"source":"hackernews","title":item.get("title",""),
                        "url":item.get("url",f"https://news.ycombinator.com/item?id={nid}"),
                        "description":f"Score:{item.get('score',0)}|Comments:{item.get('descendants',0)}",
                        "type":"news","ts":datetime.now().isoformat()})
                except: pass
            return results
        except Exception as e:
            return [{"source":"hackernews","error":str(e)[:100]}]

class DevTo:
    name = "devto"
    def fetch(self):
        try:
            data = json.loads(_fetch("https://dev.to/api/articles?top=7&per_page=10").read().decode())
            return [{"source":"devto","title":a.get("title",""),"url":a.get("url",""),
                     "description":(a.get("description")or"")[:200],"tags":",".join(a.get("tag_list",[])),
                     "reactions":a.get("positive_reactions_count",0),
                     "type":"article","ts":datetime.now().isoformat()} for a in data[:10]]
        except Exception as e:
            return [{"source":"devto","error":str(e)[:100]}]

class RedditProgramming:
    name = "reddit"
    def fetch(self):
        try:
            data = json.loads(_fetch("https://www.reddit.com/r/programming/hot.json?limit=10",
                {"User-Agent":"Mozilla/5.0"}).read().decode())
            return [{"source":"reddit","title":p["data"]["title"],
                     "url":f"https://reddit.com{p['data']['permalink']}",
                     "description":f"Score:{p['data']['score']}|Comments:{p['data']['num_comments']}",
                     "type":"discussion","ts":datetime.now().isoformat()}
                    for p in data.get("data",{}).get("children",[])]
        except Exception as e:
            return [{"source":"reddit","error":str(e)[:100]}]
