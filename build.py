from pathlib import Path
import json, shutil, html, re
ROOT=Path(__file__).parent
DIST=ROOT/'dist'
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
for name in ['index.html','creons-votre-voyage.html','conseils-destinations.html','mon-histoire.html','styles.css','article.css','script.js']:
    shutil.copy2(ROOT/name,DIST/name)
shutil.copytree(ROOT/'assets',DIST/'assets')
template=(ROOT/'templates'/'guide.html').read_text(encoding='utf-8')
def esc(v): return html.escape(str(v or ''),quote=True)
def imgsrc(v):
    v=str(v or '')
    return '../..'+v if v.startswith('/') else '../../'+v.lstrip('./')
def stop_media(stop, index=0):
    imgs=[x for x in [stop.get('image'),stop.get('image_2'),stop.get('image_3')] if x]
    if not imgs:return ''
    variant=f' variant-{(index % 3)+1}'
    if len(imgs)==1:
        return f'<div class="stop-media one{variant}"><img class="main" src="{esc(imgsrc(imgs[0]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async"></div>'
    if len(imgs)==2:
        return (f'<div class="stop-media two{variant}">'
                f'<img class="main" src="{esc(imgsrc(imgs[0]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async">'
                f'<img class="secondary" src="{esc(imgsrc(imgs[1]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async"></div>')
    return (f'<div class="stop-media three{variant}">'
            f'<img class="main" src="{esc(imgsrc(imgs[0]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async">'
            f'<img class="secondary secondary-a" src="{esc(imgsrc(imgs[1]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async">'
            f'<img class="secondary secondary-b" src="{esc(imgsrc(imgs[2]))}" alt="{esc(stop.get("name"))}" loading="lazy" decoding="async"></div>')
def render_stops(stops):
    chunks=[]
    for i,s in enumerate(stops or []):
        tags=''.join(f'<span>{esc(x)}</span>' for x in (s.get('highlights') or []))
        verdict=f'<div class="stop-verdict"><strong>Notre avis</strong>{esc(s.get("verdict"))}</div>' if s.get('verdict') else ''
        reverse=' reverse' if i%2 else ''
        chunks.append(f'<article class="stop-card{reverse}" id="etape-{i+1}">{stop_media(s,i)}<div class="stop-copy"><span class="stop-index">Étape {i+1}</span><h3>{esc(s.get("name"))}</h3><span class="stop-days">{esc(s.get("days"))}</span><div class="article-prose">{s.get("body","")}</div>{verdict}<div class="stop-highlights">{tags}</div></div></article>')
    return ''.join(chunks)
def route_section(stops):
    if not stops:return ''
    items=''.join(f'<div class="route-stop">{esc(s.get("name"))}<small>{esc(s.get("days"))}</small></div>' for s in stops)
    return f'<section class="route-section" id="itineraire"><div class="shell"><p class="section-kicker">Itinéraire</p><h2 class="article-section-title">Le voyage en un coup d’œil.</h2><div class="route-line">{items}</div></div></section>'
def budget_section(d):
    items=d.get('budget_items') or []
    if not items:return ''
    rows=[]
    for it in items:
        try:p=max(0,min(100,float(it.get('percent') or 0)))
        except:p=0
        rows.append(f'<div class="budget-row"><span>{esc(it.get("label"))}</span><div class="budget-track"><div class="budget-fill" style="width:{p}%"></div></div><strong>{esc(it.get("amount"))}</strong></div>')
    return '<section class="budget-section" id="budget"><div class="shell"><div class="budget-head"><div class="budget-total"><small>Notre budget réel</small>'+esc(d.get('budget_total') or d.get('budget'))+'</div><p class="budget-note">'+esc(d.get('budget_note'))+'</p></div><div class="budget-grid"><div class="budget-bars">'+''.join(rows)+'</div><aside class="budget-side"><strong>'+esc(d.get('budget_per_day'))+'</strong><span>par jour et par personne</span></aside></div></div></section>'
def info_cards(d):
    cards=[]
    if d.get('transport_body'):cards.append(f'<section class="info-card" id="transports"><p class="section-kicker">Logistique</p><h2>Se déplacer</h2><div class="article-prose">{d["transport_body"]}</div></section>')
    if d.get('practical_body'):cards.append(f'<section class="info-card" id="pratique"><p class="section-kicker">À savoir</p><h2>Préparer son voyage</h2><div class="article-prose">{d["practical_body"]}</div></section>')
    return ''.join(cards)
