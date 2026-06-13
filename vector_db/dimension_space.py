"""
GBT DimensionSpace - ???????
9????? + ???? + ??????
"""
import sys, os, json, time, re, hashlib, urllib.request, ssl
from datetime import datetime
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ========== 9????? ==========
DIMENSIONS = {
    "security": {
        "name": "????",
        "icon": "d0",
        "weight": 10,
        "questions": [
            "???????????",
            "?????????",
            "??????????",
            "?????????"
        ],
        "keywords": ["eval", "exec", "password", "secret", "token", "api_key", "auth", "encrypt", "hash", "sql_inject", "xss", "csrf"]
    },
    "performance": {
        "name": "????",
        "icon": "d1",
        "weight": 8,
        "questions": [
            "????N+1???",
            "?????????",
            "????????????",
            "?????????"
        ],
        "keywords": ["sync", "block", "cache", "lazy", "batch", "parallel", "async", "timeout", "pool", "buffer"]
    },
    "architecture": {
        "name": "????",
        "icon": "d2",
        "weight": 9,
        "questions": [
            "???????????",
            "???????????",
            "?????????",
            "?????????"
        ],
        "keywords": ["interface", "abstract", "dependency", "module", "decouple", "plugin", "middleware", "adapter", "factory"]
    },
    "quality": {
        "name": "????",
        "icon": "d3",
        "weight": 7,
        "questions": [
            "???????",
            "?????????",
            "????????",
            "?????????"
        ],
        "keywords": ["todo", "fixme", "hack", "workaround", "deprecated", "else if", "nested", "duplicate", "magic"]
    },
    "innovation": {
        "name": "????",
        "icon": "d4",
        "weight": 6,
        "questions": [
            "??????????",
            "?????????",
            "????????",
            "????????"
        ],
        "keywords": ["new", "novel", "unique", "custom", "ai", "ml", "agent", "autonomous", "self", "evolve", "intelligent"]
    },
    "scalability": {
        "name": "????",
        "icon": "d5",
        "weight": 8,
        "questions": [
            "???????",
            "???????",
            "????????",
            "???????"
        ],
        "keywords": ["scale", "shard", "partition", "distribute", "cluster", "replica", "load_balance", "horizontal"]
    },
    "reliability": {
        "name": "?????",
        "icon": "d6",
        "weight": 9,
        "questions": [
            "???????",
            "????????",
            "??????????",
            "?????????"
        ],
        "keywords": ["retry", "fallback", "circuit_breaker", "timeout", "health_check", "backup", "restore", "recovery"]
    },
    "intelligence": {
        "name": "????",
        "icon": "d7",
        "weight": 10,
        "questions": [
            "??????????",
            "???????",
            "????????",
            "?????????"
        ],
        "keywords": ["learn", "train", "model", "embedding", "pattern", "predict", "classify", "optimize", "auto"]
    },
    "ecosystem": {
        "name": "????",
        "icon": "d8",
        "weight": 5,
        "questions": [
            "??????",
            "??/?????",
            "???????",
            "???????"
        ],
        "keywords": ["plugin", "extension", "api", "integration", "community", "open_source", "github", "documentation"]
    }
}

# ========== ?????? (????) ==========
class LocalModel:
    """??????LLM, ???ChromaDB????"""
    def __init__(self):
        self.backend = self._detect()

    def _detect(self):
        endpoints = [
            ("ollama", "http://localhost:11434/api/generate"),
            ("lmstudio", "http://localhost:1234/v1/completions"),
            ("llamacpp", "http://localhost:8080/completion"),
        ]
        for name, url in endpoints:
            try:
                req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=2)
                return {"name": name, "url": url, "type": "llm"}
            except:
                pass
        return {"name": "heuristic", "url": None, "type": "heuristic"}

    def analyze(self, prompt, data):
        if self.backend["type"] == "llm":
            return self._llm_analyze(prompt, data)
        return self._heuristic_analyze(prompt, data)

    def _llm_analyze(self, prompt, data):
        try:
            body = json.dumps({"model": "", "prompt": f"{prompt}\n\nData: {json.dumps(data, indent=2, ensure_ascii=False)[:2000]}\n\nAnalysis:", "stream": False}).encode()
            req = urllib.request.Request(self.backend["url"], data=body, headers={"Content-Type": "application/json"})
            resp = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
            return resp.get("response", resp.get("choices", [{}])[0].get("text", ""))
        except Exception as e:
            return self._heuristic_analyze(prompt, data)

    def _heuristic_analyze(self, prompt, data):
        """????? - ?????+????"""
        text = json.dumps(data, ensure_ascii=False).lower() if isinstance(data, dict) else str(data).lower()
        scores = {}
        for dim_id, dim in DIMENSIONS.items():
            score = 0
            for kw in dim["keywords"]:
                if kw in text:
                    score += 1
            scores[dim_id] = min(score * 10 / max(len(dim["keywords"]), 1), 100)
        return json.dumps(scores, ensure_ascii=False)
