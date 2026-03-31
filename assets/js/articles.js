async function loadArticleIndex() {
  const candidates = ["content/articles/index.json", "./content/articles/index.json", "/content/articles/index.json"];

  for (const path of candidates) {
    try {
      const response = await fetch(path, { cache: "no-store" });

      if (response.ok) {
        const payload = await response.json();
        if (Array.isArray(payload) && payload.length > 0) {
          return payload;
        }
      }
    } catch (error) {
      // Try the next candidate path.
    }
  }

  if (Array.isArray(window.ARTICLES_INDEX) && window.ARTICLES_INDEX.length > 0) {
    return window.ARTICLES_INDEX;
  }

  throw new Error("Failed to load article index.");
}

function getReadLink(article) {
  return `article.html?slug=${encodeURIComponent(article.slug)}`;
}

async function loadArticles() {
  const listEl = document.getElementById("articleList");

  if (!listEl) {
    return;
  }

  try {
    const articles = await loadArticleIndex();
    const sortedArticles = [...articles].sort((a, b) => b.date.localeCompare(a.date));

    listEl.innerHTML = sortedArticles
      .map((article) => {
        const safeSummary = article.summary || "";
        const tags = Array.isArray(article.tags)
          ? article.tags.map((tag) => `<span class=\"article-tag\">${tag}</span>`).join("")
          : "";

        return `
          <article class="article-card">
            <h3>${article.title}</h3>
            <p class="article-meta">${article.date}</p>
            <p>${safeSummary}</p>
            <div class="article-tags">${tags}</div>
            <a class="app-link" href="${getReadLink(article)}">Read Article</a>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    listEl.innerHTML = `
      <article class="article-card">
        <h3>Articles are not available right now.</h3>
        <p>If you are previewing local files, open the site with a local server or publish to GitHub Pages.</p>
      </article>
    `;
    console.error(error);
  }
}

loadArticles();
