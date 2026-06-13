"""
GBT Brain - AI记忆持久化 + 自主学习 + 研发笔记
基于SQLite向量数据库, 零服务零断连永不停用
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vector_db import VectorDB
import json, time, hashlib

DB_DIR = os.path.dirname(os.path.abspath(__file__))

class Brain:
    """AI大脑: 记忆存储 + 语义检索 + 自主学习"""

    def __init__(self):
        self.vdb = VectorDB()
        self.meta_file = os.path.join(DB_DIR, "brain_meta.json")
        self.meta = self._load_meta()

    def _load_meta(self):
        if os.path.exists(self.meta_file):
            return json.load(open(self.meta_file))
        return {"notes": 0, "learnings": 0, "patterns": 0, "decisions": 0, "sessions": []}

    def _save_meta(self):
        json.dump(self.meta, open(self.meta_file, "w"), indent=2)

    def _embed(self, text):
        """简单文本向量化 (TF-based, 无外部依赖)"""
        words = text.lower().split()
        if not words:
            return [0]*128
        # build vocabulary from the text
        vocab = list(set(words))
        vec = [0]*128
        for i, w in enumerate(vocab):
            idx = hash(w) % 128
            vec[idx] += words.count(w) / len(words)
        # normalize
        norm = sum(v*v for v in vec)**0.5
        if norm > 0:
            vec = [v/norm for v in vec]
        return vec

    # ========== 笔记管理 ==========
    def note(self, title, content, tags=None):
        """写研发笔记"""
        doc_id = f"note_{int(time.time())}_{hashlib.md5(title.encode()).hexdigest()[:6]}"
        full_text = f"{title}\n{content}"
        vec = self._embed(full_text)
        self.vdb.insert("notes", [vec], texts=[full_text], doc_ids=[doc_id])
        self.meta["notes"] += 1
        # also store structured
        self._write_json(f"note_{doc_id}.json", {
            "id": doc_id, "title": title, "content": content,
            "tags": tags or [], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        self._save_meta()
        return doc_id

    def recall(self, query, top_k=5):
        """语义检索记忆"""
        vec = self._embed(query)
        results = self.vdb.search("notes", vec, top_k)
        return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in results]

    # ========== 自主学习 ==========
    def learn(self, insight, source="observation", confidence=1.0):
        """自主学到的知识点"""
        doc_id = f"learn_{int(time.time())}"
        full = f"[{source}] confidence={confidence}\n{insight}"
        vec = self._embed(full)
        self.vdb.insert("learnings", [vec], texts=[full], doc_ids=[doc_id])
        self.meta["learnings"] += 1
        self._save_meta()
        return doc_id

    def know(self, query, top_k=5):
        """检索已学知识"""
        vec = self._embed(query)
        results = self.vdb.search("learnings", vec, top_k)
        return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in results]

    # ========== 模式发现 ==========
    def pattern(self, name, description, evidence):
        """记录发现的模式"""
        doc_id = f"pat_{int(time.time())}"
        full = f"PATTERN: {name}\nDESC: {description}\nEVIDENCE: {evidence}"
        vec = self._embed(full)
        self.vdb.insert("patterns", [vec], texts=[full], doc_ids=[doc_id])
        self.meta["patterns"] += 1
        self._save_meta()
        return doc_id

    def detect(self, context, top_k=3):
        """根据上下文检测已有模式"""
        vec = self._embed(context)
        results = self.vdb.search("patterns", vec, top_k)
        return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in results]

    # ========== 决策记录 ==========
    def decide(self, problem, options, chosen, why):
        """记录技术决策"""
        doc_id = f"dec_{int(time.time())}"
        full = f"PROBLEM: {problem}\nOPTIONS: {options}\nCHOSEN: {chosen}\nWHY: {why}"
        vec = self._embed(full)
        self.vdb.insert("decisions", [vec], texts=[full], doc_ids=[doc_id])
        self.meta["decisions"] += 1
        self._save_meta()
        return doc_id

    def recall_decisions(self, query, top_k=5):
        """回顾历史决策"""
        vec = self._embed(query)
        results = self.vdb.search("decisions", vec, top_k)
        return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in results]

    # ========== 会话管理 ==========
    def session_start(self, session_id, summary=""):
        self.meta["sessions"].append({
            "id": session_id, "start": time.strftime("%Y-%m-%d %H:%M:%S"), "summary": summary
        })
        self._save_meta()

    def stats(self):
        return {
            "notes": self.meta["notes"],
            "learnings": self.meta["learnings"],
            "patterns": self.meta["patterns"],
            "decisions": self.meta["decisions"],
            "sessions": len(self.meta["sessions"]),
            "collections": [c[0] for c in self.vdb.list_cols()]
        }

    def _write_json(self, filename, data):
        p = os.path.join(DB_DIR, "notes", filename)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(data, open(p, "w"), indent=2, ensure_ascii=False)
