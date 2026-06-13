"""
GBT 向量数据库 - 纯SQLite实现
零依赖 | 零服务 | 零断连 | 永不停用
就一个 vectors.db 文件
"""
import sqlite3, json, math, os
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vectors.db")

class VectorDB:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_tables()

    def _init_tables(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS collections(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, dim INTEGER NOT NULL)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS vectors(id INTEGER PRIMARY KEY AUTOINCREMENT, collection_id INTEGER NOT NULL, doc_id TEXT NOT NULL, vector_json TEXT NOT NULL, text TEXT, metadata TEXT, FOREIGN KEY(collection_id) REFERENCES collections(id), UNIQUE(collection_id, doc_id))")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_col ON vectors(collection_id)")
        self.conn.commit()

    def create_collection(self, name, dim):
        try:
            self.conn.execute("INSERT INTO collections(name,dim) VALUES(?,?)",(name,dim))
            self.conn.commit()
            return self.conn.execute("SELECT id FROM collections WHERE name=?",(name,)).fetchone()[0]
        except:
            return self.conn.execute("SELECT id FROM collections WHERE name=?",(name,)).fetchone()[0]

    def get_collection(self, name):
        return self.conn.execute("SELECT id,dim FROM collections WHERE name=?",(name,)).fetchone()

    def insert(self, col_name, vectors, texts=None, doc_ids=None):
        col = self.get_collection(col_name)
        if not col:
            col = (self.create_collection(col_name, len(vectors[0])), len(vectors[0]))
        col_id, dim = col
        cnt = 0
        for i, v in enumerate(vectors):
            if len(v) != dim: continue
            did = doc_ids[i] if doc_ids else f"v{cnt}"
            txt = texts[i] if texts else None
            self.conn.execute("INSERT OR REPLACE INTO vectors(collection_id,doc_id,vector_json,text) VALUES(?,?,?,?)",(col_id, did, json.dumps(v), txt))
            cnt += 1
        self.conn.commit()
        return cnt

    def search(self, col_name, query_vec, top_k=5):
        col = self.get_collection(col_name)
        if not col: return []
        rows = self.conn.execute("SELECT doc_id,vector_json,text FROM vectors WHERE collection_id=?",(col[0],)).fetchall()
        res = []
        for did, vj, txt in rows:
            v = json.loads(vj)
            sim = VectorDB.cos(v, query_vec)
            res.append((did, txt, sim))
        res.sort(key=lambda x: x[2], reverse=True)
        return res[:top_k]

    @staticmethod
    def cos(a, b):
        dot = sum(x*y for x,y in zip(a,b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        return dot/(na*nb) if na and nb else 0

    def count(self, name):
        col = self.get_collection(name)
        return self.conn.execute("SELECT COUNT(*) FROM vectors WHERE collection_id=?",(col[0],)).fetchone()[0] if col else 0

    def list_cols(self):
        return self.conn.execute("SELECT name,dim FROM collections").fetchall()

    def close(self):
        self.conn.close()
