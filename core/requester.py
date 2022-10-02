import requests
import urllib3
from lxml import etree
from requests.adapters import HTTPAdapter
from requests.sessions import Session

from core.config import PROXY
from core.utils import die, writeBinary

if __name__ == "__main__":
    die()


class HttpRequester(object):
    session: Session

    def __init__(self) -> None:
        urllib3.disable_warnings()
        session = requests.session()
        session.proxies = PROXY
        session.verify = False
        session.mount("https://", HTTPAdapter(max_retries=3))
        self.session = session

    def get(self, url: str):
        r = self.session.get(url)
        r.raise_for_status()
        return r

    def getText(self, url: str):
        return self.get(url).text

    def getJson(self, url: str):
        return self.get(url).json()

    def getJsonPost(self, url: str, data: str):
        r = self.session.post(url, data=data)
        r.raise_for_status()
        return r.json()

    def getXml(self, url: str):
        return etree.fromstring(self.get(url).text)

    def getContent(self, url: str):
        return self.get(url).content

    def downloadFile(self, url: str, file: str):
        writeBinary(file, self.get(url).content)
