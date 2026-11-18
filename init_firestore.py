import csv
import json
import urllib.request
import urllib.error
import time

def load_env():
    env = {}
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def main():
    env = load_env()
    project_id = env.get('FIREBASE_PROJECT_ID')
    api_key = env.get('FIREBASE_API_KEY')

    if not project_id or not api_key:
        print("Error: FIREBASE_PROJECT_ID or FIREBASE_API_KEY not found in .env")
        return

    # Read CSV
    posts = []
    with open('sns_contents_100.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            posts.append({
                'dayNumber': idx,
                'day': row.get('Day', f'Day {idx}'),
                'category': row.get('CategoryShort', 'その他'),
                'content': row.get('Content', '').strip()
            })

    print(f"Loaded {len(posts)} posts from CSV. Checking Firestore...")

    # Upload to Firestore via REST API
    # Document path: projects/{project_id}/databases/(default)/documents/posts/day_{dayNumber}
    base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/posts"

    # Check if documents already exist to avoid overwriting modified content
    existing_check_url = f"{base_url}/day_1?key={api_key}"
    already_initialized = False
    try:
        req = urllib.request.Request(existing_check_url)
        with urllib.request.urlopen(req) as res:
            if res.status == 200:
                already_initialized = True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            already_initialized = False
        else:
            print(f"Firestore check returned {e.code}: {e.read().decode('utf-8')}")

    if already_initialized:
        print("Notice: 'day_1' already exists in Firestore! Checking total count before deciding.")
        # Proceed with merge/patch or skip if already populated
    
    print(f"Initializing {len(posts)} posts to Firestore...")

    success_count = 0
    for p in posts:
        doc_id = f"day_{p['dayNumber']}"
        doc_url = f"{base_url}/{doc_id}?key={api_key}"

        # Firestore REST format
        fields = {
            "day": {"stringValue": p["day"]},
            "dayNumber": {"integerValue": str(p["dayNumber"])},
            "category": {"stringValue": p["category"]},
            "content": {"stringValue": p["content"]},
            "status": {"stringValue": "stock"},  # stock | scheduled | published
            "scheduledAt": {"nullValue": None},
            "publishedAt": {"nullValue": None},
            "threadsMediaId": {"nullValue": None},
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

        # Use PATCH to create or update without deleting untouched fields
        patch_url = f"{doc_url}&updateMask.fieldPaths=day&updateMask.fieldPaths=dayNumber&updateMask.fieldPaths=category&updateMask.fieldPaths=content"
        # If document doesn't exist, we send full doc
        payload = json.dumps({"fields": fields}).encode('utf-8')

        req = urllib.request.Request(
            f"{doc_url}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="PATCH"
        )

        try:
            with urllib.request.urlopen(req) as res:
                success_count += 1
                if success_count % 20 == 0 or success_count == len(posts):
                    print(f"Uploaded {success_count}/{len(posts)} posts...")
        except urllib.error.HTTPError as e:
            print(f"Failed to upload {doc_id}: {e.code} - {e.read().decode('utf-8')}")
            break
        except Exception as e:
            print(f"Error on {doc_id}: {e}")
            break

    print(f"Initialization finished. Successfully set {success_count} posts in Firestore.")

if __name__ == '__main__':
    main()
