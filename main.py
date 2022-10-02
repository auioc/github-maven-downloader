import os
import sys

from core.config import CONFIG
from tools.downloader import Downloader
from tools.indexer import FileIndexer

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

if __name__ == "__main__":
    if "package" in CONFIG.keys():
        owner = CONFIG["package"]["owner"]
        packageName = CONFIG["package"]["name"]
    else:
        owner = sys.argv[1]
        packageName = sys.argv[2]

    indexer = FileIndexer(owner, packageName)
    indexer.queryAll()
    downloader = Downloader(indexer.toPackage())
    downloader.downloadAll()
