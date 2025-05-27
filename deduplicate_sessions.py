import sys
import json
import os
from collections import OrderedDict

def deduplicate_jsonl(path):
    seen = set()
    deduped = []
    with open(path, 'r') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('//'):
                continue
            obj = json.loads(line)
            # Use content+type+user_prompt as a unique key
            key = json.dumps({k: obj.get(k) for k in ('type','content','user_prompt')}, sort_keys=True)
            if key not in seen:
                seen.add(key)
                deduped.append(obj)
    with open(path, 'w') as f:
        for obj in deduped:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    print(f"Deduplicated {path}: {len(deduped)} unique entries.")

def deduplicate_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    changed = False
    # Deduplicate 'reflections' if present
    if isinstance(data, dict) and 'reflections' in data:
        seen = set()
        deduped = []
        for obj in data['reflections']:
            key = json.dumps({k: obj.get(k) for k in ('type','content','user_prompt')}, sort_keys=True)
            if key not in seen:
                seen.add(key)
                deduped.append(obj)
        if len(deduped) != len(data['reflections']):
            data['reflections'] = deduped
            changed = True
    if changed:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Deduplicated {path}: {len(data['reflections'])} unique reflections.")
    else:
        print(f"No duplicates found in {path}.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python deduplicate_sessions.py <file.jsonl|file.json>")
        return
    path = sys.argv[1]
    if path.endswith('.jsonl'):
        deduplicate_jsonl(path)
    elif path.endswith('.json'):
        deduplicate_json(path)
    else:
        print("Unsupported file type. Use .json or .jsonl")

if __name__ == "__main__":
    main()
