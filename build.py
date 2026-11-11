#!/usr/bin/env python3
"""Builds the JQ Plumbing static site into ./dist.
Facts live in B below, areas and reviews in data.py, service copy in services.py.
Run: python3 build.py
"""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import AREAS, REVIEWS
from services import SERVICES

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

# GA4 measurement ID lives in one place: JQ_CONFIG.GA4_ID in dist/js/site.js
import re as _re
_m = _re.search(r'GA4_ID:\s*"([^"]*)"', open(os.path.join(DIST, "js", "site.js")).read())
GA4_ID = _m.group(1) if _m else ""
_a = _re.search(r'ADS_ID:\s*"([^"]*)"', open(os.path.join(DIST, "js", "site.js")).read())
ADS_ID = _a.group(1) if _a else ""

def gtag_head():
    if not GA4_ID:
        return ""
    return (f'<!-- Google tag (gtag.js) -->\n'
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
            f'<script>window.JQ_GTAG_IN_HEAD=true;window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
            f'gtag("js",new Date());gtag("config","{GA4_ID}");' + (f'gtag("config","{ADS_ID}");' if ADS_ID else '') + '</script>\n')

B = {
    "name": "JQ Plumbing LLC",
    "short": "JQ Plumbing",
    "owner": "Jonathan Quintanilla",
    "phone_display": "210-793-6046",
    "phone_tel": "+12107936046",
    "license": "RMP-47009",
    "board_url": "https://www.tsbpe.texas.gov",
    "email": "Jonq@jqplumbingllc.com",
    "url": "https://jqplumbingllc.com",
    "hours": "Monday to Friday, 9am to 5pm",
    "weekends": "Weekends are for scheduled and emergency work.",
    "years": "10",
    "maps": "https://share.google/plbjmm6l2AgL8kuZH",
    "reviews_all": "https://search.google.com/local/reviews?placeid=ChIJOymPdtwjWwgRBy5KUhyCero",
    "review_write": "https://g.page/r/CQcuSlIcgnq6EBM/review",
    "facebook": "https://www.facebook.com/61573244019779/",
}

ICON = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "badge": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5zm-1.2 14.2-3.5-3.5 1.4-1.4 2.1 2.1 4.9-4.9 1.4 1.4z"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.4 11.6 12.4 2.6A2 2 0 0 0 11 2H4a2 2 0 0 0-2 2v7c0 .55.22 1.05.59 1.41l9 9a2 2 0 0 0 2.82 0l7-7a2 2 0 0 0 0-2.82zM6.5 8A1.5 1.5 0 1 1 8 6.5 1.5 1.5 0 0 1 6.5 8z"/></svg>',
    "home": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 12h3v8h5v-6h4v6h5v-8h3z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 10.4 3.5 2.1-.8 1.3L11 13V7h2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 14.5 9 2.5 2.5 0 0 1 12 11.5z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.4 8.6 12 13.2l4.6-4.6L18 10l-6 6-6-6z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 5.3 19.9 12l-6.7 6.7-1.4-1.4 4.3-4.3H4v-2h12.1l-4.3-4.3z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6.4 5 5.6 5.6L17.6 5 19 6.4 13.4 12l5.6 5.6-1.4 1.4-5.6-5.6L6.4 19 5 17.6l5.6-5.6L5 6.4z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4.6 7H4v.6l8 5.6 8-5.6V7h-.6z"/></svg>',
}

def esc(s):
    return html.escape(s, quote=True)

def svc_path(s):
    return "/" + s["slug"] + "/"

def tel(loc, cls="", inner=None):
    inner = inner or B["phone_display"]
    return f'<a class="{cls}" href="tel:{B["phone_tel"]}" data-call-location="{loc}">{inner}</a>'

def pic(name, alt, sizes="(min-width: 960px) 50vw, 100vw", cls="", eager=False, w=1200, h=1600):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/img/{name}-640.webp" '
            f'srcset="/img/{name}-640.webp 640w, /img/{name}-1200.webp 1200w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {load}>')

def review_by(name):
    return next(r for r in REVIEWS if r["name"] == name)

# ---------------------------------------------------------------- header with services dropdown
NAV = [("/about/", "About"), ("/reviews/", "Reviews"), ("/service-areas/", "Service areas"), ("/contact/", "Contact")]

def board_notice(cls):
    return (f'<div class="{cls}"><span>Texas State Board of Plumbing Examiners</span>'
            f'<span>7915 Cameron Rd. Austin, TX 78754</span>'
            f'<span><a href="tel:+15129365200" data-no-track>512-936-5200</a></span>'
            f'<span><a href="{B["board_url"]}" target="_blank" rel="noopener noreferrer">www.tsbpe.texas.gov</a></span></div>')

