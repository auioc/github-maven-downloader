import json
import os


def die(reason: str = None):
    if not reason is None:
        print(reason)
    exit(1)


if __name__ == "__main__":
    die()


def readText(file: str):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


def writeText(file: str, text: str):
    absFile = os.path.abspath(file)
    absDir = os.path.dirname(absFile)
    if not os.path.exists(absDir):
        os.makedirs(absDir)
    with open(absFile, "w", encoding="utf-8") as f:
        f.write(text)


def readJson(file: str):
    return json.loads(readText(file))


def writeJson(file: str, jsonObj: dict):
    writeText(file, json.dumps(jsonObj, ensure_ascii=False, indent=4))
