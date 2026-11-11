"""Generate crawlable articles, library links, metadata and sitemap (stdlib only)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://chinesewithbaiba.eu/"
articles = json.loads((ROOT / "content/articles/index.json").read_text(encoding="utf-8"))


def metadata(page, url, title, description, kind="website", schema=None):
    page = re.sub(r'\s*<!-- SEO:start -->.*?<!-- SEO:end -->', '', page, flags=re.S)
    page = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', page)
    page = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{html.escape(description, quote=True)}">', page)
    tags = [f'<link rel="canonical" href="{url}">',
            '<meta property="og:site_name" content="Chinese with Baiba">',
            f'<meta property="og:type" content="{kind}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:title" content="{html.escape(title, quote=True)}">',
            f'<meta property="og:description" content="{html.escape(description, quote=True)}">',
            '<meta name="twitter:card" content="summary">']
    if schema:
        tags.append('<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>')
    return page.replace('</head>', '  <!-- SEO:start -->\n  ' + '\n  '.join(tags) + '\n  <!-- SEO:end -->\n</head>')


home = ROOT / "index.html"
home.write_text(metadata(home.read_text(encoding="utf-8"), BASE,
    "Chinese Tutor in Latvia & Free Apps | Chinese with Baiba",
    "Learn with Baiba, a native Chinese tutor in Riga, Latvia. Book lessons in person or online across the EU, and explore four free Chinese learning apps.",
    schema={"@context": "https://schema.org", "@type": "WebSite", "name": "Chinese with Baiba", "url": BASE,
            "publisher": {"@type": "Person", "name": "Baiba", "alternateName": "冰玉", "url": BASE}}), encoding="utf-8")

template = (ROOT / "article.html").read_text(encoding="utf-8")
cards = []
urls = [BASE, BASE + "articles.html"]
for article in sorted(articles, key=lambda a: a["date"], reverse=True):
    slug = article["slug"]
    assert re.fullmatch(r"[a-z0-9-]+", slug), "Invalid article slug"
    relative = f"articles/{slug}.html"
    url = BASE + relative
    urls.append(url)
    body = (ROOT / article["file"]).read_text(encoding="utf-8")
    body = re.sub(r'^<!--.*?-->\s*', '', body, count=1, flags=re.S)
    # Source fragments use paths relative to the site root.
    body = re.sub(r'(href|src)="(?![a-zA-Z]+:|/|#)([^"]+)"', r'\1="../\2"', body)
    title = html.escape(article["title"])
    summary = html.escape(article["summary"])
    tags = ''.join(f'<span class="article-tag">{html.escape(t)}</span>' for t in article["tags"])
    page = template.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    page = page.replace('href="index.html', 'href="../index.html').replace('href="articles.html', 'href="../articles.html')
    page = page.replace('Loading article...', title)
    page = page.replace('id="articleMeta" class="article-meta"></p>', f'id="articleMeta" class="article-meta">{article["date"]}</p>')
    page = page.replace('id="articleTags" class="article-tags"></div>', f'id="articleTags" class="article-tags">{tags}</div>')
    page = page.replace('id="articleBody" class="article-body"></div>', f'id="articleBody" class="article-body">{body}</div>')
    page = re.sub(r'  <script src="../assets/js/(?:article|articles-data).js"></script>\n?', '', page)
    page = metadata(page, url, article["title"] + " | Chinese with Baiba", article["summary"], "article",
        {"@context": "https://schema.org", "@type": "Article", "headline": article["title"],
         "description": article["summary"], "datePublished": article["date"], "mainEntityOfPage": url,
         "author": {"@type": "Person", "name": "Baiba", "url": BASE}})
    (ROOT / "articles").mkdir(exist_ok=True)
    (ROOT / relative).write_text(page, encoding="utf-8")
    cards.append(f'<article class="article-card"><h3>{title}</h3><p class="article-meta">{article["date"]}</p><p>{summary}</p><div class="article-tags">{tags}</div><a class="app-link" href="{relative}">Read Article</a></article>')

library = ROOT / "articles.html"
page = library.read_text(encoding="utf-8")
page = re.sub(r'(<div id="articleList" class="article-list" aria-live="polite">).*?(</div>\s*</section>)',
              lambda m: m[1] + '\n' + '\n'.join(cards) + '\n' + m[2], page, flags=re.S)
page = re.sub(r'  <script src="assets/js/(?:articles|articles-data).js"></script>\n?', '', page)
library.write_text(metadata(page, BASE + "articles.html", "Chinese Study Articles & HSK Guides | Chinese with Baiba",
    "Explore practical Mandarin study guides on pinyin pronunciation, Chinese characters, grammar and HSK preparation from tutor Baiba."), encoding="utf-8")
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    '\n'.join(f'  <url><loc>{html.escape(url)}</loc></url>' for url in urls) + '\n</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n', encoding="utf-8")
print(f"Generated {len(articles)} articles, library, metadata and sitemap.")
