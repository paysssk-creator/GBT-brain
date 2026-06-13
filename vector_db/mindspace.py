"""
GBT MindSpace Engine - ???????
???????10????, ?????Brain
"""
import json, time, os, sys, threading
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mindspace_collectors import GitHubTrending, HackerNews, DevTo, RedditProgramming

COLLECTORS = [GitHubTrending(), HackerNews(), DevTo(), RedditProgramming()]
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mindspace_data.json")

# Keywords that signal high-value content
VALUE_KEYWORDS = [
    "ai", "ml", "llm", "gpt", "transformer", "deepseek", "openai",
    "vector", "embedding", "rag", "agent", "autonomous", "self-evolve",
    "rust", "golang", "python", "typescript", "wasm",
    "database", "postgres", "sqlite", "redis",
    "security", "vulnerability", "exploit", "cve",
    "opensource", "free", "self-hosted", "local", "privacy",
    "new", "release", "breakthrough", "0day", "hot"
]

class MindSpaceEngine:
    def __init__(self):
        self.data = self._load()
        from brain import Brain
        self.brain = Brain()

    def _load(self):
        if os.path.exists(DATA_FILE):
            return json.load(open(DATA_FILE))
        return {"last_scan": None, "items": {}, "top_finds": []}

    def _save(self):
        json.dump(self.data, open(DATA_FILE, "w"), indent=2)

    def scan(self):
        """???????, ?????10"""
        all_items = []
        for src in COLLECTORS:
            try:
                items = src.fetch()
                print(f"  [{src.name}] fetched {len(items)} items")
                all_items.extend(items)
            except Exception as e:
                print(f"  [{src.name}] ERROR: {e}")

        # ?????
        seen = set()
        scored = []
        for item in all_items:
            key = hashlib.md5(item.get("title", "").encode()).hexdigest()
            if key in seen: continue
            seen.add(key)
            score = self._score(item)
            item["score"] = score
            scored.append(item)
            # Store in brain
            self._store_to_brain(item)

        scored.sort(key=lambda x: x["score"], reverse=True)
        top10 = scored[:10]

        # Update data
        self.data["last_scan"] = datetime.now().isoformat()
        for item in top10:
            hid = hashlib.md5(item["title"].encode()).hexdigest()
            if hid not in self.data["items"]:
                self.data["items"][hid] = item
        self.data["top_finds"] = top10
        self._save()

        return top10

    def _score(self, item):
        """????: ????? + ????"""
        text = (item.get("title", "") + " " + item.get("description", "")).lower()
        score = 0
        source_weight = {"github": 3, "hackernews": 2, "reddit": 1.5, "devto": 1}
        score += source_weight.get(item.get("source", ""), 1)
        for kw in VALUE_KEYWORDS:
            if kw in text:
                score += 2
        if any(w in text for w in ["new", "release", "breakthrough", "0day"]):
            score += 3
        return round(score, 1)

    def _store_to_brain(self, item):
        try:
            title = item.get("title", "")[:200]
            desc = item.get("description", "")[:500]
            text = f"[{item.get('source','').upper()}] {title}"
            if desc:
                text += f"\n{desc}"
            self.brain.note(title, text, tags=[item.get("source", ""), item.get("type", "")])
        except:
            pass

    def top(self, n=10):
        return self.data.get("top_finds", [])[:n]

    def search(self, query):
        results = self.brain.recall(query, top_k=5)
        return results

    def stats(self):
        return {
            "last_scan": self.data.get("last_scan"),
            "total_items": len(self.data.get("items", {})),
            "brain": self.brain.stats()
        }

    def watch(self, interval_sec=3600):
        """????"""
        print(f"MindSpace watching every {interval_sec}s... Ctrl+C to stop")
        while True:
            try:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scanning...")
                top10 = self.scan()
                print(f"  Top {len(top10)}:")
                for i, item in enumerate(top10[:5]):
                    print(f"    {i+1}. [{item.get('source','')}] {item.get('title','')[:80]} (score:{item.get('score',0)})")
                time.sleep(interval_sec)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"  Error: {e}")
                time.sleep(60)


import hashlib

if __name__ == "__main__":
    engine = MindSpaceEngine()
    print("=" * 60)
    print("GBT MindSpace - AI????")
    print(f"???: GitHub Trending, Hacker News, Dev.to, Reddit")
    print(f"??: ???? (ChromaDB all-MiniLM-L6-v2)")
    print(f"??: SQLite (????)")
    print("=" * 60)

    top10 = engine.scan()
    print(f"\n=== TOP 10 ?? ===")
    for i, item in enumerate(top10):
        print(f"\n  {i+1}. [{item['source'].upper()}] score={item['score']}")
        print(f"     {item['title'][:100]}")
        if item.get('description'):
            print(f"     {item['description'][:120]}")
        if item.get('url'):
            print(f"     {item['url']}")

    print(f"\n=== MindSpace Stats ===")
    print(json.dumps(engine.stats(), indent=2))
