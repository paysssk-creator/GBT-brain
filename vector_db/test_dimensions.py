import sys,os; sys.path.insert(0,"C:/Users/ADMIN/.gbt/vector_db")
from mindmap_extender import ExtendedDimensionEngine
engine = ExtendedDimensionEngine()
data = {
    "languages": ["TypeScript","Python","JavaScript"],
    "features": ["self-evolve","vector-search","ai-memory","mindspace","multidimensional-analysis","security-scan","desktop-control","mcp-server"],
    "dependencies": ["electron","react","antd","openai","chromadb","sqlite3","ws"],
    "security_modules": ["input-validator","secure-file-system","audit-log","auth-system"],
    "ai_modules": ["self_evolve","mindspace","brain","dimension_engine","collector"],
    "architecture": "MCP-stdio + Electron + React + Python-Brain",
    "performance": "WAL-mode SQLite, async operations, embedded db",
    "reliability": "embedded database no disconnect, WAL journaling",
    "innovation": "9-dimension reasoning, mindmap extension, autonomous evolution",
    "scalability": "PostgreSQL+pgvector ready via Docker compose",
    "intelligence": "autonomous learning, pattern detection, semantic search"
}
result = engine.mindmap_analyze("GBT Self-Evolving Platform", data)
print(f"Overall: {result['analysis']['total']}/100")
print(f"Nodes: {result['stats']['nodes']}")
for a in result["evolution_plan"]["evolve_plan"][:5]:
    print(f"  Action: {a['dim_name']} ({a['current_score']}) -> {a['action'][:80]}")
print(f"Brain: {engine.engine.brain.stats()}")
print("Done!")
