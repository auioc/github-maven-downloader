from typing import Dict, List, TypedDict


class File(TypedDict):
    name: str
    sha1: str
    size: int


class Version(TypedDict):
    files: List[File]


class Package(TypedDict):
    owner: str
    name: str
    versions: Dict[str, Version]
