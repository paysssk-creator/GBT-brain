"""
GBT ????????
???? + 9???? + ???? + ??Brain
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mindmap_extender import ExtendedDimensionEngine, MindMap
from dimension_space import DIMENSIONS

print("=" * 65)
print("  GBT Multi-Dimensional Space - ???????")
print(f"  Dimensions: {len(DIMENSIONS)} | Model: Local Heuristic")
print("=" * 65)

engine = ExtendedDimensionEngine()

# ??1: ?????????????
target1 = "GBT Creator - ???? MCP Server"
data1 = {
    "type": "project",
    "files": 246,
    "lines": 148742,
    "languages": ["TypeScript", "Python", "JavaScript"],
    "features": ["MCP server", "desktop control", "security scanner", "self-evolve", "vector db"],
    "dependencies": ["electron", "react", "antd", "openai", "ws", "zustand"],
    "security": ["input-validator", "secure-file-system", "audit-log", "auth-system"]
}

print("\n--- Test 1: Project Analysis ---")
result1 = engine.mindmap_analyze(target1, data1)
print(f"\n  Analysis Score: {result1['analysis']['total']}/100")
print(f"  MindMap Nodes: {result1['stats']['nodes']}")
print(f"  Connections: {result1['stats']['connections']}")
print(f"  Evolution Plan: {len(result1['evolution_plan']['evolve_plan'])} actions")

# ??2: ????????
target2 = "MindSpace Data Pipeline"
data2 = {
    "type": "pipeline",
    "sources": ["GitHub API", "HackerNews API", "Dev.to API", "Reddit API"],
    "model": "ChromaDB all-MiniLM-L6-v2 (80MB)",
    "storage": "SQLite vectors.db (140KB)",
    "output": "Brain memory system",
    "features": ["auto-fetch", "scoring", "dedup", "semantic search"]
}

print("\n--- Test 2: Pipeline Analysis ---")
result2 = engine.mindmap_analyze(target2, data2)
print(f"\n  Analysis Score: {result2['analysis']['total']}/100")

# ??3: ??????
print("\n--- Test 3: Mutation Simulation ---")
mutations = {
    "add_cache": {**data1, "cache": "redis", "cache_strategy": "LRU"},
    "add_distributed": {**data1, "distributed": True, "replicas": 3},
    "add_streaming": {**data1, "streaming": True, "websocket": True},
}
sim = engine.engine.run_simulation(target1, data1, mutations)
print(f"\n  Baseline: {sim['baseline']}")
print(f"  Best: {sim['best']['mutation']} ({sim['best']['score']})")

# ??
print(f"\n--- Evolution Trend ---")
trend = engine.engine.trend()
print(f"  Total runs: {trend['runs']}")
print(f"  Latest score: {trend['latest']}")

print("\n" + "=" * 65)
print("  Multi-Dimensional Space Active!")
print(f"  Files: dimension_space.py, dimension_engine.py, mindmap_extender.py")
print("=" * 65)
