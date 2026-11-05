#!/usr/bin/env python3
"""Builds the JQ Plumbing static site into ./dist.
Edit the BUSINESS block or page copy here, then run: python3 build.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

# ---------------------------------------------------------------- business facts (from Jon)
B = {
    "name": "JQ Plumbing LLC",
    "short": "JQ Plumbing",
    "owner": "Jonathan Quintanilla",
    "phone_display": "210-793-6046",
    "phone_tel": "+12107936046",
    "license": "RMP-47009",
    "email": "Jonq@jqplumbingllc.com",
    "url": "https://jqplumbingllc.com",
    "area": "San Antonio, TX and surrounding areas",
    "hours": "Monday to Friday, 9am to 5pm",
    "weekends": "Weekends are for scheduled and emergency work.",
    "years": "10",
    "maps": "https://maps.app.goo.gl/ebH1gkydNdcFtpzK9",
    "facebook": "https://www.facebook.com/61573244019779/",
}

AREAS = ['Schertz', 'New Braunfels', 'Canyon Lake', 'Bandera', 'Converse', 'Kirby', 'City Base', 'Castroville', 'Lytle', 'Devine', 'Somerset', 'Elmendorf', 'Floresville', 'Bulverde', 'Stone Oak', 'Boerne', 'Marion', 'Seguin', 'Universal City']

# Paste Jon's real Google reviews here, word for word. Section stays hidden while empty.
# Example: {"name": "Maria G.", "text": "Exact review text...", "stars": 5}
REVIEWS = [{'name': 'Jose Torres', 'text': 'I had an excellent experience working with JQ Plumbing LLC during a recent home renovation. They handled several important plumbing projects, including installing a new water heater, bringing the plumbing up to code, and helping diagnose a gas leak.\n\nWhat impressed me most was the honesty and transparency throughout the entire process. From the beginning, he was upfront about pricing, clearly explained his recommendations, and made sure I understood the work that needed to be done. His pricing was also very reasonable and competitive.\n\nI especially appreciated that he was personally involved in much of the work alongside his crew. It’s clear that he takes pride in his workmanship and operates his business with a high level of integrity.\n\nFinding a contractor who is honest, dependable, and fairly priced isn’t always easy. JQ Plumbing LLC certainly earned my trust, and I would highly recommend them to anyone needing quality plumbing services. I wouldn’t hesitate to use them again!', 'stars': 5}, {'name': 'Crash_2600', 'text': 'I had major plumbing issues that I kept off for many years. A few weeks ago it finally caught up to me and I needed to fix it asap. I had about 6 estimates done and everyone’s was way out of my budget. Jonathan with JQ Plumbing LLC contacted me and was able to squeeze me in on a random day for an estimate.\n\nRight off the bat Jonathan and Jesse pointed out issues that I didn’t know were bad or getting to that point. They also mentioned faulty things with previous work that was done. They were very professional and thinking long term so I would never have to deal with this again. They were the lowest estimate of all the 6 others I received. Jonathan was very communicative with me and answering all the questions I had pertaining to the estimate and work, including the poorly installed water heater I had the previous year.\n\nWork began and I was impressed with the constant communication between myself and Jonathan, pertaining to the work being done. A price was set and work started. From the start they were on time and very professional. Jesse, Marcel, Jonathan, and Ismael were very courteous to my needs and were very professional when it came to my home. I was comfortable enough to leave them in my home without me being there and they were very professional in their up keep of the house after they were done for the day.\n\nEveryone was attentive and I am very happy and confident that the job was done right. Problems with the pipeline in different areas were brought up which added costs, but Jonathan was able to provide documentation so I wouldn’t feel like I was getting robbed, major kudos for that. I highly recommend JQ Plumbing LLC for any plumbing needs no matter how big or small. I am also very happy that they were attentive to my 2 dogs when I wasn’t there. All of them are a great team and work well together. Again, 5 star company and I would definitely hire these guys again. Communication, budget, professionalism, honesty, courtesy, and integrity were selling points for me, which they all achieved. ⭐️⭐️⭐️⭐️⭐️', 'stars': 5}, {'name': 'Sean Seaworth', 'text': 'I hired the team because they seemed the most prepared and most professional. They one hundred percent were. They did a great job done quickly and took care of all my needs. Will be using them exclusively going forward.', 'stars': 5}, {'name': 'Google reviewer', 'text': 'I needed an expansion tank replaced on my water heater additionally I needed a PRV replaced. JQ (Jonathan)showed up when he said he would, he finished the job in less time than he quoted. JQ and his helper were courteous and professionally in dress and in actions. I was pleased with the work they did and I will call JQ plumbing next time I need any type of plumbing work done. I just had some additional work done by JQ Plumbing. They did a great job: showed up when they said they would, finished when they said they would, charged m what they said they would. They also did a good job cleaning everything up. I will use them again!', 'stars': 5}]

ICON = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "badge": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5zm-1.2 14.2-3.5-3.5 1.4-1.4 2.1 2.1 4.9-4.9 1.4 1.4z"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.4 11.6 12.4 2.6A2 2 0 0 0 11 2H4a2 2 0 0 0-2 2v7c0 .55.22 1.05.59 1.41l9 9a2 2 0 0 0 2.82 0l7-7a2 2 0 0 0 0-2.82zM6.5 8A1.5 1.5 0 1 1 8 6.5 1.5 1.5 0 0 1 6.5 8z"/></svg>',
    "home": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 12h3v8h5v-6h4v6h5v-8h3z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 10.4 3.5 2.1-.8 1.3L11 13V7h2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 14.5 9 2.5 2.5 0 0 1 12 11.5z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
}

def esc(s):
    return html.escape(s, quote=True)

def tel(loc, cls="", inner=None):
    inner = inner or B["phone_display"]
    return f'<a class="{cls}" href="tel:{B["phone_tel"]}" data-call-location="{loc}">{inner}</a>'

def pic(name, alt, sizes="(min-width: 960px) 50vw, 100vw", cls="", eager=False, w=1200, h=1600):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/img/{name}-640.webp" '
            f'srcset="/img/{name}-640.webp 640w, /img/{name}-1200.webp 1200w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {load}>')

# ---------------------------------------------------------------- shared chunks
def header(active=""):
    nav = [("/#services", "Services"), ("/#about", "About"), ("/#area", "Service area"), ("/#estimate", "Free estimate")]
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in nav)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="/" aria-label="{B["name"]} home">
      <img src="/img/logo-120.webp" width="130" height="120" alt="{B["short"]} logo, license {B["license"]}">
      <span class="brand-txt"><strong>{B["short"]}</strong><span>Lic. {B["license"]}</span></span>
    </a>
    <nav class="nav" aria-label="Main">{links}</nav>
    {tel("header", "btn btn-call topcall", ICON["phone"] + '<span class="topcall-label">Call </span><span>' + B["phone_display"] + '</span>')}
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

SERVICE_OPTIONS = ["Drain cleaning or clog", "Sewer camera inspection", "Water heater", "Water leak",
                   "Burst pipe or urgent repair", "Fixture or faucet replacement", "Water treatment system",
                   "Commercial plumbing", "Something else"]

def form_block(heading="Get a free estimate", lead=None, preselect=""):
    lead = lead or f"Tell us what is going on and we will get back to you. Estimates are free within city limits. For anything urgent, call {B['phone_display']}."
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{o}</option>' for o in SERVICE_OPTIONS)
    return f'''<section class="estimate" id="estimate" aria-labelledby="estimate-h">
  <div class="wrap estimate-grid">
    <div class="estimate-copy">
      <h2 id="estimate-h">{heading}</h2>
      <p>{lead}</p>
      <div class="estimate-call">
        <span>Faster by phone</span>
        {tel("form_side", "bignum bignum-sm", B["phone_display"])}
        <span class="muted">Open {B["hours"]}</span>
      </div>
    </div>
    <form class="form" name="estimate" method="POST" novalidate>
      <input type="hidden" name="form-name" value="estimate">
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

def footer():
    return f'''<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <img src="/img/logo-120.webp" width="130" height="120" alt="{B["short"]} logo" loading="lazy">
      <p><strong>{B["name"]}</strong><br>Texas license {B["license"]}<br>Licensed and insured</p>
    </div>
    <div>
      <h2>Call us</h2>
      <p>{tel("footer", "footer-phone")}<br>Open {B["hours"]}<br><a href="mailto:{B["email"]}">{B["email"]}</a></p>
    </div>
    <div>
      <h2>Services</h2>
      <ul>
        <li><a href="/drain-cleaning-san-antonio/">Drain cleaning and camera inspection</a></li>
        <li><a href="/water-heater-repair-san-antonio/">Water heater repair and installation</a></li>
        <li><a href="/leak-detection-san-antonio/">Leak detection and repair</a></li>
        <li><a href="/emergency-plumber-san-antonio/">Burst pipes and urgent repairs</a></li>
      </ul>
    </div>
    <div>
      <h2>Service area</h2>
      <p>{B["area"]}</p>
      <p><a href="{B["maps"]}" rel="noopener" target="_blank">Find us on Google</a><br><a href="{B["facebook"]}" rel="noopener" target="_blank">Follow us on Facebook</a></p>
    </div>
  </div>
  <div class="wrap footer-base">
    <span>&copy; <span data-year>2026</span> {B["name"]}. All rights reserved.</span>
    <a href="/privacy/">Privacy policy</a>
  </div>
</footer>
<div class="callbar" role="region" aria-label="Quick contact">
  {tel("sticky_bar", "callbar-call", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
  <a class="callbar-est" href="#estimate">Free estimate</a>
</div>'''

def page(path, title, desc, body, schema=None, og_img="/img/og.jpg"):
    canonical = B["url"] + path
    schema_tags = "".join(f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>' for s in (schema or []))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
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
<link rel="stylesheet" href="/css/site.css">
<script src="/js/site.js" defer></script>
{schema_tags}
</head>
<body>
{header()}
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
    "knowsAbout": ["Drain cleaning", "Sewer camera inspection", "Water heater repair", "Water heater installation",
                   "Leak detection", "Water treatment systems", "Fixture replacement", "Tunnel work", "Commercial plumbing"],
    "sameAs": [B["maps"], B["facebook"]],
}

def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": B["url"] + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": B["url"] + path}]}

def service_schema(name, path, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "description": desc, "url": B["url"] + path, "provider": {"@id": B["url"] + "/#business"},
            "areaServed": {"@type": "City", "name": "San Antonio"}}

FAQ = [
    ("Do you give free estimates?", "Yes. Estimates are free within San Antonio city limits."),
    ("Are you licensed and insured?", f"Yes. JQ Plumbing is fully licensed and insured. Our Texas plumbing license is {B['license']}, and our plumbers are fingerprint background checked."),
    ("What are your hours?", f"We are open {B['hours']}. {B['weekends']} We are not a 24 hour service."),
    ("What warranty do you offer?", "All parts carry the manufacturer warranty. Our workmanship is covered for 90 days to 1 year, depending on the size and scope of the job."),
    ("Do you offer any discounts?", "Yes. Military, first responders and teachers get a discount with a valid ID."),
    ("Do you work on commercial properties?", "Yes. We are a residential and commercial plumbing company."),
    ("What areas do you serve?", "San Antonio and the surrounding areas, including " + ", ".join(AREAS[:-1]) + " and " + AREAS[-1] + "."),
]

def faq_schema():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

# ---------------------------------------------------------------- home
SERVICES = [
    ("/drain-cleaning-san-antonio/", "Drain cleaning and sewer camera inspection", "Clogged sinks, showers, toilets and main lines. We can run a camera down the line so you see the problem before you pay to fix it.", "drain-machine", "Drain cleaning machine clearing a commercial restroom drain"),
    ("/water-heater-repair-san-antonio/", "Water heater repair and installation", "No hot water, a leaking tank or an old unit ready to go. We repair and install water heaters, plus water treatment systems.", "water-heater-team", "JQ Plumbing team working on a wall mounted water heater"),
    ("/leak-detection-san-antonio/", "Water leak detection and repair", "High water bill, damp floors or low pressure. We track down the leak and fix it, including tunnel work under slabs.", "pressure-gauge", "Pressure gauge on an outdoor hose bib during a water pressure test"),
    ("/emergency-plumber-san-antonio/", "Burst pipes and urgent repairs", f"Water where it should not be? Call us right away during business hours, {B['hours']}.", "tunnel", "Plumber crawling through a tunnel under a slab to reach a broken pipe"),
]

def home():
    rows = "".join(f'''<li class="svc">
  <a href="{h}">
    {pic(img, alt, sizes="(min-width: 960px) 220px, 34vw", cls="svc-img")}
    <div class="svc-txt"><h3>{t}</h3><p>{d}</p><span class="svc-more">See {t.split(" and ")[0].lower()} details</span></div>
  </a></li>''' for h, t, d, img, alt in SERVICES)

    gallery = [
        ("camera-pipe", "Sewer camera inspection showing the inside of a drain line"),
        ("slab-roughin", "Under slab plumbing laid out before a concrete pour"),
        ("water-softener", "Water treatment system installed in a utility closet"),
        ("faucet-brushed", "Newly installed brushed nickel kitchen faucet"),
        ("meter-line", "New water service line connected at the meter box"),
        ("under-sink", "New kitchen sink drain and trap under the counter"),
        ("trench-dig", "JQ Plumbing plumber digging to reach a buried line"),
        ("roof-vent", "Plumber running a camera down a roof vent stack"),
    ]
    gal = "".join(f'<figure>{pic(n, a, sizes="(min-width: 960px) 25vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in gallery)

    if REVIEWS:
        def card(r):
            paras = [esc(x) for x in r["text"].split("\n\n")]
            more = "".join(f"<p>{x}</p>" for x in paras[1:])
            more = f'<details class="rev-more"><summary>Read full review</summary>{more}</details>' if more else ""
            return (f'<blockquote class="review"><div class="stars" role="img" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
                    f'<p>{paras[0]}</p>{more}<footer>{esc(r["name"])}, Google review</footer></blockquote>')
        cards = "".join(card(r) for r in REVIEWS)
        reviews = f'''<section class="reviews" id="reviews" aria-labelledby="rev-h"><div class="wrap">
<h2 id="rev-h">What customers say</h2><p class="rev-sub">Real reviews from our customers on Google, word for word.</p><div class="review-list">{cards}</div>
<p><a class="btn btn-ghost" href="{B["maps"]}" target="_blank" rel="noopener">Read all our reviews on Google</a></p></div></section>'''
    else:
        reviews = f'''<section class="reviews" id="reviews" aria-labelledby="rev-h"><div class="wrap reviews-empty">
<h2 id="rev-h">See what your neighbors say</h2>
<p>Our reviews come straight from customers on Google.</p>
<a class="btn btn-ghost" href="{B["maps"]}" target="_blank" rel="noopener">Read our Google reviews</a></div></section>'''

    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

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
        <a class="btn btn-ghost-light btn-lg" href="#estimate">Get a free estimate</a>
      </div>
    </div>
    <figure class="hero-photo">
      {pic("hero-tankless", "JQ Plumbing plumbers working on a water heater at a San Antonio home", sizes="(min-width: 960px) 40vw, 100vw", eager=True)}
      <figcaption>Our crew on a water heater job in San Antonio</figcaption>
    </figure>
  </div>
</section>
{facts_strip()}
<section class="services" id="services" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="svc-h">Plumbing services</h2>
      <p>Residential and commercial work across San Antonio. Fixture replacement, general repairs and tunnel work too.</p>
    </div>
    <ul class="svc-list">{rows}</ul>
  </div>
</section>
<section class="about" id="about" aria-labelledby="about-h">
  <div class="wrap about-grid">
    <figure class="about-photo">{pic("jon", f"{B['owner']}, owner of JQ Plumbing LLC", sizes="(min-width: 960px) 34vw, 100vw")}</figure>
    <div class="about-copy">
      <h2 id="about-h">Local, family owned, and here for the long run</h2>
      <p>JQ Plumbing is a local, family owned company. {B["owner"]} and his wife own the business, and our employees are family men too. Jonathan is a licensed plumber with {B["years"]} years of experience.</p>
      <p>We are focused on giving real value and the best customer experience possible. When you call, you get plumbers who are honest, trustworthy, skilled and reliable, and giving back to the community is important to us.</p>
      <ul class="ticks">
        <li>{ICON["check"]}Fully licensed and insured, Texas license {B["license"]}</li>
        <li>{ICON["check"]}Licensed plumbers, fingerprint background checked</li>
        <li>{ICON["check"]}Residential and commercial service</li>
        <li>{ICON["check"]}Manufacturer warranty on all parts, plus 90 days to 1 year on workmanship</li>
        <li>{ICON["check"]}Free estimates within city limits</li>
        <li>{ICON["check"]}Military, first responder and teacher discount with valid ID</li>
      </ul>
    </div>
  </div>
</section>
<section class="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="work-h">Recent jobs</h2><p>Real photos from our job sites. No stock pictures.</p></div>
    <div class="gallery">{gal}</div>
  </div>
</section>
{reviews}
<section class="area" id="area" aria-labelledby="area-h">
  <div class="wrap area-grid">
    <div>
      <h2 id="area-h">Serving San Antonio and surrounding areas</h2>
      <p>We work throughout San Antonio, TX and nearby communities. Estimates are free within city limits. Not sure if we cover your street? Give us a call.</p>
      <ul class="towns">{"".join(f"<li>{a}</li>" for a in AREAS)}</ul>
      <p class="muted">Hours: {B["hours"]}. {B["weekends"]}</p>
      {tel("area", "btn btn-call", ICON["phone"] + "<span>" + B["phone_display"] + "</span>")}
    </div>
    <div class="faq">
      <h2 class="faq-h">Common questions</h2>
      {faq}
    </div>
  </div>
</section>
{form_block()}'''
    page("/", "Licensed Plumber in San Antonio, TX | JQ Plumbing LLC",
         f"Licensed, insured, family owned plumbers in San Antonio. Drains, water heaters, leaks and repairs. Free estimates in city limits. Call {B['phone_display']}.",
         body, [BUSINESS_SCHEMA, faq_schema()])

# ---------------------------------------------------------------- service pages
def service_page(p):
    lists = "".join(f'<li>{ICON["check"]}{i}</li>' for i in p["handle"])
    signs = "".join(f"<li>{s}</li>" for s in p["signs"])
    extra = p.get("extra", "")
    photos = "".join(f'<figure>{pic(n, a, sizes="(min-width: 960px) 30vw, 50vw")}<figcaption>{a}</figcaption></figure>' for n, a in p["photos"])
    others = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, *_ in SERVICES if h != p["path"])
    body = f'''<section class="hero hero-svc">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span>{p["crumb"]}</span></nav>
      <h1>{p["h1"]}</h1>
      <p class="hero-sub">{p["intro"]}</p>
      <div class="hero-call">
        {tel("hero_number", "bignum", B["phone_display"])}
        <p class="hero-call-note">{ICON["clock"]}<span>Tap to call. Open {B["hours"]}.</span></p>
      </div>
      <div class="hero-actions">
        {tel("hero_button", "btn btn-call btn-lg", ICON["phone"] + "<span>Call now</span>")}
        <a class="btn btn-ghost-light btn-lg" href="#estimate">Get a free estimate</a>
      </div>
    </div>
    <figure class="hero-photo">{pic(p["hero"][0], p["hero"][1], sizes="(min-width: 960px) 40vw, 100vw", eager=True)}</figure>
  </div>
</section>
{facts_strip()}
<section class="detail">
  <div class="wrap detail-grid">
    <div>
      <h2>{p["handle_h"]}</h2>
      <ul class="ticks">{lists}</ul>
      {extra}
    </div>
    <aside class="signs">
      <h2>{p["signs_h"]}</h2>
      <ul>{signs}</ul>
      <p>{p["signs_cta"]}</p>
      {tel("signs_box", "btn btn-call btn-block", ICON["phone"] + "<span>Call " + B["phone_display"] + "</span>")}
    </aside>
  </div>
</section>
<section class="work">
  <div class="wrap">
    <div class="sec-head"><h2>From our job sites</h2></div>
    <div class="gallery gallery-3">{photos}</div>
  </div>
</section>
{form_block(preselect=p["select"])}
<section class="more"><div class="wrap"><h2>Other services</h2><ul class="more-list">{others}</ul></div></section>'''
    page(p["path"], p["title"], p["desc"], body,
         [BUSINESS_SCHEMA, service_schema(p["crumb"], p["path"], p["desc"]), crumbs(p["crumb"], p["path"])])

PAGES = [
    {
        "path": "/drain-cleaning-san-antonio/",
        "crumb": "Drain cleaning and sewer camera inspection",
        "title": "Drain Cleaning and Camera Inspection in San Antonio | JQ Plumbing",
        "desc": f"Clogged drain or sewer backup in San Antonio? Licensed plumbers for drain cleaning and sewer camera inspections. Free estimates in city limits. Call {B['phone_display']}.",
        "h1": "Drain cleaning and sewer camera inspection in San Antonio",
        "intro": "Slow sinks, backed up toilets, or a main line that keeps clogging. We clear the drain and, when it makes sense, put a camera in the line so you can see exactly what is causing it.",
        "hero": ("drain-machine", "Drain cleaning machine clearing a commercial restroom drain in San Antonio"),
        "handle_h": "What we handle",
        "handle": ["Kitchen, bathroom, shower and tub drains", "Toilet clogs and backups", "Main sewer line clogs", "Sewer camera inspections", "Residential and commercial drains"],
        "signs_h": "Signs it is time to call",
        "signs": ["Water draining slowly or not at all", "Gurgling sounds from drains or toilets", "Sewage smell inside or outside the house", "More than one fixture backing up at the same time"],
        "signs_cta": "More than one drain backing up usually points to the main line. Call before it overflows.",
        "photos": [("camera-pipe", "Camera view inside a drain line during an inspection"), ("bathroom-drain", "Drain machine set up to clear a shower drain"), ("camera-pipe-2", "Sewer camera monitor showing the inside of a pipe")],
        "select": "Drain cleaning or clog",
    },
    {
        "path": "/water-heater-repair-san-antonio/",
        "crumb": "Water heater repair and installation",
        "title": "Water Heater Repair and Installation in San Antonio | JQ Plumbing",
        "desc": f"No hot water? Licensed San Antonio plumbers for water heater repairs and installs, plus water treatment systems. Free estimates in city limits. Call {B['phone_display']}.",
        "h1": "Water heater repair and installation in San Antonio",
        "intro": "Cold showers, a leaking tank, or a heater that is near the end of its life. We repair and install water heaters, and we install water treatment systems too.",
        "hero": ("water-heater-team", "JQ Plumbing team working on a water heater at a home"),
        "handle_h": "What we handle",
        "handle": ["Water heater repairs", "Water heater replacement and installation", "Water treatment and softener systems", "Residential and commercial units"],
        "signs_h": "Signs your water heater needs help",
        "signs": ["No hot water, or it runs out fast", "Water pooling around the base of the tank", "Rusty or discolored hot water", "Popping or rumbling sounds from the tank"],
        "signs_cta": "A leaking tank can get worse quickly. Turn off the water supply to the heater and give us a call.",
        "photos": [("water-softener", "Water treatment system installed in a utility closet"), ("softener-open", "Control panel of a newly installed water softener"), ("hero-tankless", "JQ Plumbing crew working on a water heater")],
        "select": "Water heater",
    },
    {
        "path": "/leak-detection-san-antonio/",
        "crumb": "Water leak detection and repair",
        "title": "Water Leak Detection and Repair in San Antonio | JQ Plumbing",
        "desc": f"Hidden water leak in San Antonio? Licensed plumbers who find and fix leaks, including under slab tunnel work. Free estimates in city limits. Call {B['phone_display']}.",
        "h1": "Water leak detection and repair in San Antonio",
        "intro": "A high water bill or a damp spot that will not dry usually means water is going somewhere it should not. We find the leak and repair it.",
        "hero": ("pressure-gauge", "Water pressure gauge on an outdoor spigot during a leak test"),
        "handle_h": "What we handle",
        "handle": ["Finding hidden water leaks", "Water line and pipe repairs", "Pressure testing", "Water service lines at the meter", "Tunnel work to reach pipes under a slab"],
        "signs_h": "Signs you may have a leak",
        "signs": ["Water bill higher than usual with no change in use", "Water meter moving while every tap is off", "Damp floors, walls or ceilings", "Low water pressure", "Sound of running water when nothing is on"],
        "signs_cta": "The longer a leak runs, the more it costs. Call us and we will track it down.",
        "photos": [("meter-line", "New water line connected at the meter box"), ("tunnel", "Plumber in a tunnel under a slab reaching a broken pipe"), ("gas-gauge", "Pressure test gauge on a line")],
        "select": "Water leak",
    },
    {
        "path": "/emergency-plumber-san-antonio/",
        "crumb": "Burst pipes and urgent repairs",
        "title": "Burst Pipe and Urgent Plumbing Repair in San Antonio | JQ Plumbing",
        "desc": f"Burst pipe or active leak in San Antonio? Licensed, insured local plumbers for urgent repairs, weekdays and weekend emergencies. Call {B['phone_display']}.",
        "h1": "Burst pipe or urgent plumbing problem in San Antonio?",
        "intro": f"Water spraying, flooding, or a line that just broke. Call us right away. We are open {B['hours']}, and weekends are for scheduled and emergency work.",
        "hero": ("tunnel", "Plumber in a tunnel under a slab repairing a broken pipe"),
        "handle_h": "What we handle",
        "handle": ["Burst and broken pipes", "Active leaks and water line breaks", "Backed up drains and sewer lines", "Leaking water heaters", "Residential and commercial properties"],
        "signs_h": "What to do right now",
        "signs": ["Shut off your main water valve. It is usually near the street or where the line enters the house.", "If the water heater is leaking, turn off its water supply and power or gas.", "Move valuables and electronics away from the water.", "Call us and tell us what you see."],
        "signs_cta": f"Our hours are {B['hours']}. The earlier you call, the sooner we can get to you.",
        "photos": [("trench-dig", "Plumber digging to reach a broken water line"), ("sewer-trench", "Open trench for a sewer line repair"), ("yard-cleanout", "New cleanout caps installed in a front yard")],
        "select": "Burst pipe or urgent repair",
        "extra": f'<p class="note">{ICON["clock"]}<span>We are not a 24 hour service. Our hours are {B["hours"]}. {B["weekends"]}</span></p>',
    },
]

def privacy():
    body = f'''<section class="legal"><div class="wrap narrow">
<h1>Privacy policy</h1>
<p>This policy explains what information {B["name"]} collects through this website and how we use it.</p>
<h2>Information you send us</h2>
<p>When you fill out our estimate form we collect what you enter, such as your name, phone number, email, ZIP code and a description of your plumbing problem. We use it only to respond to your request and provide our services. We do not sell your information.</p>
<h2>Analytics and advertising</h2>
<p>We use Google Analytics and Google Ads to understand how visitors use our site and to measure calls and form requests from our ads. These services may use cookies to collect information such as pages visited and the device used. You can learn how Google uses this data at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">policies.google.com/technologies/partner-sites</a> and opt out of personalized ads at <a href="https://adssettings.google.com" rel="noopener" target="_blank">adssettings.google.com</a>.</p>
<h2>Contact</h2>
<p>Questions about this policy? Email <a href="mailto:{B["email"]}">{B["email"]}</a> or call {tel("privacy", "", B["phone_display"])}.</p>
</div></section>'''
    page("/privacy/", "Privacy Policy | JQ Plumbing LLC", f"Privacy policy for {B['name']}, a licensed plumbing company in San Antonio, TX.", body)

def not_found():
    body = f'''<section class="legal"><div class="wrap narrow">
<h1>That page is not here</h1>
<p>The link may be old. Head back to the <a href="/">home page</a>, or call us at {tel("404", "", B["phone_display"])}.</p></div></section>'''
    out = page("/404-tmp/", "Page not found | JQ Plumbing LLC", "Page not found.", body)
    os.replace(out, os.path.join(DIST, "404.html")); os.rmdir(os.path.dirname(out))

def extras():
    urls = ["/", "/drain-cleaning-san-antonio/", "/water-heater-repair-san-antonio/", "/leak-detection-san-antonio/", "/emergency-plumber-san-antonio/", "/privacy/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{B['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {B['url']}/sitemap.xml\n")

if __name__ == "__main__":
    home()
    for p in PAGES:
        service_page(p)
    privacy()
    not_found()
    extras()
    print("built", DIST)
