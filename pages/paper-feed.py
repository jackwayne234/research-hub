#!/usr/bin/env python3
"""
Daily Research Feed Scanner
Scans arXiv, Zenodo, Semantic Scholar, and science news RSS feeds
for papers/news matching CJ's research interests.
Outputs feed-data.json for the research hub.
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import re
import time

FEED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "feed-data.json")

# Search queries grouped by topic
TOPICS = {
    "Benford's Law": [
        "Benford's Law physics",
        "Benford's Law gravitational",
        "first digit law astrophysics",
    ],
    "General Relativity & Black Holes": [
        "modified Schwarzschild metric",
        "emergent gravity entropy",
        "black hole information paradox resolution",
        "emergent spacetime thermodynamics",
    ],
    "Primes & Physics": [
        "prime numbers physics",
        "Riemann zeta function gravity",
        "number theory quantum gravity",
        "Euler product physics",
        "zeta function Schwarzschild metric",
        "complete monotonicity gravity",
        "Dirichlet series spacetime",
    ],
    "Optical Computing": [
        "optical computing ternary",
        "wavelength division computing",
        "photonic neural network",
        "optical logic gates",
    ],
    "Quantum Gravity": [
        "causal set quantum gravity",
        "emergent dimensions quantum gravity",
        "discrete spacetime",
        "entropic gravity",
        "holographic principle number theory",
    ],
    "Dark Energy & Cosmology": [
        "dark energy emergent",
        "dark matter alternative theory",
        "cosmological constant problem",
    ],
}

# RSS news feeds
NEWS_FEEDS = [
    ("Quanta Magazine", "https://api.quantamagazine.org/feed/"),
    ("Phys.org - Physics", "https://phys.org/rss-feed/physics-news/"),
    ("ScienceDaily - Physics", "https://www.sciencedaily.com/rss/matter_energy.xml"),
]

NEWS_KEYWORDS = [
    "black hole", "gravity", "spacetime", "quantum gravity", "dark energy",
    "dark matter", "optical comput", "photonic", "prime number", "riemann",
    "benford", "entropy", "hawking", "gravitational wave",
    "cosmolog", "general relativity", "neutron star", "wormhole",
    "ternary", "optical chip", "emergent", "holograph",
]

def fetch_url(url, timeout=15):
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchFeedBot/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None


def search_arxiv(queries, max_per_query=5, days_back=7):
    """Search arXiv API for recent papers."""
    results = []
    seen_ids = set()
    cutoff = datetime.utcnow() - timedelta(days=days_back)

    for query in queries:
        encoded = urllib.parse.quote(query)
        url = (
            f"http://export.arxiv.org/api/query?search_query=all:{encoded}"
            f"&sortBy=submittedDate&sortOrder=descending&max_results={max_per_query}"
        )
        xml_data = fetch_url(url)
        if not xml_data:
            continue

        try:
            root = ET.fromstring(xml_data)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                arxiv_id = entry.find("atom:id", ns).text.strip()
                if arxiv_id in seen_ids:
                    continue
                seen_ids.add(arxiv_id)

                published = entry.find("atom:published", ns).text[:10]
                pub_date = datetime.strptime(published, "%Y-%m-%d")
                if pub_date < cutoff:
                    continue

                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                title = re.sub(r"\s+", " ", title)
                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                summary = re.sub(r"\s+", " ", summary)
                if len(summary) > 300:
                    summary = summary[:297] + "..."

                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
                author_str = ", ".join(authors[:3])
                if len(authors) > 3:
                    author_str += f" +{len(authors)-3} more"

                link = arxiv_id
                for l in entry.findall("atom:link", ns):
                    if l.get("type") == "text/html":
                        link = l.get("href")
                        break

                results.append({
                    "source": "arXiv",
                    "title": title,
                    "authors": author_str,
                    "date": published,
                    "abstract": summary,
                    "url": link,
                    "query": query,
                })
        except Exception as e:
            print(f"  [WARN] arXiv parse error for '{query}': {e}")

        time.sleep(1)  # Be nice to arXiv

    return results


def search_zenodo(queries, max_per_query=3, days_back=30):
    """Search Zenodo API for recent papers."""
    results = []
    seen_ids = set()
    cutoff = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    for query in queries:
        encoded = urllib.parse.quote(query)
        url = (
            f"https://zenodo.org/api/records?q={encoded}"
            f"&sort=mostrecent&size={max_per_query}&type=publication"
        )
        data = fetch_url(url)
        if not data:
            continue

        try:
            resp = json.loads(data)
            for hit in resp.get("hits", {}).get("hits", []):
                rec_id = str(hit.get("id", ""))
                if rec_id in seen_ids:
                    continue
                seen_ids.add(rec_id)

                meta = hit.get("metadata", {})
                pub_date = meta.get("publication_date", "")
                if pub_date < cutoff:
                    continue

                title = meta.get("title", "Untitled")
                desc = meta.get("description", "")
                # Strip HTML tags
                desc = re.sub(r"<[^>]+>", "", desc)
                if len(desc) > 300:
                    desc = desc[:297] + "..."

                creators = meta.get("creators", [])
                author_str = ", ".join(c.get("name", "") for c in creators[:3])
                if len(creators) > 3:
                    author_str += f" +{len(creators)-3} more"

                link = hit.get("links", {}).get("html", f"https://zenodo.org/records/{rec_id}")

                results.append({
                    "source": "Zenodo",
                    "title": title,
                    "authors": author_str,
                    "date": pub_date,
                    "abstract": desc,
                    "url": link,
                    "query": query,
                })
        except Exception as e:
            print(f"  [WARN] Zenodo parse error for '{query}': {e}")

        time.sleep(0.5)

    return results


def search_semantic_scholar(queries, max_per_query=5, days_back=7):
    """Search Semantic Scholar API."""
    results = []
    seen_ids = set()
    cutoff = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    for query in queries:
        encoded = urllib.parse.quote(query)
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={encoded}&limit={max_per_query}"
            f"&fields=title,authors,abstract,url,publicationDate,externalIds"
            f"&sort=publicationDate:desc"
        )
        data = fetch_url(url)
        if not data:
            continue

        try:
            resp = json.loads(data)
            for paper in resp.get("data", []):
                pid = paper.get("paperId", "")
                if pid in seen_ids:
                    continue
                seen_ids.add(pid)

                pub_date = paper.get("publicationDate") or ""
                if pub_date and pub_date < cutoff:
                    continue

                title = paper.get("title", "Untitled")
                abstract = paper.get("abstract") or ""
                if len(abstract) > 300:
                    abstract = abstract[:297] + "..."

                authors = paper.get("authors", [])
                author_str = ", ".join(a.get("name", "") for a in authors[:3])
                if len(authors) > 3:
                    author_str += f" +{len(authors)-3} more"

                link = paper.get("url") or f"https://www.semanticscholar.org/paper/{pid}"

                results.append({
                    "source": "Semantic Scholar",
                    "title": title,
                    "authors": author_str,
                    "date": pub_date or "Unknown",
                    "abstract": abstract,
                    "url": link,
                    "query": query,
                })
        except Exception as e:
            print(f"  [WARN] S2 parse error for '{query}': {e}")

        time.sleep(1)  # Rate limit: 1 req/sec for unauthenticated

    return results


def fetch_news(feeds, keywords):
    """Fetch science news from RSS feeds and filter by keywords."""
    results = []
    cutoff = datetime.utcnow() - timedelta(days=3)

    for feed_name, feed_url in feeds:
        xml_data = fetch_url(feed_url)
        if not xml_data:
            continue

        try:
            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            for item in items[:20]:  # Check first 20 items
                title_el = item.find("title")
                desc_el = item.find("description")
                link_el = item.find("link")
                pub_el = item.find("pubDate")

                title = title_el.text if title_el is not None and title_el.text else ""
                desc = desc_el.text if desc_el is not None and desc_el.text else ""
                link = link_el.text if link_el is not None and link_el.text else ""

                # Strip HTML
                desc = re.sub(r"<[^>]+>", "", desc)
                if len(desc) > 300:
                    desc = desc[:297] + "..."

                # Check keywords
                text_lower = (title + " " + desc).lower()
                matched = any(kw.lower() in text_lower for kw in keywords)
                if not matched:
                    continue

                # Parse date loosely
                date_str = ""
                if pub_el is not None and pub_el.text:
                    try:
                        # RFC 822 date
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(pub_el.text)
                        if dt.replace(tzinfo=None) < cutoff:
                            continue
                        date_str = dt.strftime("%Y-%m-%d")
                    except:
                        date_str = pub_el.text[:10]

                results.append({
                    "source": feed_name,
                    "title": title.strip(),
                    "date": date_str,
                    "abstract": desc.strip(),
                    "url": link.strip(),
                    "type": "news",
                })
        except Exception as e:
            print(f"  [WARN] RSS parse error for {feed_name}: {e}")

    return results


def main():
    print(f"🔍 Research Feed Scanner — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    all_papers = []
    all_news = []

    # Collect all queries
    all_queries = []
    for topic, queries in TOPICS.items():
        all_queries.extend(queries)

    # Search each source
    print("\n📚 Searching arXiv...")
    all_papers.extend(search_arxiv(all_queries, max_per_query=3, days_back=7))
    print(f"   Found {len(all_papers)} papers")

    print("\n📚 Searching Zenodo...")
    zenodo = search_zenodo(all_queries, max_per_query=3, days_back=30)
    all_papers.extend(zenodo)
    print(f"   Found {len(zenodo)} papers")

    print("\n📚 Searching Semantic Scholar...")
    s2 = search_semantic_scholar(all_queries, max_per_query=3, days_back=7)
    all_papers.extend(s2)
    print(f"   Found {len(s2)} papers")

    print("\n📰 Fetching science news...")
    all_news = fetch_news(NEWS_FEEDS, NEWS_KEYWORDS)
    print(f"   Found {len(all_news)} articles")

    # Deduplicate by title similarity
    seen_titles = set()
    deduped_papers = []
    for p in all_papers:
        title_key = re.sub(r"[^a-z0-9]", "", p["title"].lower())[:60]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            deduped_papers.append(p)

    # Tag papers with topics
    for paper in deduped_papers:
        query = paper.get("query", "")
        for topic, queries in TOPICS.items():
            if query in queries:
                paper["topic"] = topic
                break
        paper.pop("query", None)

    # Sort by date (newest first)
    deduped_papers.sort(key=lambda x: x.get("date", ""), reverse=True)
    all_news.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Build feed data
    feed = {
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "papers": deduped_papers[:50],  # Cap at 50
        "news": all_news[:20],  # Cap at 20
        "stats": {
            "total_papers": len(deduped_papers),
            "total_news": len(all_news),
            "sources": {
                "arXiv": sum(1 for p in deduped_papers if p["source"] == "arXiv"),
                "Zenodo": sum(1 for p in deduped_papers if p["source"] == "Zenodo"),
                "Semantic Scholar": sum(1 for p in deduped_papers if p["source"] == "Semantic Scholar"),
            },
        },
    }

    with open(FEED_PATH, "w") as f:
        json.dump(feed, f, indent=2)

    print(f"\n✅ Feed saved: {len(deduped_papers)} papers, {len(all_news)} news items")
    print(f"   → {FEED_PATH}")


if __name__ == "__main__":
    main()
