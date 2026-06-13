"""
GBT 向量数据库 — ChromaDB 嵌入式模式
零服务器 | 零断连 | 零配置 | 自动持久化
用法: python vectordb.py
"""
import chromadb
import os

DB_PATH = os.path.dirname(os.path.abspath(__file__))

class VectorDB:
    def __init__(self, name="gbt_knowledge"):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, texts, ids=None, metadatas=None, embeddings=None):
        """添加文档: 有embedding直接用，没有就用内置embedding"""
        params = {"documents": texts}
        if ids: params["ids"] = ids
        if metadatas: params["metadatas"] = metadatas
        if embeddings: params["embeddings"] = embeddings
        self.collection.add(**params)
        return len(texts)
    
    def search(self, query_text, n=5):
        """语义搜索"""
        r = self.collection.query(query_texts=[query_text], n_results=n)
        return [(doc, 1-dist) for doc, dist in zip(r["documents"][0], r["distances"][0])]
    
    def search_by_embedding(self, embedding, n=5):
        """用已有向量搜索"""
        r = self.collection.query(query_embeddings=[embedding], n_results=n)
        return [(doc, 1-dist) for doc, dist in zip(r["documents"][0], r["distances"][0])]
    
    def count(self):
        return self.collection.count()
    
    def list_collections(self):
        return self.client.list_collections()

# 自测
if __name__ == "__main__":
    db = VectorDB("demo")
    
    db.add(
        texts=["向量数据库用于存储和检索高维向量数据",
               "机器学习模型通过Embedding将文本转为向量",
               "GBT小土豆是全能AI开发者平台"],
        ids=["d1", "d2", "d3"]
    )
    
    print(f"已存储: {db.count()} 条记录")
    print(f"\n搜索 '什么是向量数据库':")
    for text, score in db.search("什么是向量数据库", n=2):
        print(f"  [{score:.3f}] {text[:60]}")
    print("\n部署成功! 零服务器, 零断连!")
