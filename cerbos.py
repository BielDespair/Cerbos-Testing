import requests
from typing import Dict, List


class CerbosClient:
    def __init__(self, base_url: str = "http://localhost:3592", timeout: float = 2.0):
        self.base_url = base_url.strip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def check(self, principal: Dict, resources: List[Dict]) -> Dict[str, bool]:
        payload = {
            "principal": principal,
            "resources": resources
        }

        r = self.session.post(
            f"{self.base_url}/api/check/resources",
            json=payload,
            timeout=self.timeout
        )

        r.raise_for_status()
        data = r.json()

        return r.json()