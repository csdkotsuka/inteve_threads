import argparse
import datetime
import json
import time
import urllib.request
import urllib.error
from threads_api import ThreadsAPI, load_env
from linkedin_api import LinkedInAPI

def get_now_iso():
    jst = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(jst).isoformat()

def get_firestore_posts(project_id, api_key):
    """Firestoreから全投稿ドキュメントを取得"""
    base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/posts?pageSize=300&key={api_key}"
    req = urllib.request.Request(base_url)
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        docs = data.get('documents', [])
        posts = []
        for doc in docs:
            name = doc.get('name', '')
            doc_id = name.split('/')[-1]
            fields = doc.get('fields', {})

            def get_val(f):
                if not f: return None
                if 'stringValue' in f: return f['stringValue']
                if 'integerValue' in f: return int(f['integerValue'])
                if 'nullValue' in f: return None
                if 'mapValue' in f:
                    m = f['mapValue'].get('fields', {})
                    return {k: get_val(v) for k, v in m.items()}
                return None

            posts.append({
                'doc_id': doc_id,
                'name': name,
                'day': get_val(fields.get('day')),
                'dayNumber': get_val(fields.get('dayNumber')),
                'category': get_val(fields.get('category')),
                'content': get_val(fields.get('content')),
                'platforms': get_val(fields.get('platforms')) or 'threads',
                'status': get_val(fields.get('status')) or 'stock',
                'scheduledAt': get_val(fields.get('scheduledAt')),
                'publishedAt': get_val(fields.get('publishedAt')),
                'threadsMediaId': get_val(fields.get('threadsMediaId')),
                'linkedinPostId': get_val(fields.get('linkedinPostId')),
                'insights': get_val(fields.get('insights')) or {}
            })
        return posts

def update_firestore_post(project_id, api_key, doc_id, fields_to_update):
    """Firestoreの特定フィールドを更新"""
    base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/posts/{doc_id}?key={api_key}"
    
    update_masks = []
    firestore_fields = {}

    for k, v in fields_to_update.items():
        update_masks.append(f"updateMask.fieldPaths={k}")
        if v is None:
            firestore_fields[k] = {"nullValue": None}
        elif isinstance(v, str):
            firestore_fields[k] = {"stringValue": v}
        elif isinstance(v, int):
            firestore_fields[k] = {"integerValue": str(v)}
        elif isinstance(v, dict):
            map_fields = {}
            for mk, mv in v.items():
                if isinstance(mv, int):
                    map_fields[mk] = {"integerValue": str(mv)}
                elif isinstance(mv, str):
                    map_fields[mk] = {"stringValue": mv}
                else:
                    map_fields[mk] = {"nullValue": None}
            firestore_fields[k] = {"mapValue": {"fields": map_fields}}

    query_str = "&".join(update_masks)
    patch_url = f"{base_url}&{query_str}"

    payload = json.dumps({"fields": firestore_fields}).encode('utf-8')
    req = urllib.request.Request(patch_url, data=payload, headers={"Content-Type": "application/json"}, method="PATCH")
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def parse_iso_utc(iso_str):
    if not iso_str:
        return None
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
    except Exception:
        return None

def check_and_publish():
    env = load_env()
    project_id = env.get('FIREBASE_PROJECT_ID')
    api_key = env.get('FIREBASE_API_KEY')
    threads = ThreadsAPI()
    linkedin = LinkedInAPI()

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_iso = get_now_iso()
    print(f"[{now_iso}] Checking scheduled posts... (LinkedIn enabled: {linkedin.is_configured()})")

    try:
        posts = get_firestore_posts(project_id, api_key)
    except Exception as e:
        print(f"Error fetching Firestore posts: {e}")
        return

    scheduled_posts = []
    for p in posts:
        if p.get('status') == 'scheduled' and p.get('scheduledAt'):
            sched_dt = parse_iso_utc(p['scheduledAt'])
            if sched_dt and sched_dt <= now_utc:
                scheduled_posts.append(p)
    scheduled_posts.sort(key=lambda x: x['scheduledAt'])

    for post in scheduled_posts:
        print(f"Found post ready for publishing: {post['day']} (Target: {post['platforms']}, Scheduled: {post['scheduledAt']})")
        text = post.get('content')
        if not text:
            print(f"Skipping empty post: {post['day']}")
            continue

        target = post.get('platforms', 'threads')
        update_data = {}
        published_any = False

        # 1. Threads 投稿
        if target in ('threads', 'both'):
            try:
                res = threads.publish_text_post(text)
                media_id = res.get('media_id')
                print(f"  -> Threads published! Media ID: {media_id}")
                update_data['threadsMediaId'] = media_id
                published_any = True
            except Exception as e:
                print(f"  -> Failed to publish to Threads ({post['day']}): {e}")

        # 2. LinkedIn 投稿
        if target in ('linkedin', 'both'):
            if linkedin.is_configured():
                try:
                    li_res = linkedin.publish_text_post(text)
                    li_id = li_res.get('post_id')
                    print(f"  -> LinkedIn published! Post ID: {li_id}")
                    update_data['linkedinPostId'] = li_id
                    published_any = True
                except Exception as e:
                    print(f"  -> Failed to publish to LinkedIn ({post['day']}): {e}")
            else:
                print(f"  -> LinkedIn token not configured; skipping LinkedIn for {post['day']}.")

        if published_any:
            update_data['status'] = 'published'
            update_data['publishedAt'] = get_now_iso()
            update_firestore_post(project_id, api_key, post['doc_id'], update_data)
            print(f"Updated Firestore status to 'published' for {post['doc_id']}.")

    # Update insights for published Threads posts
    published_with_media = [p for p in posts if p.get('threadsMediaId')]
    if published_with_media:
        print(f"Updating Threads insights for {len(published_with_media)} published posts...")
        for p in published_with_media:
            m_id = p['threadsMediaId']
            insights = threads.get_post_insights(m_id)
            if insights:
                print(f"Insights for {p['day']}: Views={insights.get('views')}, Likes={insights.get('likes')}")
                update_firestore_post(project_id, api_key, p['doc_id'], {'insights': insights})

def main():
    parser = argparse.ArgumentParser(description="Threads & LinkedIn Auto-Poster")
    parser.add_argument('--daemon', action='store_true', help="Run continuously in background (checks every 5 minutes)")
    parser.add_argument('--interval', type=int, default=300, help="Check interval in seconds for daemon mode (default: 300)")
    args = parser.parse_args()

    if args.daemon:
        print(f"Starting Auto-Poster daemon (checking every {args.interval} seconds)...")
        while True:
            try:
                check_and_publish()
            except Exception as e:
                print(f"Error in cycle: {e}")
            time.sleep(args.interval)
    else:
        check_and_publish()

if __name__ == '__main__':
    main()
