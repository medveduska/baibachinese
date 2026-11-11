# Chinese with Baiba

Simple static website for Chinese language students to learn basic information about tutor Baiba (冰玉).

## Stack

- HTML
- CSS
- JavaScript

## Domain

- Production domain: `chinesewithbaiba.eu`
- Hosting: GitHub Pages

## App Links

- Vocabulary Cards: https://wordcards.chinesewithbaiba.eu/
- Chinese Grammar Studio: https://grammar.chinesewithbaiba.eu/
- Pinyin Wheel (Little Pinyin · Spin & Say): https://pinyinwheel.chinesewithbaiba.eu/
- Reading Studio: https://reading.chinesewithbaiba.eu/
- Future tools can be published as subdomains of `chinesewithbaiba.eu`

## Article CMS (Manual, File-Based)

This project includes a simple content management flow that works on GitHub Pages without a backend.

### Structure

- `index.html` - homepage
- `articles.html` - article list page
- `article.html` - article detail page that loads an article by slug
- `assets/css/styles.css` - shared styles
- `assets/js/main.js` - shared base scripts
- `assets/js/articles.js` - article library rendering
- `assets/js/article.js` - single article rendering
- `assets/js/articles-data.js` - fallback article data for local preview mode
- `content/articles/index.json` - article registry used by the article library page
- `content/articles/*.html` - full article content files

### Add a New Article

1. Create a new file in `content/articles/`, for example: `content/articles/hsk-speaking-tips.html`.
2. Add metadata in an HTML comment at the top of the file:

```html
<!--
title: HSK Speaking Tips
date: 2026-04-10
summary: Practical speaking strategies for early HSK levels.
tags: HSK,Speaking,Practice
-->
```

3. Write the article body using regular HTML (`<h2>`, `<p>`, `<ul>`, etc.).
4. Add an entry in `content/articles/index.json` with matching `slug`, `title`, `date`, `summary`, `tags`, and `file`.
5. Run `py scripts/build-seo.py` to regenerate the complete article pages, article library, metadata, and sitemap.
6. Commit and push. The GitHub Pages workflow also runs the generator before publishing.

### Notes

- Use date format `YYYY-MM-DD` for clean sorting.
- Keep `slug` lowercase with hyphens.
- The article library automatically sorts by newest date first.
- Published articles live at `articles/<slug>.html` with their full content available without JavaScript. Existing `article.html?slug=...` links remain supported and point search engines to the static canonical page.

## Google Search

The site includes unique titles and descriptions, canonical URLs, Open Graph metadata, WebSite/Article structured data, a robots file, and a sitemap. Run `py scripts/build-seo.py` after changing article metadata or templates. Edit article source fragments, rather than generated pages.

After deploying, verify the domain in Google Search Console and submit `https://chinesewithbaiba.eu/sitemap.xml`. Use URL Inspection to check the homepage and an article. Indexing, search rankings, and Core Web Vitals are not established by these code changes; review Search Console and PageSpeed Insights for live results.

## Local Run

Open `index.html` in a browser.

## GitHub Pages Setup

1. Push this project to a GitHub repository.
2. In repository settings, enable GitHub Pages from the main branch.
3. Ensure the `CNAME` file contains `chinesewithbaiba.eu`.
4. Configure DNS records at your domain registrar to point to GitHub Pages.
