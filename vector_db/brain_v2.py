"""
GBT Brain v2 - SQLite/PostgreSQL ??
??: SQLite (???, ????)
??: PostgreSQL + pgvector (Docker????)
"""
import sys, os, json, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vector_db import VectorDB

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "infra", "db_config.json")

def _pg_config():
    try:
        return json.load(open(CONFIG_FILE))["postgresql"]
    except:
        return None

class Brain:
    def __init__(self, mode="auto"):
        cfg = _pg_config()
        self.mode = "pg" if mode == "auto" and cfg and self._pg_ok(cfg) else "sqlite"
        if self.mode == "pg":
            import psycopg2
            self.pg = psycopg2.connect(
                host=cfg["host"], port=cfg["port"],
                user=cfg["user"], password=cfg["password"],
                dbname="gbt_brain"
            )
            self.pg.autocommit = True
        else:
            self.vdb = VectorDB()

    def _pg_ok(self, cfg):
        try:
            import psycopg2
            c = psycopg2.connect(host=cfg["host"], port=cfg["port"],
                user=cfg["user"], password=cfg["password"],
                dbname="gbt_brain", connect_timeout=3)
            c.close()
            return True
        except:
            return False

    def _embed(self, text):
        words = text.lower().split()
        if not words: return [0]*128
        vocab = list(set(words))
        vec = [0]*128
        for w in vocab:
            vec[hash(w) % 128] += words.count(w) / len(words)
        norm = sum(v*v for v in vec)**0.5
        return [v/norm for v in vec] if norm > 0 else vec

    def note(self, title, content, tags=None):
        did = f"n_{int(time.time())}_{hashlib.md5(title.encode()).hexdigest()[:6]}"
        if self.mode == "pg":
            emb = json.dumps(self._embed(f"{title} {content}"))
            tags_arr = "{" + ",".join(tags or []) + "}" if tags else "{}"
            self.pg.cursor().execute(
                "INSERT INTO notes(id,title,content,embedding,tags) VALUES(%s,%s,%s,%s,%s)",
                (did, title, content, emb, tags_arr))
        else:
            self.vdb.insert("notes", [self._embed(f"{title}\n{content}")],
                           texts=[f"{title}\n{content}"], doc_ids=[did])
        return did

    def recall(self, query, top_k=5):
        vec = self._embed(query)
        if self.mode == "pg":
            cur = self.pg.cursor()
            cur.execute(
                "SELECT id,title,content,1-(embedding<=>%s) as sim FROM notes ORDER BY embedding<=>%s LIMIT %s",
                (json.dumps(vec), json.dumps(vec), top_k))
            return [{"id": r[0], "title": r[1], "text": (r[2] or "")[:200], "score": round(r[3], 4)} for r in cur.fetchall()]
        else:
            r = self.vdb.search("notes", vec, top_k)
            return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in r]

    def learn(self, insight, source="obs", confidence=1.0):
        did = f"l_{int(time.time())}"
        text = f"[{source}] c={confidence}: {insight}"
        if self.mode == "pg":
            emb = json.dumps(self._embed(text))
            self.pg.cursor().execute(
                "INSERT INTO learnings(id,insight,embedding,source,confidence) VALUES(%s,%s,%s,%s,%s)",
                (did, insight, emb, source, confidence))
        else:
            self.vdb.insert("learnings", [self._embed(text)], texts=[text], doc_ids=[did])
        return did

    def know(self, query, top_k=5):
        vec = self._embed(query)
        if self.mode == "pg":
            cur = self.pg.cursor()
            cur.execute(
                "SELECT id,insight,source,1-(embedding<=>%s) as sim FROM learnings ORDER BY embedding<=>%s LIMIT %s",
                (json.dumps(vec), json.dumps(vec), top_k))
            return [{"id": r[0], "text": r[1][:200], "source": r[2], "score": round(r[3], 4)} for r in cur.fetchall()]
        else:
            r = self.vdb.search("learnings", vec, top_k)
            return [{"id": rid, "text": txt[:200], "score": round(s, 4)} for rid, txt, s in r]

    def stats(self):
        if self.mode == "pg":
            cur = self.pg.cursor()
            tables = ["notes", "learnings", "patterns", "decisions"]
            return {t: cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}
        return {"mode": "sqlite", "collections": [c[0] for c in self.vdb.list_cols()]}

    @property
    def mode_name(self):
        return "PostgreSQL+pgvector (????)" if self.mode == "pg" else "SQLite (???,????)"
