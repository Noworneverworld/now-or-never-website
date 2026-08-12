from pathlib import Path
import json, shutil, html

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()

# Copy the visible static site.
for name in ["index.html","creons-votre-voyage.html","conseils-destinations.html","mon-histoire.html","styles.css","script.js"]:
    shutil.copy2(ROOT/name, DIST/name)
shutil.copytree(ROOT/"assets", DIST/"assets")

template = (ROOT/"templates"/"guide.html").read_text(encoding="utf-8")

def esc(v): return html.escape(str(v or ""), quote=True)

for path in sorted((ROOT/"content"/"guides").glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("draft", True):
        continue
    slug = data["slug"]
    out = DIST/"guides"/slug
    out.mkdir(parents=True, exist_ok=True)
    meta = []
    if data.get("duration"): meta.append(f"<span>{esc(data['duration'])}</span>")
    if data.get("budget"): meta.append(f"<span>{esc(data['budget'])}</span>")
    if data.get("travel_period"): meta.append(f"<span>{esc(data['travel_period'])}</span>")
    page = template
    replacements = {
        "{{SEO_TITLE}}": esc(data.get("seo_title") or data["title"] + " | Now or Never"),
        "{{SEO_DESCRIPTION}}": esc(data.get("seo_description") or data.get("excerpt", "")),
        "{{TYPE}}": esc(data.get("type", "Guide")), "{{COUNTRY}}": esc(data.get("country", "")),
        "{{TITLE}}": esc(data["title"]), "{{EXCERPT}}": esc(data.get("excerpt", "")),
        "{{COVER_IMAGE}}": esc(data.get("cover_image", "")), "{{META}}": "".join(meta),
        "{{BODY}}": data.get("body", "")
    }
    for key, value in replacements.items(): page = page.replace(key, value)
    (out/"index.html").write_text(page, encoding="utf-8")

# Basic sitemap for core pages + published guides.
base = "https://noworneverworld.com"
urls = ["/", "/creons-votre-voyage.html", "/conseils-destinations.html", "/mon-histoire.html"]
for path in sorted((ROOT/"content"/"guides").glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("draft", True): urls.append(f"/guides/{data['slug']}/")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{base}{u}</loc></url>\n' for u in urls) + '</urlset>'
(DIST/"sitemap.xml").write_text(sitemap, encoding="utf-8")
(DIST/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://noworneverworld.com/sitemap.xml\n", encoding="utf-8")
print(f"Site construit dans {DIST}")
