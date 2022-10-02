from typing import List

from lxml import etree

from core.config import TOKEN
from core.requester import HttpRequester
from core.types import Metadata, Package, PackageName
from core.utils import die

if __name__ == "__main__":
    die()

REQUESTER = HttpRequester()
REQUESTER.session.headers.update({"Authorization": f"token {TOKEN}"})

BASE_URL = "https://maven.pkg.github.com"


def getUrl(package: Package):
    name = package["package"].rsplit(".", 1)
    return f"{BASE_URL}/{package['owner']}/{package['repository']}/{name[0]}/{name[1]}"


def getMetadata(package: Package) -> Metadata:
    url = f"{getUrl(package)}/maven-metadata.xml"
    metadata = REQUESTER.getXml(url)
    versions: List[str] = metadata.xpath("/metadata/versioning/versions/version/text()")
    if versions.sort() == list(package["versions"].keys()).sort():
        return {
            "metadata": etree.tostring(metadata),
            "md5": REQUESTER.getText(f"{url}.md5"),
            "sha1": REQUESTER.getText(f"{url}.sha1"),
        }
    else:
        die()


def getFile(package: Package, version: str, file: str):
    if not version in package["versions"].keys():
        die()
    return REQUESTER.getContent(f"{getUrl(package)}/{version}/{file}")
