import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from brain_mirror import BrainMirror
m=BrainMirror()
d=m.project()
json.dump(d,open("mirror_data.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
print(f"Saved: {d['meta']['total_nodes']} nodes, {d['meta']['total_edges']} edges")
