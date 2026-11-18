import csv
import json
import urllib.request
import urllib.error
import os

def load_env():
    env = dict(os.environ)
    try:
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    if k.strip() not in env or not env[k.strip()]:
                        env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env

def main():
    env = load_env()
    project_id = env.get('FIREBASE_PROJECT_ID')
    api_key = env.get('FIREBASE_API_KEY')

    if not project_id or not api_key:
        print("Error: FIREBASE_PROJECT_ID or FIREBASE_API_KEY not found in .env")
        return

    csv_file = 'sns_contents_140.csv' if os.path.exists('sns_contents_140.csv') else 'sns_contents_100.csv'
    posts = []
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            cat = row.get('CategoryShort', 'その他')
            # 新規カテゴリーやDX・キャリア系は LinkedIn との相性も高いため初期値設定可能
            default_platform = "both" if idx > 100 else "threads"
            posts.append({
                'dayNumber': idx,
                'day': row.get('Day', f'Day {idx}'),
                'category': cat,
                'content': row.get('Content', '').strip(),
                'platforms': default_platform
            })

    print(f"Loaded {len(posts)} posts from {csv_file}. Syncing missing posts to Firestore...")

    base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/posts"

    # 既存ドキュメントID一覧を取得
    existing_ids = set()
    list_url = f"{base_url}?pageSize=300&key={api_key}"
    try:
        with urllib.request.urlopen(urllib.request.Request(list_url)) as res:
            data = json.loads(res.read().decode('utf-8'))
            for doc in data.get('documents', []):
                existing_ids.add(doc.get('name', '').split('/')[-1])
    except Exception as e:
        print(f"Notice checking existing docs: {e}")

    print(f"Found {len(existing_ids)} existing documents in Firestore.")

    created_count = 0
    for p in posts:
        doc_id = f"day_{p['dayNumber']}"
        if doc_id in existing_ids:
            continue

        doc_url = f"{base_url}/{doc_id}?key={api_key}"
        fields = {
            "day": {"stringValue": p["day"]},
            "dayNumber": {"integerValue": str(p["dayNumber"])},
            "category": {"stringValue": p["category"]},
            "content": {"stringValue": p["content"]},
            "platforms": {"stringValue": p["platforms"]},
            "status": {"stringValue": "stock"},
            "scheduledAt": {"nullValue": None},
            "publishedAt": {"nullValue": None},
            "threadsMediaId": {"nullValue": None},
            "linkedinPostId": {"nullValue": None},
            "insights": {
                "mapValue": {
                    "fields": {
                        "views": {"integerValue": "0"},
                        "likes": {"integerValue": "0"},
                        "replies": {"integerValue": "0"},
                        "reposts": {"integerValue": "0"},
                        "quotes": {"integerValue": "0"}
                    }
                }
            }
        }

        payload = json.dumps({"fields": fields}).encode('utf-8')
        req = urllib.request.Request(
            doc_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="PATCH"
        )

        try:
            with urllib.request.urlopen(req):
                created_count += 1
                if created_count % 10 == 0:
                    print(f"Added {created_count} new posts...")
        except urllib.error.HTTPError as e:
            print(f"Failed to upload {doc_id}: {e.code} - {e.read().decode('utf-8')}")
            break

    print(f"Sync complete! Added {created_count} new posts. Total in Firestore should now be {len(existing_ids) + created_count}.")

if __name__ == '__main__':
    main()
