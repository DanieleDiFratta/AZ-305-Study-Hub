"""Print selected cached evidence for editorial review, never fetch or publish bodies."""
import json
import re
import sys
from inspect_source import Page, ROOT
from research import get_page, clean

rows = json.loads((ROOT / 'data/resources.json').read_text(encoding='utf-8'))
pattern = re.compile(r'Azure Cache for Redis|Azure AD B2C|Azure Active Directory B2C|Azure Data Studio|Log Analytics agent|Microsoft Monitoring Agent|Azure Blueprints|Basic Load Balancer|default outbound', re.I)
for row in rows:
    if sys.argv[1:] and row['id'] not in sys.argv[1:]:
        continue
    if not sys.argv[1:] and row['kind'] != 'learn_unit':
        continue
    html, _ = get_page(row['url'])
    main = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S)
    page = Page()
    page.feed(main[1] if main else html)
    text = clean(' '.join(page.text))
    matches = list(pattern.finditer(text))
    if sys.argv[1:]:
        print(row['id'], row['title'], '\n', text[:1600], '\n')
    elif matches:
        print(row['id'], ' | '.join(text[max(0,m.start()-90):m.end()+160] for m in matches[:3]))
