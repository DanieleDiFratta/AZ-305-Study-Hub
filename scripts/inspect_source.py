"""Inspect public Microsoft metadata; downloaded HTML stays in ignored .cache/."""
import hashlib
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.meta_all = {}
        self.links = []
        self.headings = []
        self.text = []
        self._a = None
        self._h = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self._skip += 1
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('name', a.get('property', ''))
            self.meta[key] = a.get('content', '')
            self.meta_all.setdefault(key, []).append(a.get('content', ''))
        if tag == 'a' and a.get('href'):
            self._a = [a['href'], '']
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self._h = [tag, a.get('id', ''), '']

    def handle_data(self, data):
        if self._skip:
            return
        self.text.append(data)
        if self._a is not None:
            self._a[1] += data
        if self._h is not None:
            self._h[2] += data

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._skip = max(0, self._skip - 1)
        if tag == 'a' and self._a is not None:
            self.links.append(self._a)
            self._a = None
        if tag in ('h1', 'h2', 'h3', 'h4') and self._h is not None:
            self.headings.append(self._h)
            self._h = None


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'AZ305-Study-Hub research/1.0'})
    with urllib.request.urlopen(request, timeout=35) as response:
        raw = response.read()
        final = response.url
        status = response.status
    page = Page()
    html = raw.decode('utf-8')
    page.feed(html)
    cache = ROOT / '.cache' / 'inspection'
    cache.mkdir(parents=True, exist_ok=True)
    cache_file = cache / (hashlib.sha256(url.encode()).hexdigest() + '.html')
    cache_file.write_text(html, encoding='utf-8')
    return page, html, final, status


if __name__ == '__main__':
    for url in sys.argv[1:]:
        p, html, final, status = fetch(url)
        print(json.dumps({'url': final, 'http': status, 'meta': p.meta,
                          'headings': p.headings,
                          'training_links': [[urljoin(final, u), re.sub(r'\s+', ' ', t).strip()]
                                             for u, t in p.links if '/training/' in urljoin(final, u)],
                          'embedded_paths': sorted(set(re.findall(r'[\w/-]*training/paths/[\w/-]+', html)))}, ensure_ascii=True))
