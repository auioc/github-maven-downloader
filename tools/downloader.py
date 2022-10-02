import os

from core.maven import getFile, getMetadata
from core.types import Package
from core.utils import writeBinary, writeText


class Downloader(object):
    package: Package
    path: str

    def __init__(self, package: Package) -> None:
        self.package = package
        self.path = f"maven/{'/'.join([n for n in self.package['package'].split('.')])}/"

    def downloadMetadata(self):
        print(f"Downloading metadata of package '{self.package['owner']}:{self.package['package']}'")
        metadata = getMetadata(self.package)
        file = os.path.join(self.path, "maven-metadata.xml")
        writeBinary(file, metadata["metadata"])
        writeText(f"{file}.md5", metadata["md5"])
        writeText(f"{file}.sha1", metadata["sha1"])

    def downloadVersions(self):
        c1 = len(self.package["versions"].keys())
        for i1, version in enumerate(self.package["versions"].items()):
            p1 = f"[{i1+1}/{c1}]"
            print(f"{p1} Downloading files of version '{version[0]}'")
            path = os.path.join(self.path, version[0])
            c2 = len(version[1]["files"])
            for i2, file in enumerate(version[1]["files"]):
                print(f"{p1}[{i2+1}/{c2}] Downloading file '{file['name']}'")
                writeBinary(os.path.join(path, file['name']), getFile(self.package, version[0], file['name']))

    def downloadAll(self):
        self.downloadMetadata()
        self.downloadVersions()
