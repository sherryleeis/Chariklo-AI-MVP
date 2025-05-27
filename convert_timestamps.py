import sys
import json
import datetime


def human_time(ts):
    try:
        return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return str(ts)

def process_jsonl(path):
    with open(path, 'r') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('//'):
                continue
            obj = json.loads(line)
            ts = obj.get('timestamp')
            if ts:
                print(f"[{human_time(ts)}] {json.dumps(obj, ensure_ascii=False)}")
            else:
                print(json.dumps(obj, ensure_ascii=False))

def process_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    # Try to find all timestamps recursively
    def walk(obj):
        if isinstance(obj, dict):
            if 'timestamp' in obj:
                obj['timestamp_human'] = human_time(obj['timestamp'])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_timestamps.py <file.jsonl|file.json>")
        return
    path = sys.argv[1]
    if path.endswith('.jsonl'):
        process_jsonl(path)
    elif path.endswith('.json'):
        process_json(path)
    else:
        print("Unsupported file type. Use .json or .jsonl")

if __name__ == "__main__":
    main()
