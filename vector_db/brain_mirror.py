"""
GBT Brain Mirror - ??????
3D??? + ???? + ????
"""
import json, os, sys, math, random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain import Brain
from dimension_space import DIMENSIONS

class BrainMirror:
    """?????? - ?Brain???????????"""

    def __init__(self):
        self.brain = Brain()
        self.nodes = []
        self.edges = []
        self.clusters = {}

    def project(self):
        """?Brain????????????"""
        # ??????
        # 全量拉取所有知识(通过维度关键词搜索)
        seen = set()
        all_items = []
        for dim_id, dim_info in DIMENSIONS.items():
            for kw in dim_info["keywords"][:3]:
                for item in self.brain.know(kw, top_k=10) + self.brain.recall(kw, top_k=10):
                    key = item.get("id", item.get("text", "")[:30])
                    if key not in seen:
                        seen.add(key)
                        all_items.append(item)
        learnings = all_items
        notes = all_items

        center = (0, 0, 0)
        theta = 0
        node_id = 0

        # ?????
        for dim_id, dim_info in DIMENSIONS.items():
            # ??????????????
            angle = (list(DIMENSIONS.keys()).index(dim_id) / len(DIMENSIONS)) * math.pi * 2
            base_x = math.cos(angle) * 5
            base_y = (random.random() - 0.5) * 3
            base_z = math.sin(angle) * 5

            cluster_nodes = []

            # ?????????????
            for i, item in enumerate(learnings):
                text = item.get("text", "").lower()
                kw_hits = sum(1 for kw in dim_info["keywords"] if kw in text)
                if kw_hits > 0:
                    offset_angle = (i / max(len(learnings), 1)) * math.pi * 2
                    r = 1 + kw_hits * 0.5
                    node = {
                        "id": f"node_{node_id}",
                        "x": base_x + math.cos(offset_angle) * r,
                        "y": base_y + (random.random() - 0.5) * 2,
                        "z": base_z + math.sin(offset_angle) * r,
                        "label": text[:40],
                        "type": "learning",
                        "dimension": dim_id,
                        "score": item.get("score", 0),
                        "size": 0.5 + kw_hits * 0.3
                    }
                    self.nodes.append(node)
                    cluster_nodes.append(node["id"])
                    node_id += 1

            self.clusters[dim_id] = {
                "name": dim_info["name"],
                "icon": dim_info["icon"],
                "center": (base_x, base_y, base_z),
                "nodes": cluster_nodes,
                "count": len(cluster_nodes)
            }

        # ?????? (???) - ????????
        self._build_edges()

        return self.export()

    def _build_edges(self):
        """????????? - ????"""
        for i, na in enumerate(self.nodes):
            for j, nb in enumerate(self.nodes):
                if i >= j: continue
                # ????????
                dx = na["x"] - nb["x"]
                dy = na["y"] - nb["y"]
                dz = na["z"] - nb["z"]
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                # ????????
                if dist < 4.0:
                    self.edges.append({
                        "from": na["id"],
                        "to": nb["id"],
                        "distance": round(dist, 2),
                        "strength": round(1 - dist/4.0, 3)
                    })

    def export(self):
        return {
            "meta": {
                "name": "GBT Brain Mirror",
                "timestamp": datetime.now().isoformat(),
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "dimensions": len(self.clusters),
                "brain_stats": self.brain.stats()
            },
            "clusters": self.clusters,
            "nodes": self.nodes,
            "edges": self.edges
        }

    def query(self, concept):
        """?????????????"""
        results = []
        for node in self.nodes:
            if concept.lower() in node["label"].lower():
                results.append(node)
        # ?????
        if results:
            return {
                "concept": concept,
                "location": results[0],
                "neighbors": [e for e in self.edges
                    if e["from"] == results[0]["id"] or e["to"] == results[0]["id"]]
            }
        return {"concept": concept, "found": False}

    def render_html(self):
        """??3D???HTML"""
        data = self.export()
        nodes_json = json.dumps(data["nodes"])
        edges_json = json.dumps(data["edges"])
        clusters_json = json.dumps(data["clusters"])

        html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>GBT Brain Mirror</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#0a0a1a; overflow:hidden; font-family:monospace; }}
