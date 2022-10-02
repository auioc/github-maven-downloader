import json
from typing import Any, Dict

from core.config import TOKEN
from core.requester import HttpRequester
from core.utils import die

if __name__ == "__main__":
    die()

API_URL = "https://api.github.com"

REQUESTER = HttpRequester()
REQUESTER.session.headers.update({"Authorization": f"Bearer {TOKEN}"})


def queryGql(query: str, vars: Dict[str, Any]):
    return REQUESTER.getJsonPost(
        f"{API_URL}/graphql",
        json.dumps({"query": query, "variables": vars})
    )


def queryRest(path: str, handler=None):
    j = REQUESTER.getJson(f"{API_URL}{path}")
    return j if (handler is None) else handler(j)