def header(active):
    svc_active = active == "services" or active.startswith("svc:")
    items = "".join(
        f'<li><a href="{svc_path(s)}"{" aria-current=page" if active == "svc:" + s["slug"] else ""}>'
        f'<strong>{s["name"]}</strong><span>{s["short"]}</span></a></li>' for s in SERVICES)
    links = "".join(f'<li><a class="nav-link" href="{h}"{" aria-current=page" if active == h else ""}>{t}</a></li>' for h, t in NAV)
    mobile_svcs = "".join(f'<li><a href="{svc_path(s)}">{s["name"]}</a></li>' for s in SERVICES)
    mobile_links = "".join(f'<li><a class="m-link" href="{h}">{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<aside class="board-strip" aria-label="Texas State Board of Plumbing Examiners"><div class="wrap">{board_notice("board-in")}</div></aside>
<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="/" aria-label="{B["name"]} home">
      <img src="/img/logo-120.webp" width="130" height="120" alt="{B["short"]} logo, license {B["license"]}">
      <span class="brand-txt"><strong>{B["short"]}</strong><span>Lic. {B["license"]}</span></span>
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav-list">
        <li class="has-menu">
          <button class="nav-link menu-btn{" is-active" if svc_active else ""}" type="button" aria-expanded="false" aria-controls="svc-menu">Services {ICON["chev"]}</button>
          <div class="mega" id="svc-menu">
            <div class="mega-in">
              <ul class="mega-list">{items}</ul>
              <div class="mega-foot">
                <a class="mega-all" href="/services/">See all services {ICON["arrow"]}</a>
                <span>Free estimates within city limits</span>
              </div>
            </div>
          </div>
        </li>
        {links}
      </ul>
    </nav>
    {tel("header", "btn btn-call topcall", ICON["phone"] + '<span class="topcall-label">Call </span><span>' + B["phone_display"] + '</span>')}
    <button class="burger" type="button" aria-expanded="false" aria-controls="m-menu" aria-label="Open menu"><span class="i-menu">{ICON["menu"]}</span><span class="i-close">{ICON["close"]}</span></button>
  </div>
  <div class="m-menu" id="m-menu" hidden>
    <div class="wrap">
      <details class="m-svcs"{" open" if svc_active else ""}>
        <summary>Services {ICON["chev"]}</summary>
        <ul>{mobile_svcs}<li><a class="m-all" href="/services/">See all services</a></li></ul>
      </details>
      <ul class="m-list">{mobile_links}</ul>
      {tel("mobile_menu", "btn btn-call btn-block btn-lg", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
      <p class="m-hours">Open {B["hours"]}</p>
    </div>
  </div>
</header>'''

def facts_strip():
    items = [
        (ICON["badge"], f"Texas license {B['license']}", "Licensed and insured plumbers"),
        (ICON["tag"], "Free estimates", "Within San Antonio city limits"),
        (ICON["home"], "Family owned and local", "Fingerprint background checked"),
        (ICON["check"], "Military, first responder and teacher discount", "With valid ID"),
    ]
    lis = "".join(f'<li>{i}<div><strong>{a}</strong><span>{b}</span></div></li>' for i, a, b in items)
    return f'<section class="facts" aria-label="Why customers trust us"><ul class="wrap facts-list">{lis}</ul></section>'

SERVICE_OPTIONS = [s["select"] for s in SERVICES] + ["Something else"]

def form_block(heading="Get a free estimate", lead=None, preselect="", sec_id="estimate"):
    lead = lead or f"Tell us what is going on and we will get back to you. Estimates are free within city limits. For anything urgent, call {B['phone_display']}."
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{o}</option>' for o in SERVICE_OPTIONS)
    return f'''<section class="estimate" id="{sec_id}" aria-labelledby="{sec_id}-h">
  <div class="wrap estimate-grid">
    <div class="estimate-copy">
      <h2 id="{sec_id}-h">{heading}</h2>
      <p>{lead}</p>
      <div class="estimate-call">
        <span>Faster by phone</span>
        {tel("form_side", "bignum bignum-sm", B["phone_display"])}
        <span class="muted">Open {B["hours"]}</span>
      </div>
    </div>
    <form class="form" name="estimate" method="POST" novalidate>
      <input type="hidden" name="page" value="">
      <p class="hp"><label>Leave this empty <input name="_honey" tabindex="-1" autocomplete="off"></label></p>
      <div class="row2">
        <label>Your name<input name="name" autocomplete="name" required></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
      </div>
      <div class="row2">
        <label><span>Email <span class="opt">(optional)</span></span><input name="email" type="email" autocomplete="email"></label>
        <label>ZIP code<input name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="10"></label>
      </div>
      <label>What do you need help with?<select name="service" required><option value="">Choose one</option>{opts}</select></label>
      <label><span>Details <span class="opt">(optional)</span></span><textarea name="message" rows="3" placeholder="Where is the problem and when did it start?"></textarea></label>
      <button class="btn btn-blue btn-block" type="submit">Request my free estimate</button>
      <p class="form-status" role="status" aria-live="polite"></p>
      <p class="fine">By sending this form you agree we can contact you about your request. See our <a href="/privacy/">privacy policy</a>.</p>
    </form>
  </div>
</section>'''

def cta_band(heading="Have a plumbing problem?", text=None):
    text = text or f"Call us and talk to a licensed plumber. Estimates are free within city limits. Open {B['hours']}."
    return f'''<section class="cta-band"><div class="wrap cta-in">
  <div><h2>{heading}</h2><p>{text}</p></div>
  <div class="cta-actions">{tel("cta_band", "btn btn-call btn-lg", ICON["phone"] + "<span>" + B["phone_display"] + "</span>")}
  <a class="btn btn-ghost-light btn-lg" href="/contact/">Request an estimate</a></div>
</div></section>'''

def footer():
    svc_links = "".join(f'<li><a href="{svc_path(s)}">{s["name"]}</a></li>' for s in SERVICES)
    return f'''<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <img src="/img/logo-120.webp" width="130" height="120" alt="{B["short"]} logo" loading="lazy">
      <p><strong>{B["name"]}</strong><br>Texas license {B["license"]}<br>Licensed and insured</p>
      {board_notice("board-foot")}
      <p><a href="{B["maps"]}" target="_blank" rel="noopener noreferrer">Find us on Google</a><br><a href="{B["facebook"]}" target="_blank" rel="noopener noreferrer">Follow us on Facebook</a></p>
    </div>
    <div class="footer-svcs">
      <h2>Services</h2>
      <ul>{svc_links}</ul>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about/">About us</a></li>
        <li><a href="/reviews/">Reviews</a></li>
        <li><a href="/service-areas/">Service areas</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy/">Privacy policy</a></li>
      </ul>
    </div>
    <div>
      <h2>Call us</h2>
      <p>{tel("footer", "footer-phone")}<br>Open {B["hours"]}<br>{B["weekends"]}</p>
      <p><a href="mailto:{B["email"]}">{B["email"]}</a></p>
    </div>
  </div>
  <div class="wrap footer-base">
    <span>&copy; <span data-year>2026</span> {B["name"]}. All rights reserved.</span>
    <span>Serving San Antonio, TX and surrounding areas</span>
  </div>
</footer>
<div class="callbar" role="region" aria-label="Quick contact">
  {tel("sticky_bar", "callbar-call", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
  <a class="callbar-est" href="/contact/">Free estimate</a>
</div>'''

def page(path, title, desc, body, active="", schema=None, og_img="/img/og.jpg"):
    canonical = B["url"] + path
    schema_tags = "".join(f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>' for s in (schema or []))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{gtag_head()}<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#06173A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{B["name"]}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{B["url"]}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/barlow-condensed-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/public-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v=6">
<script src="/js/site.js?v=5" defer></script>
{schema_tags}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    out = os.path.join(DIST, path.strip("/"), "index.html") if path != "/" else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(doc)
    return out

# ---------------------------------------------------------------- schema
BUSINESS_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Plumber",
    "@id": B["url"] + "/#business",
    "name": B["name"],
    "url": B["url"] + "/",
    "telephone": B["phone_tel"],
    "email": B["email"],
    "logo": B["url"] + "/img/logo-240.png",
    "image": B["url"] + "/img/og.jpg",
    "founder": {"@type": "Person", "name": B["owner"]},
    "address": {"@type": "PostalAddress", "addressLocality": "San Antonio", "addressRegion": "TX", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": "San Antonio", "containedInPlace": {"@type": "State", "name": "Texas"}}] + [{"@type": "Place", "name": a + ", TX"} for a in AREAS],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
    "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                      "name": "Texas Responsible Master Plumber license " + B["license"]},
    "knowsAbout": [s["name"] for s in SERVICES],
    "sameAs": [B["maps"], B["facebook"]],
}

def crumbs(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": B["url"] + "/"}]
    for i, (name, path) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": B["url"] + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def crumb_nav(trail):
    parts = ['<a href="/">Home</a>']
    for i, (name, path) in enumerate(trail):
        parts.append(f'<span>{name}</span>' if i == len(trail) - 1 else f'<a href="{path}">{name}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(parts) + '</nav>'

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

FAQ = [
    ("Do you give free estimates?", "Yes. Estimates are free within San Antonio city limits."),
    ("Are you licensed and insured?", f"Yes. JQ Plumbing is fully licensed and insured. Our Texas plumbing license is {B['license']}, and our plumbers are fingerprint background checked."),
    ("What are your hours?", f"We are open {B['hours']}. {B['weekends']} We are not a 24 hour service."),
    ("What warranty do you offer?", "All parts carry the manufacturer warranty. Our workmanship is covered for 90 days to 1 year, depending on the size and scope of the job."),
    ("Do you offer any discounts?", "Yes. Military, first responders and teachers get a discount with a valid ID."),
    ("Do you work on commercial properties?", "Yes. We are a residential and commercial plumbing company."),
    ("What areas do you serve?", "San Antonio and the surrounding areas, including " + ", ".join(AREAS[:-1]) + " and " + AREAS[-1] + "."),
]

def faq_html(faqs):
    return "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)

def svc_cards(cls="svc-grid"):
    cards = "".join(f'''<li><a class="svc-card" href="{svc_path(s)}">
  <span class="svc-card-img">{pic(s["hero"][0], s["hero"][1], sizes="(min-width: 960px) 30vw, (min-width: 600px) 45vw, 92vw")}</span>
  <span class="svc-card-body"><h3>{s["name"]}</h3><p>{s["intro"]}</p><span class="svc-card-more">View service {ICON["arrow"]}</span></span>
</a></li>''' for s in SERVICES)
    return f'<ul class="{cls}">{cards}</ul>'

def review_card(r, full=False):
    paras = [esc(x) for x in r["text"].split("\n\n")]
    if full:
        body = "".join(f"<p>{x}</p>" for x in paras)
    else:
        more = "".join(f"<p>{x}</p>" for x in paras[1:])
        body = f"<p>{paras[0]}</p>" + (f'<details class="rev-more"><summary>Read full review</summary>{more}</details>' if more else "")
    return (f'<blockquote class="review"><div class="stars" role="img" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            f'{body}<footer>{esc(r["name"])}, Google review</footer></blockquote>')

def steps_html():
    steps = [
        ("Call or send a request", f"Call {B['phone_display']} or send the estimate form. Tell us what is going on."),
        ("Get a clear estimate", "We look at the problem and give you a clear price before any work starts. Estimates are free within city limits."),
        ("We do the work right", "Licensed, background checked plumbers do the job and clean up when they are done."),
        ("Covered by warranty", "Parts carry the manufacturer warranty, and our workmanship is covered for 90 days to 1 year depending on the job."),
    ]
    lis = "".join(f'<li><span class="step-n" aria-hidden="true">{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps, 1))
    return f'''<section class="steps"><div class="wrap">
  <div class="sec-head"><h2>How it works</h2><p>Simple, upfront and no surprises.</p></div>
  <ol class="steps-list">{lis}</ol>
</div></section>'''

def page_hero(h1, sub, trail, extra=""):
    return f'''<section class="page-hero"><div class="wrap">
  {crumb_nav(trail)}
  <h1>{h1}</h1>
  <p class="hero-sub">{sub}</p>
  <div class="hero-actions">
    {tel("page_hero", "btn btn-call btn-lg", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
    {extra}
  </div>
</div></section>'''

# ---------------------------------------------------------------- pages
def home():
    gallery = [
        ("camera-pipe", "Sewer camera inspection showing the inside of a drain line"),
        ("slab-roughin", "Under slab plumbing laid out before a concrete pour"),
        ("water-softener", "Water treatment system installed in a utility closet"),
        ("faucet-brushed", "Newly installed brushed nickel kitchen faucet"),
        ("meter-line", "New water service line connected at the meter box"),
        ("under-sink", "New kitchen sink drain and trap under the counter"),
        ("tunnel", "Plumber working in a tunnel under a slab"),
        ("roof-vent", "Plumber running a camera down a roof vent stack"),
    ]
    gal = "".join(f'<figure>{pic(n, a, sizes="(min-width: 960px) 25vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in gallery)
    reviews = "".join(review_card(review_by(n)) for n in ["Jose Torres", "Crash_2600"])
    towns = "".join(f"<li>{a}</li>" for a in AREAS[:10])
    body = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Licensed plumbers for San Antonio homes and businesses</h1>
      <p class="hero-sub">Local and family owned, with {B["years"]} years in the trade. Honest work, fair pricing, and we stand behind it.</p>
      <div class="hero-call">
        {tel("hero_number", "bignum", B["phone_display"])}
        <p class="hero-call-note">{ICON["clock"]}<span>Tap to call. Open {B["hours"]}.</span></p>
      </div>
      <div class="hero-actions">
        {tel("hero_button", "btn btn-call btn-lg", ICON["phone"] + "<span>Call now</span>")}
        <a class="btn btn-ghost-light btn-lg" href="/contact/">Get a free estimate</a>
      </div>
    </div>
    <figure class="hero-photo">
      {pic("hero-tankless", "JQ Plumbing plumbers working on a water heater at a San Antonio home", sizes="(min-width: 960px) 40vw, 100vw", eager=True)}
      <figcaption>Our crew on a water heater job in San Antonio</figcaption>
    </figure>
  </div>
</section>
{facts_strip()}
<section class="services"><div class="wrap">
  <div class="sec-head sec-head-row">
    <div><h2>Plumbing services</h2><p>Residential and commercial plumbing across San Antonio and the surrounding areas.</p></div>
    <a class="link-arrow" href="/services/">All services {ICON["arrow"]}</a>
  </div>
  {svc_cards()}
</div></section>
<section class="about"><div class="wrap about-grid">
  <figure class="about-photo">{pic("jon", f"{B['owner']}, owner of JQ Plumbing LLC", sizes="(min-width: 960px) 34vw, 100vw")}</figure>
  <div class="about-copy">
    <h2>Local, family owned, and here for the long run</h2>
    <p>JQ Plumbing is owned by {B["owner"]} and his wife. Jonathan is a licensed plumber with {B["years"]} years of experience, and our employees are family men too.</p>
    <p>We are focused on giving real value and the best customer experience possible. Honest, trustworthy, skilled and reliable is how we work.</p>
    <a class="btn btn-ghost" href="/about/">More about us</a>
  </div>
</div></section>
{steps_html()}
<section class="work"><div class="wrap">
  <div class="sec-head"><h2>Recent jobs</h2><p>Real photos from our job sites. No stock pictures.</p></div>
  <div class="gallery">{gal}</div>
</div></section>
<section class="reviews"><div class="wrap">
  <div class="sec-head sec-head-row">
    <div><h2>What customers say</h2><p class="rev-sub">Real reviews from our customers on Google, word for word.</p></div>
    <a class="link-arrow link-light" href="/reviews/">All reviews {ICON["arrow"]}</a>
  </div>
  <div class="review-list">{reviews}</div>
</div></section>
<section class="area"><div class="wrap area-grid">
  <div>
    <h2>Serving San Antonio and surrounding areas</h2>
    <p>We work throughout San Antonio, TX and nearby communities. Estimates are free within city limits.</p>
    <ul class="towns">{towns}<li class="towns-more"><a href="/service-areas/">and {len(AREAS) - 10} more</a></li></ul>
    <a class="link-arrow" href="/service-areas/">See all service areas {ICON["arrow"]}</a>
  </div>
  <div class="faq">
    <h2 class="faq-h">Common questions</h2>
    {faq_html(FAQ[:5])}
  </div>
</div></section>
{form_block()}'''
    page("/", "Licensed Plumber in San Antonio, TX | JQ Plumbing LLC",
         f"Licensed, insured, family owned plumbers in San Antonio. Drains, water heaters, leaks and repairs. Free estimates in city limits. Call {B['phone_display']}.",
         body, "home", [BUSINESS_SCHEMA, faq_schema(FAQ)])

def services_index():
    body = page_hero("Plumbing services in San Antonio",
                     "Residential and commercial plumbing from licensed, background checked plumbers. Choose a service to see what is included.",
                     [("Services", "/services/")],
                     '<a class="btn btn-ghost-light btn-lg" href="/contact/">Get a free estimate</a>')
    body += facts_strip()
    body += f'<section class="services"><div class="wrap">{svc_cards()}</div></section>'
    body += steps_html() + cta_band()
    page("/services/", "Plumbing Services in San Antonio, TX | JQ Plumbing LLC",
         "Drain cleaning, sewer camera inspection, water heaters, water treatment, leak detection, fixtures, repairs, tunnel work and commercial plumbing in San Antonio.",
         body, "services", [BUSINESS_SCHEMA, crumbs([("Services", "/services/")])])

def service_page(s):
    path = svc_path(s)
    handle = "".join(f'<li>{ICON["check"]}<span>{i}</span></li>' for i in s["handle"])
    signs = "".join(f"<li>{x}</li>" for x in s["signs"])
    photos = "".join(f'<figure>{pic(n, a, sizes="(min-width: 960px) 30vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in s["photos"])
    lead = "".join(f"<p>{p}</p>" for p in s["lead"])
    rname, ridx = s["review"]
    r = review_by(rname)
    quote = esc(r["text"].split("\n\n")[ridx])
    related = [x for x in SERVICES if x is not s][:3] if s["slug"] != SERVICES[0]["slug"] else SERVICES[1:4]
    idx = SERVICES.index(s)
    related = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
    rel = "".join(f'<li><a class="rel-card" href="{svc_path(x)}"><strong>{x["name"]}</strong><span>{x["short"]}</span>{ICON["arrow"]}</a></li>' for x in related)
    faqs = s["faqs"] + [FAQ[0], FAQ[2]]
    trail = [("Services", "/services/"), (s["name"], path)]
    body = f'''<section class="hero hero-svc">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumb_nav(trail)}
      <h1>{s["h1"]}</h1>
      <p class="hero-sub">{s["intro"]}</p>
      <div class="hero-call">
        {tel("hero_number", "bignum", B["phone_display"])}
        <p class="hero-call-note">{ICON["clock"]}<span>Tap to call. Open {B["hours"]}.</span></p>
      </div>
      <div class="hero-actions">
        {tel("hero_button", "btn btn-call btn-lg", ICON["phone"] + "<span>Call now</span>")}
        <a class="btn btn-ghost-light btn-lg" href="/contact/?service={s["slug"]}">Get a free estimate</a>
      </div>
    </div>
    <figure class="hero-photo">{pic(s["hero"][0], s["hero"][1], sizes="(min-width: 960px) 40vw, 100vw", eager=True)}<figcaption>{s["hero"][2]}</figcaption></figure>
  </div>
</section>
{facts_strip()}
<section class="overview"><div class="wrap overview-grid">
  <div class="overview-copy">
    <h2>{s["name"]} done right</h2>
    {lead}
  </div>
  <div class="handle">
    <h3>What we handle</h3>
    <ul>{handle}</ul>
  </div>
</div></section>
<section class="signs-sec"><div class="wrap signs-grid">
  <div>
    <h2>{s["signs_h"]}</h2>
    <ul class="signs-list">{signs}</ul>
  </div>
  <aside class="signs-note">
    <p>{s["signs_note"]}</p>
    {tel("signs_box", "btn btn-call btn-block btn-lg", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
    <p class="muted">Open {B["hours"]}. {B["weekends"]}</p>
  </aside>
</div></section>
{steps_html()}
<section class="work"><div class="wrap">
  <div class="sec-head"><h2>From our job sites</h2><p>Real photos of our work. No stock pictures.</p></div>
  <div class="gallery gallery-{len(s["photos"])}">{photos}</div>
</div></section>
<section class="quote-sec"><div class="wrap narrow">
  <figure class="quote">
    <div class="stars" role="img" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
    <blockquote><p>{quote}</p></blockquote>
    <figcaption>{esc(r["name"])}, Google review <a href="/reviews/">Read more reviews</a></figcaption>
  </figure>
</div></section>
<section class="svc-faq"><div class="wrap narrow faq">
  <h2>Questions about {s["name"].lower()}</h2>
  {faq_html(faqs)}
</div></section>
{form_block(heading="Get a free estimate", preselect=s["select"])}
<section class="related"><div class="wrap">
  <div class="sec-head sec-head-row"><h2>Related services</h2><a class="link-arrow" href="/services/">All services {ICON["arrow"]}</a></div>
  <ul class="rel-list">{rel}</ul>
</div></section>'''
    page(path, s["title"], s["desc"], body, "svc:" + s["slug"],
         [BUSINESS_SCHEMA,
          {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
           "description": s["desc"], "url": B["url"] + path, "provider": {"@id": B["url"] + "/#business"},
           "areaServed": {"@type": "City", "name": "San Antonio"}},
          crumbs(trail), faq_schema(faqs)])

def about():
    values = [("Honest", "Clear prices before the work starts and straight answers about the work."),
              ("Trustworthy", "Licensed, insured and fingerprint background checked plumbers in your home or business."),
              ("Skilled", f"{B['years']} years in the trade, licensed under Texas license {B['license']}."),
              ("Reliable", "We stand behind our warranty and our work.")]
    vals = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in values)
    body = page_hero("About JQ Plumbing", "A local, family owned plumbing company serving San Antonio homes and businesses.", [("About", "/about/")],
                     '<a class="btn btn-ghost-light btn-lg" href="/contact/">Get a free estimate</a>')
    body += f'''<section class="story"><div class="wrap about-grid">
  <figure class="about-photo">{pic("jon", f"{B['owner']}, owner of JQ Plumbing LLC", sizes="(min-width: 960px) 34vw, 100vw", eager=True)}</figure>
  <div class="about-copy">
    <h2>Family owned, and it shows</h2>
    <p>JQ Plumbing LLC is a local, family owned company. {B["owner"]} and his wife own the business, and our employees are family men too. Jonathan has been plumbing for {B["years"]} years and is a licensed plumber.</p>
    <p>We are hard focused on providing value and the best customer experience possible. That means showing up, explaining the work clearly, doing it right and cleaning up after ourselves.</p>
    <p>Giving back to the community is important to us.</p>
  </div>
</div></section>
<section class="values"><div class="wrap">
  <div class="sec-head"><h2>How we work</h2></div>
  <ul class="values-list">{vals}</ul>
</div></section>
<section class="creds"><div class="wrap creds-grid">
  <div><h2>Licensed, insured and covered</h2></div>
  <ul class="ticks">
    <li>{ICON["check"]}Fully licensed and insured, Texas license {B["license"]}</li>
    <li>{ICON["check"]}Licensed plumbers, fingerprint background checked</li>
    <li>{ICON["check"]}Residential and commercial service</li>
    <li>{ICON["check"]}Manufacturer warranty on all parts, plus 90 days to 1 year on workmanship</li>
    <li>{ICON["check"]}Free estimates within city limits</li>
    <li>{ICON["check"]}Military, first responder and teacher discount with valid ID</li>
  </ul>
</div></section>
<section class="work"><div class="wrap">
  <div class="sec-head"><h2>Our work</h2></div>
  <div class="gallery">{"".join(f'<figure>{pic(n, a, sizes="(min-width: 960px) 25vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in [("water-heater-team", "Our crew on a water heater job"), ("tunnel", "Tunnel work under a slab"), ("slab-wide", "Under slab plumbing before a pour"), ("faucet-gold", "A new kitchen faucet install")])}</div>
</div></section>
{cta_band()}'''
    page("/about/", "About JQ Plumbing LLC | Family Owned San Antonio Plumbers",
         f"JQ Plumbing LLC is a local, family owned, licensed and insured plumbing company in San Antonio. {B['years']} years in the trade. Texas license {B['license']}.",
         body, "/about/", [BUSINESS_SCHEMA, crumbs([("About", "/about/")])])

def reviews_page():
    cards = "".join(review_card(r, full=True) for r in REVIEWS)
    body = page_hero("Customer reviews", "Real reviews from our customers on Google, shared word for word.", [("Reviews", "/reviews/")],
                     f'<a class="btn btn-ghost-light btn-lg" href="{B["maps"]}" target="_blank" rel="noopener noreferrer">See us on Google</a>')
    body += f'''<section class="reviews reviews-page"><div class="wrap">
  <div class="review-list review-masonry">{cards}</div>
  <p class="center review-actions"><a class="btn btn-ghost" href="{B["reviews_all"]}" target="_blank" rel="noopener noreferrer">Read all our reviews on Google</a> <a class="btn btn-blue" href="{B["review_write"]}" target="_blank" rel="noopener noreferrer">Leave us a review</a></p>
</div></section>
{cta_band("Ready to be our next happy customer?")}'''
    page("/reviews/", "Reviews | JQ Plumbing LLC, San Antonio Plumber",
         "Read real Google reviews from JQ Plumbing LLC customers in San Antonio. Honest, upfront, on time and fairly priced plumbing.",
         body, "/reviews/", [BUSINESS_SCHEMA, crumbs([("Reviews", "/reviews/")])])

def areas_page():
    towns = "".join(f'<li>{ICON["pin"]}<span>{a}</span></li>' for a in ["San Antonio"] + AREAS)
    body = page_hero("Service areas", "Licensed plumbing for San Antonio, TX and the surrounding communities.", [("Service areas", "/service-areas/")],
                     '<a class="btn btn-ghost-light btn-lg" href="/contact/">Get a free estimate</a>')
    body += f'''<section class="areas-sec"><div class="wrap areas-grid">
  <div class="areas-copy">
    <h2>Where we work</h2>
    <p>JQ Plumbing serves homes and businesses across San Antonio and these nearby communities. Estimates are free within city limits.</p>
    <p>Do not see your town? Give us a call and ask.</p>
    <p class="muted">Open {B["hours"]}. {B["weekends"]}</p>
  </div>
  <ul class="town-grid">{towns}</ul>
</div></section>
<section class="services"><div class="wrap">
  <div class="sec-head"><h2>Services in every area we cover</h2></div>
  {svc_cards()}
</div></section>
{cta_band()}'''
    page("/service-areas/", "Plumbing Service Areas Around San Antonio, TX | JQ Plumbing",
         "JQ Plumbing serves San Antonio, Schertz, New Braunfels, Boerne, Seguin, Converse, Universal City, Stone Oak and more. Free estimates in city limits.",
         body, "/service-areas/", [BUSINESS_SCHEMA, crumbs([("Service areas", "/service-areas/")])])

def contact_page():
    body = f'''<section class="page-hero"><div class="wrap">
  {crumb_nav([("Contact", "/contact/")])}
  <h1>Contact JQ Plumbing</h1>
  <p class="hero-sub">Call to talk to a licensed plumber, or send a request and we will get back to you.</p>
</div></section>
<section class="contact-cards"><div class="wrap contact-grid">
  <div class="c-card c-card-main">
    <h2>Call us</h2>
    {tel("contact_card", "bignum bignum-sm", B["phone_display"])}
    <p class="muted">The fastest way to reach us</p>
  </div>
  <div class="c-card">
    <h2>Hours</h2>
    <p>{B["hours"]}</p>
    <p class="muted">{B["weekends"]} We are not a 24 hour service.</p>
  </div>
  <div class="c-card">
    <h2>Email</h2>
    <p><a href="mailto:{B["email"]}">{B["email"]}</a></p>
    <p class="muted">Serving San Antonio, TX and surrounding areas. <a href="/service-areas/">See areas</a></p>
  </div>
</div></section>
{form_block(heading="Request a free estimate", sec_id="estimate")}
<section class="svc-faq"><div class="wrap narrow faq">
  <h2>Common questions</h2>
  {faq_html(FAQ)}
</div></section>'''
    page("/contact/", "Contact JQ Plumbing LLC | San Antonio Plumber | 210-793-6046",
         f"Call JQ Plumbing at {B['phone_display']} or request a free estimate online. Open {B['hours']}. Serving San Antonio and surrounding areas.",
         body, "/contact/", [BUSINESS_SCHEMA, crumbs([("Contact", "/contact/")]), faq_schema(FAQ)])

def privacy():
    body = f'''<section class="legal"><div class="wrap narrow">
<h1>Privacy policy</h1>
<p>This policy explains what information {B["name"]} collects through this website and how we use it.</p>
<h2>Information you send us</h2>
<p>When you fill out our estimate form we collect what you enter, such as your name, phone number, email, ZIP code and a description of your plumbing problem. We use it only to respond to your request and provide our services. We do not sell your information. Form submissions are delivered to us by email through a form delivery service.</p>
<h2>Analytics and advertising</h2>
<p>We use Google Analytics and Google Ads to understand how visitors use our site and to measure calls and form requests from our ads. These services may use cookies to collect information such as pages visited and the device used. You can learn how Google uses this data at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">policies.google.com/technologies/partner-sites</a> and opt out of personalized ads at <a href="https://adssettings.google.com" rel="noopener" target="_blank">adssettings.google.com</a>.</p>
<h2>Contact</h2>
<p>Questions about this policy? Email <a href="mailto:{B["email"]}">{B["email"]}</a> or call {tel("privacy", "", B["phone_display"])}.</p>
</div></section>'''
    page("/privacy/", "Privacy Policy | JQ Plumbing LLC", f"Privacy policy for {B['name']}, a licensed plumbing company in San Antonio, TX.", body, "/privacy/")

def not_found():
    body = f'''<section class="page-hero"><div class="wrap">
<h1>That page is not here</h1>
<p class="hero-sub">The link may be old. Try one of our services below, or call us at {tel("404", "", B["phone_display"])}.</p>
</div></section>
<section class="services"><div class="wrap">{svc_cards()}</div></section>'''
    out = page("/404-tmp/", "Page not found | JQ Plumbing LLC", "Page not found.", body, "")
    os.replace(out, os.path.join(DIST, "404.html")); os.rmdir(os.path.dirname(out))

def extras():
    urls = ["/", "/services/"] + [svc_path(s) for s in SERVICES] + ["/about/", "/reviews/", "/service-areas/", "/contact/", "/privacy/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{B['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {B['url']}/sitemap.xml\n")

if __name__ == "__main__":
    home()
    services_index()
    for s in SERVICES:
        service_page(s)
    about()
    reviews_page()
    areas_page()
    contact_page()
    privacy()
    not_found()
    extras()
    print("built", DIST, len(SERVICES), "service pages")
