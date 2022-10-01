import json
from typing import Any, Dict

import requests
import urllib3
from requests.adapters import HTTPAdapter

from core.config import PROXY, TOKEN
from core.utils import die

if __name__ == "__main__":
    die()

urllib3.disable_warnings()
SESSION = requests.session()
SESSION.proxies = PROXY
SESSION.headers.update({"Authorization": f"Bearer {TOKEN}"})
SESSION.verify = False
SESSION.mount("https://", HTTPAdapter(max_retries=3,))

API_URL = "https://api.github.com"


def get(path: str):
    r = SESSION.get(f"{API_URL}{path}")
    r.raise_for_status()
    return json.loads(r.text)


def post(path: str, data: str):
    r = SESSION.post(f"{API_URL}{path}", data=data)
    r.raise_for_status()
    return json.loads(r.text)


def queryGql(query: str, vars: Dict[str, Any]):
    return post("/graphql", json.dumps({"query": query, "variables": vars}))


def queryRest(path: str, handler=None):
    j = get(path)
    return j if (handler is None) else handler(j)
