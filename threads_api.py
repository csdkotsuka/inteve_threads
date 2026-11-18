import json
import urllib.request
import urllib.parse
import urllib.error
import time

def load_env():
    import os
    env = dict(os.environ)
    try:
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    # Don't overwrite existing environment variables
                    if k.strip() not in env or not env[k.strip()]:
                        env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env


class ThreadsAPI:
    def __init__(self, access_token=None, user_id=None):
        env = load_env()
        self.access_token = access_token or env.get('THREADS_ACCESS_TOKEN')
        self.user_id = user_id or env.get('THREADS_USER_ID', 'me')
        self.base_url = 'https://graph.threads.net/v1.0'

    def get_profile(self):
        """アカウントのプロフィール情報を取得"""
        url = f"{self.base_url}/me?fields=id,username,name,threads_profile_picture_url&access_token={self.access_token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode('utf-8'))

    def publish_text_post(self, text):
        """
        Threads にテキスト投稿を公開する（2ステップ）
        1. コンテナ作成 (POST /{user_id}/threads)
        2. 公開 (POST /{user_id}/threads_publish)
        """
        # Step 1: Create Container
        container_url = f"{self.base_url}/{self.user_id}/threads"
        data = urllib.parse.urlencode({
            'media_type': 'TEXT',
            'text': text,
            'access_token': self.access_token
        }).encode('utf-8')

        req = urllib.request.Request(container_url, data=data, method='POST')
        try:
            with urllib.request.urlopen(req) as res:
                container_res = json.loads(res.read().decode('utf-8'))
                creation_id = container_res.get('id')
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise RuntimeError(f"Failed to create Threads container: {e.code} - {err_body}")

        if not creation_id:
            raise RuntimeError(f"No creation_id returned: {container_res}")

        # Threads API recommended wait before publish (1-2 seconds)
        time.sleep(2)

        # Step 2: Publish Container
        publish_url = f"{self.base_url}/{self.user_id}/threads_publish"
        publish_data = urllib.parse.urlencode({
            'creation_id': creation_id,
            'access_token': self.access_token
        }).encode('utf-8')

        req_pub = urllib.request.Request(publish_url, data=publish_data, method='POST')
        try:
            with urllib.request.urlopen(req_pub) as res:
                pub_res = json.loads(res.read().decode('utf-8'))
                media_id = pub_res.get('id')
                return {
                    'success': True,
                    'media_id': media_id,
                    'creation_id': creation_id
                }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise RuntimeError(f"Failed to publish Threads container: {e.code} - {err_body}")

    def get_post_insights(self, media_id):
        """
        投稿のインサイト（閲覧数、いいね数、返信数、再投稿数、引用数）を取得
        """
        metrics = 'views,likes,replies,reposts,quotes'
        url = f"{self.base_url}/{media_id}/insights?metric={metrics}&access_token={self.access_token}"
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                insights_data = {
                    'views': 0,
                    'likes': 0,
                    'replies': 0,
                    'reposts': 0,
                    'quotes': 0
                }
                for item in data.get('data', []):
                    name = item.get('name')
                    values = item.get('values', [])
                    if values and len(values) > 0:
                        val = values[0].get('value', 0)
                        if name in insights_data:
                            insights_data[name] = val
                return insights_data
        except urllib.error.HTTPError as e:
            print(f"Warning: Failed to get insights for {media_id}: {e.code}")
            return None

    def refresh_token(self):
        """
        60日間の長期アクセストークンを延長・更新
        """
        url = f"https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={self.access_token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode('utf-8'))
