from pathlib import Path
import re
import xml.etree.ElementTree as ElementTree
from urllib.parse import unquote


ROOT = Path(__file__).parent
ASSET_VERSION = "20261020-1"
SOCIAL_IMAGE = "https://eduline.kr/og-image.png"

all_pages = [ROOT / "index.html", *ROOT.glob("*/index.html"), *ROOT.glob("*/*/index.html")]
assert (ROOT / "og-image.png").exists(), "Missing social preview image"
for page in all_pages:
    html = page.read_text(encoding="utf-8")
    assert f'<meta property="og:image" content="{SOCIAL_IMAGE}">' in html, f"Missing Open Graph image: {page}"
    assert '<meta property="og:image:width" content="1200">' in html, f"Missing image width: {page}"
    assert '<meta property="og:image:height" content="630">' in html, f"Missing image height: {page}"
    assert '<meta name="twitter:card" content="summary_large_image">' in html, f"Missing Twitter card: {page}"

pages = list(ROOT.glob("*/*/index.html"))
assert len(pages) == 158, f"Expected 158 locality pages, found {len(pages)}"

for page in pages:
    html = page.read_text(encoding="utf-8")
    assert f'../../styles.css?v={ASSET_VERSION}' in html, f"Missing versioned stylesheet: {page}"
    assert '../../script.js' in html, f"Missing script: {page}"
    assert "contact-form" not in html, f"Unexpected contact form: {page}"
    assert '<link rel="canonical"' in html, f"Missing canonical: {page}"
    assert 'type="application/ld+json"' in html, f"Missing structured data: {page}"

parent_link_count = 0
for parent_page in ROOT.glob("*/index.html"):
    html = parent_page.read_text(encoding="utf-8")
    assert f'../styles.css?v={ASSET_VERSION}' in html, f"Missing versioned stylesheet: {parent_page}"
    grids = re.findall(r'class="locality-grid">(.*?)</div>', html, re.S)
    assert len(grids) == 1, f"Expected one locality grid: {parent_page}"
    for href in re.findall(r'href="([^"]+)/"', grids[0]):
        target = parent_page.parent / unquote(href) / "index.html"
        assert target.exists(), f"Broken locality link: {target}"
        parent_link_count += 1

assert parent_link_count == 158, f"Expected 158 parent links, found {parent_link_count}"

sitemap = ElementTree.parse(ROOT / "sitemap.xml")
namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [element.text for element in sitemap.findall(".//s:loc", namespace)]
assert len(urls) == 169, f"Expected 169 sitemap URLs, found {len(urls)}"
assert len(urls) == len(set(urls)), "Duplicate sitemap URL found"

print(f"PASS pages={len(pages)} parent_links={parent_link_count} sitemap_urls={len(urls)}")