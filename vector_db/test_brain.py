import sys
sys.path.insert(0, "C:/Users/ADMIN/.gbt/vector_db")
from brain import Brain

b = Brain()

# 1. write notes
b.note("SQLite vector database design", "Using pure SQLite for vector storage. Each collection is a table, vectors stored as JSON. Cosine similarity for search. WAL mode for performance.", tags=["database", "vector", "sqlite"])
b.note("MCP server path validation bug", "Found bug in input-validator.ts line 254-262. allowRelative=false was also rejecting absolute paths. Fixed by separating path traversal check from relative path check.", tags=["bug", "security", "typescript"])
b.note("ChromaDB embedded mode", "ChromaDB supports embedded PersistentClient mode. No server needed. But downloads ONNX model on first use (79MB). Works with Python 3.12.", tags=["chromadb", "vector-db"])

# 2. autonomous learning
b.learn("Python 3.11 default on this system, but pip packages installed to Python 3.12. Need to use full path C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python.exe for chromadb", source="environment")
b.learn("PowerShell encoding issues with Chinese characters in command line. Use ASCII for test scripts, UTF8 for data files.", source="debugging")
b.learn("Docker daemon not running on this Windows system. Docker Desktop needs manual start. Embedded databases (SQLite) preferred for reliability.", source="infrastructure")

# 3. patterns
b.pattern("MCP disconnection", "MCP server processes can be killed but restart with same PIDs. Cline takes time to reconnect stdio transport.", "Observed 4 server.js processes, killed all, processes restarted but Cline needed ~2min to reconnect")
b.pattern("Windows path escaping", "PowerShell handles backslash paths differently. Use forward slashes or double backslashes in cross-platform code.", "Failed dir command for .gbt directory due to PowerShell interpreting the dot prefix")

# 4. decisions
b.decide("Vector database choice", "Milvus vs Qdrant vs ChromaDB vs pgvector vs LanceDB", "SQLite-based custom", "Zero server = zero disconnects. No Docker needed. Always available. Simplicity over performance for this use case.")
b.decide("Memory architecture", "File-based JSON vs embedded DB", "SQLite + VectorDB custom", "JSON doesn't support semantic search. VectorDB gives both structured metadata and similarity retrieval.")

print("=" * 50)
print("STATS:", b.stats())
print()

# recall tests
print("--- recall: 'database' ---")
for r in b.recall("database"):
    print(f"  [{r['score']}] {r['text'][:80]}...")

print()
print("--- know: 'python environment' ---")
for r in b.know("python environment"):
    print(f"  [{r['score']}] {r['text'][:80]}...")

print()
print("--- detect: 'service disconnection' ---")
for r in b.detect("service disconnection"):
    print(f"  [{r['score']}] {r['text'][:80]}...")

print()
print("--- recall decisions: 'architecture choice' ---")
for r in b.recall_decisions("architecture choice"):
    print(f"  [{r['score']}] {r['text'][:80]}...")

print()
print("BRAIN STATUS: ACTIVE - memory persisted to vectors.db")
