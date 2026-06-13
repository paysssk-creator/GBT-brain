"""
GBT Self-Evolve Engine - ????????
???????? + MindSpace????? ? ????
"""
import os, sys, json, time, re, hashlib
from datetime import datetime
from collections import Counter

sys.path.insert(0, "C:/Users/ADMIN/.gbt/vector_db")

CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".c", ".cpp", ".java", ".rb", ".php"}
SKIP_DIRS = {"node_modules", "__pycache__", ".git", "dist", "build", "out", "target", ".next"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Cargo.lock"}
PROJECTS = [
    "C:/Users/ADMIN/GBTxiaotudouchuangzaozhushou",
    "C:/Users/ADMIN/.cline",
    "C:/Users/ADMIN/.gbt",
]

def scan_project(root):
    """?????????"""
    files = []
    modules = Counter()
    patterns_found = []
    total_lines = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in filenames:
            if fname in SKIP_FILES: continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in CODE_EXTS: continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                lines = content.split("\n")
                total_lines += len(lines)
                rel = os.path.relpath(fpath, root).replace("\\", "/")
                files.append({"path": rel, "ext": ext, "lines": len(lines)})

                # ????/??
                imports = extract_imports(content, ext)
                for imp in imports:
                    modules[imp] += 1

                # ????
                pats = find_patterns(content, rel)
                patterns_found.extend(pats)
            except:
                pass

    return {
        "root": root,
        "files": len(files),
        "total_lines": total_lines,
        "modules": dict(modules.most_common(50)),
        "patterns": patterns_found[:20],
        "top_files": sorted(files, key=lambda x: x["lines"], reverse=True)[:20]
    }

def extract_imports(content, ext):
    """??????import/require"""
    imports = []
    if ext in {".js", ".ts", ".jsx", ".tsx"}:
        imports.extend(re.findall(r'from\s+[\'\"]([^\'\"]+)', content))
        imports.extend(re.findall(r'require\s*\(\s*[\'\"]([^\'\"]+)', content))
        imports.extend(re.findall(r'import\s+.*?from\s+[\'\"]([^\'\"]+)', content))
    elif ext == ".py":
        imports.extend(re.findall(r'^from\s+(\S+)', content, re.MULTILINE))
        imports.extend(re.findall(r'^import\s+(\S+)', content, re.MULTILINE))
    elif ext in {".go"}:
        imports.extend(re.findall(r'"([^"]+)"', content))
    elif ext in {".rs"}:
        imports.extend(re.findall(r'use\s+(\S+)', content))
    return [i.split("/")[0] if "/" in i else i for i in imports if not i.startswith(".")]

def find_patterns(content, path):
    """???????????"""
    patterns = []
    if "class " in content:
        classes = re.findall(r'class\s+(\w+)', content)
        for cls in classes[:5]:
            patterns.append(f"CLASS:{cls} in {path}")
    if "def " in content or "function " in content:
        funcs = re.findall(r'(?:def|function)\s+(\w+)', content)
        for fn in funcs[:5]:
            patterns.append(f"FUNC:{fn} in {path}")
    if "TODO" in content or "FIXME" in content:
        todos = re.findall(r'(TODO|FIXME|HACK)[: ]*(.+)', content)
        for tag, note in todos[:3]:
            patterns.append(f"{tag}:{note.strip()[:100]} in {path}")
    if "export " in content or "__all__" in content:
        patterns.append(f"MODULE_API in {path}")
    return patterns

def run_evolution():
    """????????"""
    from mindspace import MindSpaceEngine
    from brain import Brain

    brain = Brain()
    mindspace = MindSpaceEngine()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    all_insights = []

    # 1. ????????
    print(f"[{timestamp}] === Self-Evolve Daily Scan ===")
    for proj in PROJECTS:
        name = os.path.basename(proj)
        print(f"  Scanning: {name}...")
        result = scan_project(proj)
        print(f"    {result['files']} files, {result['total_lines']} lines, {len(result['modules'])} modules")

        # ????
        insight = f"{name}: {result['files']} files ({result['total_lines']} lines), top modules: {', '.join(list(result['modules'].keys())[:5])}"
        brain.learn(insight, source="self-scan")
        all_insights.append(insight)

        # ????
        for pat in result["patterns"][:10]:
            brain.pattern(pat, f"Found in {name}", f"{result['files']} files scanned")

    # 2. ??????
    print(f"  Scanning external sources...")
    ext_items = mindspace.scan()
    print(f"    {len(ext_items)} external items collected")

    # 3. ????
    brain.learn(f"Daily scan complete at {timestamp}: {len(PROJECTS)} projects scanned, {len(ext_items)} external items", source="evolve-cycle")

    # 4. ??????
    suggestions = generate_suggestions(brain, all_insights)
    for sug in suggestions:
        brain.learn(sug, source="evolve-suggestion")
        print(f"  Suggestion: {sug[:100]}...")

    stats = brain.stats()
    print(f"\n  Brain: {stats}")
    print(f"  [{timestamp}] Evolution cycle complete!")

    return {
        "timestamp": timestamp,
        "projects_scanned": len(PROJECTS),
        "insights": len(all_insights),
        "suggestions": len(suggestions),
        "brain_stats": stats
    }

def generate_suggestions(brain, insights):
    """????????????"""
    suggestions = []
    # ?????????? ? ?????
    # ???TODO/FIXME ? ????
    # ???????? ? ????

    for ins in insights:
        if "TODO" in ins or "FIXME" in ins:
            suggestions.append(f"Consider fixing pending tasks: {ins[:150]}")
        if "vulnerability" in ins.lower() or "security" in ins.lower():
            suggestions.append(f"Security concern found: {ins[:150]}")

    # Check MindSpace for trending tools
    mindspace_items = brain.recall("github trending", top_k=5)
    for item in mindspace_items[:3]:
        suggestions.append(f"Trending tool to explore: {item['text'][:150]}")

    return suggestions[:5]

if __name__ == "__main__":
    result = run_evolution()
    print("\n" + json.dumps(result, indent=2))
