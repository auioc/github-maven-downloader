import os

from core.utils import die, readJson

if __name__ == "__main__":
    die()

CONFIG_FILE = "config.json"
CONFIG = readJson(CONFIG_FILE)

PROXY = (lambda e:
         (lambda c: c["proxy"] if ("proxy" in c.keys()) else {})(CONFIG)
         if (e is None) else {"http": e, "https": e})(os.getenv("PROXY"))

TOKEN = (lambda e:
         (lambda c: c["token"] if ("token" in c.keys()) else None)(CONFIG)
         if (e is None) else e)(os.getenv("GITHUB_TOKEN"))
if TOKEN is None:
    die("Must provide a GitHub personal access token via config or environment variable 'GITHUB_TOKEN'")