canvas {{ display:block; }}
#info {{ position:fixed; top:10px; left:10px; color:#0f0; font-size:12px; }}
#legend {{ position:fixed; bottom:10px; right:10px; color:#aaa; font-size:11px; }}
.legend-item {{ margin:2px 0; }}
</style></head><body>
<div id="info">GBT Brain Mirror | Nodes: {len(data['nodes'])} | Edges: {len(data['edges'])}<br>
Brain: {data['meta']['brain_stats']}</div>
<div id="legend">
'''
        colors = ["#ff4444","#44ff44","#4444ff","#ffff44","#ff44ff","#44ffff","#ff8844","#8844ff","#44ff88"]
        for i, (dim_id, cluster) in enumerate(data["clusters"].items()):
            html += f'<div class="legend-item"><span style="color:{colors[i%9]}">{chr(9608)}</span> {cluster["name"]} ({cluster["count"]})</div>'

        html += f'''</div>
<script>
const nodes = {nodes_json};
const edges = {edges_json};
const clusters = {clusters_json};

// Simple WebGL/Canvas 3D Brain Mirror
const canvas = document.createElement("canvas");
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

let rotX = 0, rotY = 0, zoom = 150;
let autoRotate = true;

function resize() {{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}}
window.onresize = resize; resize();

// Mouse drag to rotate
let dragging = false, lastX = 0, lastY = 0;
canvas.onmousedown = e => {{ dragging=true; lastX=e.clientX; lastY=e.clientY; autoRotate=false; }};
canvas.onmouseup = () => dragging=false;
canvas.onmousemove = e => {{ if(dragging){{ rotY+=(e.clientX-lastX)*0.005; rotX+=(e.clientY-lastY)*0.005; lastX=e.clientX; lastY=e.clientY; }} }};
canvas.onwheel = e => {{ zoom+=e.deltaY*0.1; zoom=Math.max(30,Math.min(500,zoom)); }};

const dimColors = {{"security":"#ff4444","performance":"#44ff44","architecture":"#4444ff","quality":"#ffff44","innovation":"#ff44ff","scalability":"#44ffff","reliability":"#ff8844","intelligence":"#8844ff","ecosystem":"#44ff88"}};

function project3D(x, y, z) {{
    // Rotate around Y
    const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
    const rx = x * cosY - z * sinY;
    const rz = x * sinY + z * cosY;
    // Rotate around X
    const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
    const ry = y * cosX - rz * sinX;
    const rz2 = y * sinX + rz * cosX;
    const scale = zoom / (rz2 + 15);
    return {{ x: canvas.width/2 + rx * scale, y: canvas.height/2 - ry * scale, z: rz2 }};
}}

function draw() {{
    ctx.fillStyle = "rgba(10,10,26,0.3)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Sort by Z for depth
    const projected = nodes.map(n => {{ const p = project3D(n.x, n.y, n.z); return {{...n, ...p}}; }});
    projected.sort((a,b) => a.z - b.z);

    // Draw edges
    for (const e of edges.slice(0,200)) {{
        const from = projected.find(n => n.id === e.from);
        const to = projected.find(n => n.id === e.to);
        if (!from || !to) continue;
        ctx.strokeStyle = `rgba(100,100,255,${{e.strength*0.3}})`;
        ctx.lineWidth = e.strength * 2;
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.stroke();
    }}

    // Draw nodes
    for (const n of projected) {{
        const color = dimColors[n.dimension] || "#8888ff";
        const r = n.size * 5;
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI*2);
        ctx.fill();
        ctx.globalAlpha = 1;

        // Glow
        ctx.shadowColor = color;
        ctx.shadowBlur = 8;
        ctx.fillStyle = "rgba(255,255,255,0.3)";
        ctx.beginPath();
        ctx.arc(n.x, n.y, r*0.5, 0, Math.PI*2);
        ctx.fill();
        ctx.shadowBlur = 0;

        if (n.z > 0 && n.score > 2) {{
            ctx.fillStyle = "#fff";
            ctx.font = "10px monospace";
            ctx.fillText(n.label, n.x + r + 2, n.y + 3);
        }}
    }}

    if (autoRotate) rotY += 0.003;
    requestAnimationFrame(draw);
}}

draw();
</script></body></html>'''
        return html


if __name__ == "__main__":
    mirror = BrainMirror()
    data = mirror.project()

    print(f"Brain Mirror activated!")
    print(f"  Nodes: {data['meta']['total_nodes']}")
    print(f"  Edges: {data['meta']['total_edges']}")
    print(f"  Dimensions: {data['meta']['dimensions']}")
    print(f"  Brain: {data['meta']['brain_stats']}")

    for dim_id, cluster in data["clusters"].items():
        print(f"    {cluster['icon']} {cluster['name']:10s}: {cluster['count']} nodes")

    # Generate HTML
    html = mirror.render_html()
    html_path = os.path.join(os.path.dirname(__file__), "brain_mirror.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  Mirror HTML: {html_path}")
    print(f"  Open in browser to explore the Brain Mirror!")
