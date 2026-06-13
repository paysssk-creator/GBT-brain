"""
Brain Mirror patch - ??project?????????
"""
# In brain_mirror.py, replace the project() learnings/notes fetch with:
# self._fetch_all() which pulls all data via keyword queries

def patch_brain_mirror():
    import sys, os
    sys.path.insert(0, "C:/Users/ADMIN/.gbt/vector_db")
    
    # Read the file
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_mirror.py") if "__file__" in dir() else "C:/Users/ADMIN/.gbt/vector_db/brain_mirror.py"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the old project method's learnings/notes part
    old_pattern = """        # ??????
        learnings = self.brain.know("", top_k=50)
        notes = self.brain.recall("", top_k=30)"""
    
    new_pattern = """        # ???????? (?????????)
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
        notes = all_items  # ????"""
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched brain_mirror.py project() to fetch all data")
        return True
    else:
        print("Old pattern not found, file may already be patched")
        return False

if __name__ == "__main__":
    patch_brain_mirror()
