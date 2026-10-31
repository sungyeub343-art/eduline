"""Submit every sitemap URL to Naver via IndexNow. Run after the site is deployed."""
from pathlib import Path
import json
import urllib.request
import xml.etree.ElementTree as ElementTree


ROOT = Path(__file__).parent
HOST = "eduline.kr"
ENDPOINT = "https://searchadvisor.naver.com/indexnow"

key_file = next(path for path in ROOT.glob("*.txt") if path.stem == path.read_text(encoding="utf-8").strip())
key = key_file.stem
namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [element.text for element in ElementTree.parse(ROOT / "sitemap.xml").findall(".//s:loc", namespace)]

payload = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key_file.name}", "urlList": urls}).encode("utf-8")
request = urllib.request.Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
with urllib.request.urlopen(request) as response:
    print(f"IndexNow {response.status}: submitted {len(urls)} URLs")
