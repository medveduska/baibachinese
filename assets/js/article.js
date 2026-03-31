function parseFrontmatter(text) {
  const frontmatterMatch = text.match(/^<!--\s*([\s\S]*?)\s*-->/);

  if (!frontmatterMatch) {
    return { metadata: {}, body: text };
  }

  const metadata = {};
  const lines = frontmatterMatch[1].split("\n").map((line) => line.trim()).filter(Boolean);

  for (const line of lines) {
    const separatorIndex = line.indexOf(":");
    if (separatorIndex === -1) {
      continue;
    }

    const key = line.slice(0, separatorIndex).trim();
    const value = line.slice(separatorIndex + 1).trim();
    metadata[key] = value;
  }

  const body = text.slice(frontmatterMatch[0].length).trim();
  return { metadata, body };
}

function getSlugFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("slug");
}

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

async function loadArticleFile(path) {
  const candidates = [path, `./${path}`];

  for (const candidate of candidates) {
    try {
      const response = await fetch(candidate, { cache: "no-store" });
      if (response.ok) {
        return response.text();
      }
    } catch (error) {
      // Try next path.
    }
  }

  throw new Error("Failed to load article file.");
}

async function loadArticle() {
  const titleEl = document.getElementById("articleTitle");
  const metaEl = document.getElementById("articleMeta");
  const tagsEl = document.getElementById("articleTags");
  const bodyEl = document.getElementById("articleBody");

  const slug = getSlugFromUrl();

  if (!slug) {
    titleEl.textContent = "Article not found";
    metaEl.textContent = "No slug was provided in the URL.";
    return;
  }

  try {
    const articles = await loadArticleIndex();
    const articleMeta = articles.find((item) => item.slug === slug);

    if (!articleMeta) {
      titleEl.textContent = "Article not found";
      metaEl.textContent = "The requested article is not in the index.";
      return;
    }

    let parsed;

    try {
      const articleText = await loadArticleFile(articleMeta.file);
      parsed = parseFrontmatter(articleText);
    } catch (error) {
      if (typeof articleMeta.content === "string" && articleMeta.content.trim()) {
        parsed = { metadata: {}, body: articleMeta.content.trim() };
      } else {
        throw error;
      }
    }

    const title = parsed.metadata.title || articleMeta.title;
    const date = parsed.metadata.date || articleMeta.date;
    const tags = parsed.metadata.tags
      ? parsed.metadata.tags.split(",").map((tag) => tag.trim()).filter(Boolean)
      : Array.isArray(articleMeta.tags)
        ? articleMeta.tags
        : [];

    document.title = `${title} | Chinese with Baiba`;
    titleEl.textContent = title;
    metaEl.textContent = date;
    tagsEl.innerHTML = tags.map((tag) => `<span class=\"article-tag\">${tag}</span>`).join("");
    bodyEl.innerHTML = parsed.body;
  } catch (error) {
    titleEl.textContent = "Article unavailable";
    metaEl.textContent = "Please try again after refreshing the page.";
    bodyEl.innerHTML = "";
    console.error(error);
  }
}

loadArticle();
