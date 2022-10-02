import json
from typing import Any, Callable, Dict, List

import core.api as API
from core.types import Package, Version
from core.utils import readText, writeText

_GQL_FILE_COUNT = readText("graphql/file-count.gql")
_GQL_FILES = readText("graphql/files.gql")


def _queryGql(query: str, vars: Dict[str, Any], handler: Callable):
    return handler(API.queryGql(query, vars)["data"])


class FileIndexer(object):
    owner: str
    package: str
    repository: str
    versions: Dict[str, Version]

    def __init__(self, owner: str, package: str) -> None:
        self.owner = owner
        self.package = package

    def queryRepository(self) -> str:
        repo = API.queryRest(
            f"/users/{self.owner}/packages/maven/{self.package}",
            lambda data: data["repository"]["name"]
        )
        self.repository = repo
        return repo

    def queryVersions(self) -> List[str]:
        print(f"Querying version in package '{self.owner}:{self.package}'")
        versions = API.queryRest(
            f"/users/{self.owner}/packages/maven/{self.package}/versions",
            lambda data: [i["name"] for i in data]
        )
        self.versions = {}
        for version in versions:
            self.versions[version] = {}
        return versions

    def queryFiles(self) -> Dict[str, Version]:
        if not self.versions:
            self.queryVersions()

        vars = {"login": self.owner, "names": self.package}
        versionCount = len(self.versions)
        for i, version in enumerate(self.versions.keys()):
            print(f"[{i+1}/{versionCount}] Querying files in version '{version}'")
            fileCount = _queryGql(
                _GQL_FILE_COUNT, vars | {"version": version},
                lambda data: data["organization"]["packages"]["nodes"][0]["version"]["files"]["totalCount"]
            )
            files = _queryGql(
                _GQL_FILES, vars | {"version": version, "first": fileCount},
                lambda data: [i for i in data["organization"]["packages"]["nodes"][0]["version"]["files"]["nodes"]]
            )
            self.versions[version]["files"] = files
        return self.versions

    def queryAll(self) -> None:
        self.queryRepository()
        self.queryVersions()
        self.queryFiles()

    def toPackage(self) -> Package:
        return {
            "owner": self.owner,
            "package": self.package,
            "repository": self.repository,
            "version": self.versions
        }

    def toJson(self) -> str:
        return json.dumps(self.toPackage(), ensure_ascii=False, indent=4)

    def store(self) -> str:
        return writeText(f"data/{self.owner}/{self.package}.json", self.toJson())

    def __str__(self) -> str:
        return self.toJson()