def conclusion_section(d):
    if not any([d.get('conclusion_title'),d.get('conclusion_body'),d.get('conclusion_quote')]):return ''
    return '<section class="conclusion-section"><div class="shell conclusion-grid"><div><p class="section-kicker">Ce que le voyage nous a laissé</p><h2 class="article-section-title">'+esc(d.get('conclusion_title') or 'Notre ressenti')+'</h2></div><div><div class="article-prose">'+d.get('conclusion_body','')+'</div><div class="conclusion-quote">'+esc(d.get('conclusion_quote'))+'</div></div></div></section>'

# V13: pages juridiques statiques
for legal_name in ['mentions-legales.html','cgv.html','confidentialite.html']:
    src=ROOT/legal_name
    if src.exists():
        shutil.copy2(src,DIST/legal_name)

guides=[]
testimonials=[]
for path in sorted((ROOT/'content'/'testimonials').glob('*.json')) if (ROOT/'content'/'testimonials').exists() else []:
    try:
        t=json.loads(path.read_text(encoding='utf-8'))
        testimonials.append(t)
    except Exception:
        pass
for path in sorted((ROOT/'content'/'guides').glob('*.json')):
    d=json.loads(path.read_text(encoding='utf-8'));guides.append(d)
    if d.get('draft',True):continue
    out=DIST/'guides'/d['slug'];out.mkdir(parents=True,exist_ok=True)
    meta=[]
    if d.get('duration'):meta.append(f'<span>{esc(d["duration"])}</span>')
    if d.get('budget'):meta.append(f'<span>{esc(d["budget"])}</span>')
    if d.get('travel_period'):meta.append(f'<span>{esc(d["travel_period"])}</span>')
    stops=d.get('stops') or []
    quick=[]
    if stops:quick.append('<a href="#itineraire">Itinéraire</a>')
    if d.get('budget_items'):quick.append('<a href="#budget">Budget</a>')
    if d.get('transport_body'):quick.append('<a href="#transports">Transports</a>')
    if d.get('practical_body'):quick.append('<a href="#pratique">Pratique</a>')
    quicknav='<nav class="article-quicknav"><div class="shell">'+''.join(quick)+'</div></nav>' if quick else ''
    structured=bool(stops or d.get('budget_items') or d.get('intro_body'))
    stops_html=render_stops(stops) if structured else f'<div class="article-prose" style="max-width:840px;margin:auto">{d.get("body","")}</div>'
    rep={'{{SEO_TITLE}}':esc(d.get('seo_title') or d['title']+' | Now or Never'),'{{SLUG}}':esc(d.get('slug','')),'{{SEO_DESCRIPTION}}':esc(d.get('seo_description') or d.get('excerpt','')),'{{TYPE}}':esc(d.get('type','Guide')),'{{COUNTRY}}':esc(d.get('country','')),'{{TITLE}}':esc(d['title']),'{{EXCERPT}}':esc(d.get('excerpt','')),'{{COVER_IMAGE}}':esc(d.get('cover_image','')),'{{META}}':''.join(meta),'{{QUICKNAV}}':quicknav,'{{INTRO_SCRIPT}}':esc(d.get('intro_script','')),'{{INTRO_BODY}}':d.get('intro_body',''),'{{ROUTE_SECTION}}':route_section(stops),'{{STOPS}}':stops_html,'{{BUDGET_SECTION}}':budget_section(d),'{{INFO_CARDS}}':info_cards(d),'{{CONCLUSION_SECTION}}':conclusion_section(d)}
    page=template
    for k,v in rep.items():page=page.replace(k,v)
    (out/'index.html').write_text(page,encoding='utf-8')
