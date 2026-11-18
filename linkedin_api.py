import json
import urllib.request
import urllib.error
from threads_api import load_env


class LinkedInAPI:
    def __init__(self, access_token=None, person_urn=None):
        env = load_env()
        self.access_token = (access_token or env.get('LINKEDIN_ACCESS_TOKEN', '')).strip()
        self.person_urn = (person_urn or env.get('LINKEDIN_PERSON_URN', '')).strip()
        self.api_version = '202401'

    def is_configured(self):
        return bool(self.access_token)

    def get_person_urn(self):
        if self.person_urn:
            return self.person_urn

        # Try OpenID Connect /v2/userinfo first (Standard for modern LinkedIn OAuth)
        req = urllib.request.Request(
            'https://api.linkedin.com/v2/userinfo',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                sub = data.get('sub')
                if sub:
                    self.person_urn = f"urn:li:person:{sub}"
                    return self.person_urn
        except urllib.error.HTTPError:
            pass

        # Fallback to /v2/me
        req2 = urllib.request.Request(
            'https://api.linkedin.com/v2/me',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        try:
            with urllib.request.urlopen(req2) as res:
                data = json.loads(res.read().decode('utf-8'))
                uid = data.get('id')
                if uid:
                    self.person_urn = f"urn:li:person:{uid}"
                    return self.person_urn
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise RuntimeError(f"Failed to get LinkedIn profile URN: {e.code} - {err_body}")

        raise RuntimeError("Could not determine LinkedIn Person URN.")

    def publish_text_post(self, text):
        """
        LinkedIn REST Posts API (/rest/posts) を使ってテキスト投稿を公開
        """
        if not self.is_configured():
            raise RuntimeError("LINKEDIN_ACCESS_TOKEN is not configured.")

        author_urn = self.get_person_urn()

        url = 'https://api.linkedin.com/rest/posts'
        payload = {
            "author": author_urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        data = json.dumps(payload).encode('utf-8')
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'LinkedIn-Version': self.api_version
        }

        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as res:
                post_id = res.headers.get('x-restli-id', 'published')
                return {'post_id': post_id, 'status': res.status}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise RuntimeError(f"Failed to publish to LinkedIn: {e.code} - {err_body}")
