"""
GBT Dimension Engine - ??????? (Part 2)
"""
import json, time, os, sys
from datetime import datetime
from dimension_space import DIMENSIONS, LocalModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class DimensionEngine:
    def __init__(self):
        self.model = LocalModel()
        from brain import Brain
        self.brain = Brain()
        self.history = self._load_history()

    def _load_history(self):
        f = os.path.join(os.path.dirname(__file__), "dimension_history.json")
        return json.load(open(f)) if os.path.exists(f) else {"runs": [], "total_scores": {}}

    def _save_history(self):
        json.dump(self.history, open(os.path.join(os.path.dirname(__file__), "dimension_history.json"), "w"), indent=2)

    def analyze(self, target_name, data):
        """??????? - ?????9????????"""
        print(f"\n{'='*60}")
        print(f"  Dimension Analysis: {target_name}")
        print(f"  Model: {self.model.backend['name']}")
        print(f"{'='*60}")

        results = {"target": target_name, "timestamp": datetime.now().isoformat(), "dimensions": {}, "total": 0, "suggestions": []}
        total_weighted = 0
        total_weight = 0

        for dim_id, dim in DIMENSIONS.items():
            # ???????????
            prompt = f"""Analyze the following from a {dim['name']} ({dim_id}) perspective:
Questions to answer:
{chr(10).join(f'- {q}' for q in dim['questions'])}
Return a score 0-100 and brief analysis."""

            analysis = self.model.analyze(prompt, data)

            # ????
            score = self._extract_score(analysis, dim_id, data)
            weighted = score * dim["weight"]
            total_weighted += weighted
            total_weight += dim["weight"]

            results["dimensions"][dim_id] = {
                "name": dim["name"],
                "weight": dim["weight"],
                "score": round(score, 1),
                "weighted": round(weighted, 1),
                "analysis": str(analysis)[:200]
            }

            icon = "" if score >= 80 else "" if score >= 60 else ""
            print(f"  {dim['icon']} {dim['name']:8s}: {score:5.1f}/100 {icon}")

            # ????????
            if score < 60:
                sug = f"[{dim['name']}] ??{score:.0f}???: {dim['questions'][0]}"
                results["suggestions"].append(sug)

        results["total"] = round(total_weighted / total_weight, 1) if total_weight > 0 else 0
        print(f"  {'?'*40}")
        print(f"  Overall Score: {results['total']}/100")

        # ???Brain
        self._store_results(target_name, results)

        # ????
        self.history["runs"].append(results)
        if len(self.history["runs"]) > 50:
            self.history["runs"] = self.history["runs"][-50:]
        self._save_history()

        return results

    def _extract_score(self, analysis, dim_id, data):
        """??????????"""
        if isinstance(analysis, str):
            try:
                # Try JSON parse
                parsed = json.loads(analysis)
                if isinstance(parsed, dict) and dim_id in parsed:
                    return float(parsed[dim_id])
                if isinstance(parsed, (int, float)):
                    return float(parsed)
            except:
                pass
            # ??????
            import re
            match = re.search(r'\b(\d{2,3})\b', str(analysis))
            if match:
                s = int(match.group(1))
                return min(s, 100) if s <= 100 else s / 10

        # ?????
        dim = DIMENSIONS[dim_id]
        text = json.dumps(data, ensure_ascii=False).lower() if isinstance(data, dict) else str(data).lower()
        hits = sum(1 for kw in dim["keywords"] if kw in text)
        return min(hits * 100 / max(len(dim["keywords"]), 1), 100)

    def _store_results(self, target, results):
        """???????Brain"""
        dims = {k: v["score"] for k, v in results["dimensions"].items()}
        self.brain.learn(
            f"{target}: Overall={results['total']}/100, " +
            f"Top={max(dims,key=dims.get)}={dims[max(dims,key=dims.get)]}, " +
            f"Weak={min(dims,key=dims.get)}={dims[min(dims,key=dims.get)]}",
            source="dimension-analysis"
        )
        for sug in results.get("suggestions", []):
            self.brain.learn(sug, source="dimension-suggestion")

    def run_simulation(self, target, base_data, mutations):
        """?????? - ????????????"""
        print(f"\n  Simulation: {len(mutations)} mutations for {target}")
        sim_results = []

        # ??
        base = self.analyze(f"{target}/baseline", base_data)

        # ????
        for i, (mut_name, mut_data) in enumerate(mutations.items()):
            result = self.analyze(f"{target}/{mut_name}", mut_data)
            delta = result["total"] - base["total"]
            sim_results.append({
                "mutation": mut_name,
                "score": result["total"],
                "delta": round(delta, 1),
                "better": delta > 0
            })
            print(f"    {mut_name}: {result['total']} ({'+'if delta>0 else ''}{delta} vs baseline)")

        # ??
        sim_results.sort(key=lambda x: x["score"], reverse=True)
        return {"baseline": base["total"], "mutations": sim_results, "best": sim_results[0] if sim_results else None}

    def evolve_from_analysis(self, target, analysis_results):
        """?????????????"""
        weak_dims = [(k, v["score"]) for k, v in analysis_results["dimensions"].items() if v["score"] < 60]
        strong_dims = [(k, v["score"]) for k, v in analysis_results["dimensions"].items() if v["score"] >= 80]

        plan = {
            "target": target,
            "overall": analysis_results["total"],
            "weak_points": [{"dim": k, "score": s, "dim_name": DIMENSIONS[k]["name"]} for k, s in weak_dims],
            "strengths": [{"dim": k, "score": s, "dim_name": DIMENSIONS[k]["name"]} for k, s in strong_dims],
            "evolve_plan": []
        }

        for w in weak_dims:
            dim = DIMENSIONS[w[0]]
            plan["evolve_plan"].append({
                "dimension": w[0],
                "dim_name": dim["name"],
                "current_score": w[1],
                "action": f"????{dim['name']}????{w[1]}???: {dim['questions'][0]}"
            })

        # ??????
        self.brain.note(
            f"Evolution Plan: {target}",
            json.dumps(plan, indent=2, ensure_ascii=False),
            tags=["evolution", "plan", target]
        )

        return plan

    def trend(self):
        """??????"""
        if not self.history["runs"]:
            return {"message": "No analysis history yet"}
        recent = self.history["runs"][-5:]
        trends = {}
        for run in recent:
            t = run["target"]
            if t not in trends:
                trends[t] = []
            trends[t].append(run["total"])
        return {
            "runs": len(self.history["runs"]),
            "latest": self.history["runs"][-1]["total"] if self.history["runs"] else 0,
            "trends": trends
        }