page=(DIST/'conseils-destinations.html').read_text(encoding='utf-8')
start='<!-- AUTO-GUIDES-START -->';end='<!-- AUTO-GUIDES-END -->'
def guide_card(d):
    href=f'guides/{esc(d.get("slug"))}/' if not d.get('draft',True) else '#'
    label='Découvrir le guide →' if not d.get('draft',True) else 'Bientôt disponible'
    cls='read' if not d.get('draft',True) else 'read disabled'
    img=(d.get('cover_image') or '/assets/vietnam-ninh-binh.jpg').lstrip('/')
    return f'<article class="country-card"><img src="{esc(img)}" alt="{esc(d.get("country"))}" loading="lazy" decoding="async"><div class="country-card-body"><span class="kicker">{esc(d.get("type","Guide pays"))}</span><h3>{esc(d.get("country"))}</h3><p>{esc(d.get("excerpt",""))}</p><div class="contents"><span>Itinéraire</span><span>Budget</span><span>Étapes</span><span>Conseils</span></div><a class="{cls}" href="{href}">{label}</a></div></article>'
if start in page and end in page:
    page=re.sub(re.escape(start)+r'.*?'+re.escape(end),start+''.join(guide_card(d) for d in guides)+end,page,flags=re.S)
(DIST/'conseils-destinations.html').write_text(page,encoding='utf-8')

# Synchronise les guides publiés et les témoignages avec l'accueil.
home=(DIST/'index.html').read_text(encoding='utf-8')

def home_guide_card(d):
    href=f'guides/{esc(d.get("slug"))}/' if not d.get('draft',True) else '#'
    img=(d.get('cover_image') or '/assets/vietnam-ninh-binh.jpg').lstrip('/')
    label=esc(d.get('country') or d.get('title'))
    title=esc(d.get('title'))
    link='Lire le guide →' if not d.get('draft',True) else 'Bientôt disponible'
    cls='' if not d.get('draft',True) else ' class="soon"'
    return f'<article class="article-card"><img src="{esc(img)}" alt="{label}" loading="lazy" decoding="async"><div><span>{label}</span><h3>{title}</h3><a{cls} href="{href}">{link}</a></div></article>'

published_guides=[d for d in guides if not d.get('draft',True)]
featured_guides=sorted(published_guides,key=lambda d:(not bool(d.get('featured')), d.get('country','')))[:3]
hg_start='<!-- AUTO-HOME-GUIDES-START -->';hg_end='<!-- AUTO-HOME-GUIDES-END -->'
if hg_start in home and hg_end in home:
    home=re.sub(re.escape(hg_start)+r'.*?'+re.escape(hg_end),
                hg_start+''.join(home_guide_card(d) for d in featured_guides)+hg_end,
                home,flags=re.S)

def review_card(t):
    try: stars=max(1,min(5,int(t.get('stars') or 5)))
    except: stars=5
    source='<span class="review-source">Avis Google</span>' if t.get('google') else ''
    who=f'<strong>{esc(t.get("name"))}</strong>' if t.get('name') else ''
    tagline=f'<span class="review-tagline">{esc(t.get("tagline"))}</span>' if t.get('tagline') else ''
    return (f'<article class="review-card"><div class="stars">{"★"*stars}</div>'
            f'<p>“{esc(t.get("text"))}”</p>{who}'
            f'<span>{esc(t.get("destination"))}</span>{tagline}{source}</article>')

live_reviews=[t for t in testimonials if not t.get('draft',True) and t.get('text')]
live_reviews=sorted(live_reviews,key=lambda t:t.get('order') or 999)[:3]
reviews_html=''.join(review_card(t) for t in live_reviews)
rv_start='<!-- AUTO-REVIEWS-START -->';rv_end='<!-- AUTO-REVIEWS-END -->'
if rv_start in home and rv_end in home:
    home=re.sub(re.escape(rv_start)+r'.*?'+re.escape(rv_end),rv_start+reviews_html+rv_end,home,flags=re.S)
    count=len(live_reviews)
    if count==1: home=home.replace('<div class="review-grid">','<div class="review-grid single-review">',1)
    elif count==2: home=home.replace('<div class="review-grid">','<div class="review-grid two-reviews">',1)

(DIST/'index.html').write_text(home,encoding='utf-8')

base='https://noworneverworld.com';urls=['/','/creons-votre-voyage.html','/conseils-destinations.html','/mon-histoire.html']+[f'/guides/{d["slug"]}/' for d in guides if not d.get('draft',True)]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{base}{u}</loc></url>\n' for u in urls)+'</urlset>'
(DIST/'sitemap.xml').write_text(sitemap,encoding='utf-8')
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://noworneverworld.com/sitemap.xml\n',encoding='utf-8')
print('Site construit dans',DIST)
