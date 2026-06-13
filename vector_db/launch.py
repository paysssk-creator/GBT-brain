# -*- coding: utf-8 -*-
"""
GBT Brain Launcher - 统一启动入口
品牌: GBT小土豆全能开发者
用法: python launch.py [brain|mirror|mindspace|evolve|dimensions|all]
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from splash import splash

GT_BRAND = "GBT小土豆全能开发者"
GT_TAG = "GBT xiaotudou AI Developer"

def show_title():
    splash("active", delay=0)

def run_brain():
    show_title()
    print("  Starting Brain Core...")
    from brain import Brain
    b = Brain()
    stats = b.stats()
    print(f"  Brain Online: {stats}")
    return b

def run_mindspace():
    show_title()
    print("  Starting MindSpace Scanner...")
    from mindspace import MindSpaceEngine
    m = MindSpaceEngine()
    top = m.scan()
    print(f"  Collected: {len(top)} items")
    for i, item in enumerate(top[:5]):
        print(f"    {i+1}. [{item.get('source','')}] {item.get('title','')[:70]}")
    return m

def run_mirror():
    show_title()
    print("  Projecting Brain Mirror...")
    from brain_mirror import BrainMirror
    m = BrainMirror()
    data = m.project()
    html = m.render_html()
    path = os.path.join(os.path.dirname(__file__), "brain_mirror.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    os.startfile(path)
    print(f"  Mirror: {data['meta']['total_nodes']} nodes, {data['meta']['total_edges']} edges")
    print(f"  Browser opened: {path}")
    return m

def run_evolve():
    show_title()
    print("  Running Self-Evolution Cycle...")
    from self_evolve import run_evolution
    result = run_evolution()
    print(f"  Evolution Complete: {result['insights']} insights")
    return result

def run_dimensions():
    show_title()
    print("  Running Multi-Dimensional Analysis...")
    from mindmap_extender import ExtendedDimensionEngine
    engine = ExtendedDimensionEngine()
    data = {"features": ["self-evolve","vector-search","ai-memory","mindspace","multidimensional","desktop-control"]}
    result = engine.mindmap_analyze(f"{GT_BRAND} System", data)
    print(f"  Score: {result['analysis']['total']}/100")
    print(f"  Nodes: {result['stats']['nodes']}")
    return result

def run_landing():
    """打开GBT霸气首页 (landing.html) — 默认启动页"""
    show_title()
    print("  ⚕ 正在启动 GBT小土豆全能开发者 霸气首页...")
    landing_path = os.path.join(os.path.dirname(__file__), "..", "landing.html")
    landing_path = os.path.abspath(landing_path)
    if os.path.exists(landing_path):
        os.startfile(landing_path)
        print(f"  ✅ 霸气首页已打开: {landing_path}")
    else:
        print(f"  ❌ landing.html 未找到，尝试打开 public/index.html")
        pub_path = os.path.join(os.path.dirname(__file__), "..", "public", "index.html")
        pub_path = os.path.abspath(pub_path)
        if os.path.exists(pub_path):
            os.startfile(pub_path)
        else:
            print("  ❌ 未找到任何首页文件，运行全系统启动...")
            run_all()

def run_all():
    show_title()
    print("  === Full System Boot ===")
    print()
    run_landing()
    print()
    run_brain()
    print()
    run_mindspace()
    print()
    run_evolve()
    print()
    run_dimensions()
    print()
    print(f"\n  {GT_BRAND} - All Systems Online!")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "landing"
    commands = {
        "landing": run_landing,
        "brain": run_brain,
        "mirror": run_mirror,
        "mindspace": run_mindspace,
        "evolve": run_evolve,
        "dimensions": run_dimensions,
        "all": run_all,
    }
    cmd = commands.get(arg, run_landing)
    try:
        cmd()
    except KeyboardInterrupt:
        print(f"\n  {GT_BRAND} - Shutdown complete.")
    except Exception as e:
        print(f"  Error: {e}")
        sys.exit(1)
