from typing import Dict, List, TypedDict


class File(TypedDict):
    name: str
    sha1: str
    size: int


class Version(TypedDict):
    files: List[File]


class Package(TypedDict):
    owner: str
    package: str
    repository: str
    versions: Dict[str, Version]


class PackageName(TypedDict):
    groupId: str
    artifactId: str


class Metadata(TypedDict):
    metadata: str
    md5: str
    sha1: str
