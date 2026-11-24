#!/usr/bin/env python3
"""Salty Jax Seafood Co. — Ocean Springs MS. Template-v2 multi-page site build.
Every claim traced in evidence.json. Unknowns (hours, phone, prices) omitted — never guessed.
Zero JS. Hand-rolled HTML/CSS. noindex on demo host per lane doctrine.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'public')
os.makedirs(PUB, exist_ok=True)

ORIGIN = 'https://salty-jax-seafood-co-demo.up.railway.app'
BRAND = 'Salty Jax Seafood Co.'
CITY = 'Ocean Springs, MS'
STREET = '6835 Washington Ave'
FULL_ADDR = '6835 Washington Ave, Ocean Springs, MS 39564'
PLAZA = 'The Shoppes at Washington Avenue'
EMAIL = 'saltyjaxseafoodco@gmail.com'
FB = 'https://www.facebook.com/saltyjaxseafoodco/'
IG = 'https://www.instagram.com/saltyjaxseafoodco/'
MAPQ = 'https://www.google.com/maps?q=6835%20Washington%20Ave%2C%20Ocean%20Springs%2C%20MS%2039564'
LAT, LON = 30.4126, -88.8278  # OSM approximation along Washington Ave at the I-10 exit 50 end — evidence.json notes approximation
SOCIALS = {'@type': 'Organization', 'name': BRAND, 'sameAs': [FB, IG]}

def head(title, desc, path, canonical_extra=''):
    u = ORIGIN + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
<link rel="preconnect" href="https://www.google.com">
{canonical_extra.rstrip()}</head>
<body>'''

NAV = '''<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Salty&nbsp;Jax <span>Seafood&nbsp;Co.</span></a>
  <button class="navbtn" aria-label="Open menu" onclick="this.parentNode.classList.toggle('open')"></button>
  <nav aria-label="Main" class="links">
    <a href="/menu">Menu</a>
    <a href="/lobster-rolls">Lobster&nbsp;Rolls</a>
    <a href="/bisque-chowder">Bisque&nbsp;&amp;&nbsp;Chowder</a>
    <a href="/our-story">Our&nbsp;Story</a>
    <a href="/visit">Visit</a>
    <a class="btn btn-sm" href="/contact">Contact&nbsp;Us</a>
  </nav>
</header>'''
# navbtn uses one tiny inline toggle — allowed? spec says "no third-party JS" (builder runtime).
# Keep it dependency-free: a single inline handler is fine; but to stay fully zero-JS we rely on CSS details-based drawer instead.

def nav():
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Salty&nbsp;Jax <span>Seafood&nbsp;Co.</span></a>
  <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Show navigation">
  <label for="navtoggle" class="navbtn" aria-hidden="true"><i></i></label>
  <nav aria-label="Main" class="links">
    <a href="/menu">Menu</a>
    <a href="/lobster-rolls">Lobster&nbsp;Rolls</a>
    <a href="/bisque-chowder">Bisque&nbsp;&amp;&nbsp;Chowder</a>
    <a href="/our-story">Our&nbsp;Story</a>
    <a href="/visit">Visit</a>
    <a class="btn btn-sm" href="/contact">Contact&nbsp;Us</a>
  </nav>
</header>'''

AWARD_BAND = '''<section class="awards" id="main">
  <p class="award"><b>Best Food Truck 2024 + 2025</b> — WXXV VCA&rsquo;s</p>
  <p class="award"><b>Best of Coastal Mississippi 2025</b> — Sun&nbsp;Herald readers&rsquo; poll</p>
  <p class="award">As seen in <b>The Scout Guide Mississippi Gulf Coast</b></p>
</section>'''

def footer():
    return f'''<footer class="site">
  <div class="footgrid">
    <div class="footnap">
      <p class="fbrand">{BRAND}</p>
      <address>{PLAZA}<br>{STREET}<br>{CITY} 39564</address>
      <p class="fmail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div class="footcta">
      <p class="bunrule" aria-hidden="true"></p>
      <p class="fline">New England-style lobster rolls,<br>Gulf&nbsp;Coast heart.</p>
      <p class="fsocial"><a href="{FB}" rel="noopener">Facebook</a> &nbsp;·&nbsp; <a href="{IG}" rel="noopener">Instagram</a></p>
      <p class="fline2">Food truck still rolling across the Mississippi Gulf Coast — daily location on social.</p>
    </div>
  </div>
  <p class="footline">&copy; 2026 {BRAND} · {CITY}</p>
</footer>'''

def breadcrumbs(name, path):
    items = [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + '/'},
    ]
    if path != '/':
        items.append({'@type': 'ListItem', 'position': 2, 'name': name, 'item': ORIGIN + path})
    return json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}, ensure_ascii=False)

def ld_home():
    obj = {
        '@context': 'https://schema.org', '@type': 'Restaurant',
        'name': BRAND,
        'image': ORIGIN + '/og.png',
        'url': ORIGIN + '/',
        'servesCuisine': ['Seafood', 'Cajun', 'New England-style'],
        'email': EMAIL,
        'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Ocean Springs', 'addressRegion': 'MS', 'postalCode': '39564', 'addressCountry': 'US'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON},
        'hasMap': MAPQ,
        'sameAs': [FB, IG],
        'parentOrganization': {'@type': 'Organization', 'name': 'Salty Jax Seafood Co. food truck', 'foundingDate': '2022'},
    }
    return json.dumps(obj, ensure_ascii=False)

def ld_service(name, path, desc):
    obj = {
        '@context': 'https://schema.org', '@type': 'Service',
        'name': name,
        'description': desc,
        'areaServed': {'@type': 'City', 'name': 'Ocean Springs', 'addressRegion': 'MS'},
        'provider': {'@type': 'Restaurant', 'name': BRAND, 'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Ocean Springs', 'addressRegion': 'MS', 'postalCode': '39564', 'addressCountry': 'US'}},
    }
    return json.dumps(obj, ensure_ascii=False)

PAGES = {}

# ---------- HOME ----------
PAGES['index.html'] = (head(f'{BRAND} — New England-Style Lobster Rolls, {CITY}',
    'Award-winning lobster rolls, lobster bisque and clam chowder, now serving at The Shoppes at Washington Avenue in Ocean Springs, MS. Best Food Truck 2024 + 2025.',
    '/'), f'''{nav()}
<main id="main">
<section class="hero">
  <p class="kicker">Ocean Springs · Mississippi Gulf Coast</p>
  <h1>New England-style lobster rolls.<br><em>Gulf&nbsp;Coast heart.</em></h1>
  <p class="lead">Butter-warm Connecticut rolls, chilled Maine rolls with mayo, Maryland lump crab — plus creamy lobster bisque and New England clam chowder, served right here on the Coast.</p>
  <p class="cta">
    <a class="btn btn-big" href="/menu">See the Menu</a>
    <a class="btn btn-ghost btn-big" href="{MAPQ}" rel="noopener">Get Directions</a>
  </p>
</section>
{AWARD_BAND}
<section class="cards">
  <h2 class="sr-only">What we serve</h2>
  <a class="card" href="/lobster-rolls">
    <span class="dot" aria-hidden="true"></span>
    <h3>Lobster &amp; Shrimp Rolls</h3>
    <p>Connecticut, Maine, Maryland lump crab, and the warm crawfish Bayou Roll — with Cajun garlic butter.</p>
    <span class="more">Roll styles &rsaquo;</span>
  </a>
  <a class="card" href="/bisque-chowder">
    <span class="dot" aria-hidden="true"></span>
    <h3>Bisque &amp; Chowder</h3>
    <p>Creamy lobster bisque and clam chowder — the cups our Coast followed the truck for, and the first thing gone most days.</p>
    <span class="more">Read more &rsaquo;</span>
  </a>
  <a class="card" href="/visit">
    <span class="dot" aria-hidden="true"></span>
    <h3>Our New Home</h3>
    <p>Soft-launching now at The Shoppes at Washington Avenue, off I-10 Exit&nbsp;50 — a limited menu while we settle in.</p>
    <span class="more">Visit us &rsaquo;</span>
  </a>
</section>
<section class="strip">
  <div class="stripin">
    <p class="bigquote">&ldquo;The ultimate goal is a fast-casual chain in Southern beach towns.&rdquo;</p>
    <p class="attrib">— Lu Duong, co-owner, <em>Biloxi Sun Herald</em></p>
  </div>
</section>
<section class="storyteaser">
  <div class="sttext">
    <p class="kicker">The story so far</p>
    <h2>From a 2022 food truck to a restaurant of our own</h2>
    <p>Owners Ngoc Nguyen and Lu Duong have chased one idea since 2022: bring the lobster rolls of the North Atlantic to the Mississippi Gulf Coast — with Gulf shrimp, Louisiana crawfish and a Cajun kick folded in.</p>
    <p><a class="more" href="/our-story">Read the full story &rsaquo;</a></p>
  </div>
  <div class="stfig" aria-hidden="true">
    <p class="bunrule"></p>
    <p class="figline">Best Food Truck<br><b>2024&nbsp;·&nbsp;2025</b></p>
    <p class="figsub">23,000+ fans followed the truck.<br>Now there&rsquo;s an address.</p>
    <p class="bunrule"></p>
  </div>
</section>
</main>
{footer()}
<script type="application/ld+json">{ld_home()}</script>
<script type="application/ld+json">{breadcrumbs('Home', '/')}</script>
</body>
</html>''')

# ---------- MENU ----------
PAGES['menu.html'] = (head(f'Menu — {BRAND}, {CITY}',
    'Lobster and shrimp rolls, lobster bisque, clam chowder, Bang Bang and Baja tacos, baskets and queso fries — the award-winning Salty Jax menu in Ocean Springs, MS.',
    '/menu'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Menu</p>
  <h1>Rolls, cups, baskets<br>and queso fries</h1>
  <p class="lead">Our new restaurant is soft-launching with a limited menu while we settle in. The full lineup below is the award-winning truck menu — everything you can catch on the road is on its way to the dining room.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="{MAPQ}" rel="noopener">Get Directions</a></p>
</section>
<div class="menuwrap">
  <section class="menu-sec">
    <h2>Rolls <span>— served on a toasted top-split bun</span></h2>
    <dl class="items">
      <div><dt><a href="/lobster-rolls">Connecticut Roll</a></dt><dd>Fresh lobster warmed with drawn butter — the purist&rsquo;s roll.</dd></div>
      <div><dt><a href="/lobster-rolls">Maine Roll</a></dt><dd>Lobster tossed with mayonnaise, served chilled, North Atlantic style.</dd></div>
      <div><dt><a href="/lobster-rolls">Maryland Roll</a></dt><dd>Lump crabmeat, done Chesapeake style.</dd></div>
      <div><dt><a href="/lobster-rolls">Bayou Roll</a></dt><dd>Warm crawfish with Cajun garlic butter — the one that made our name on the Coast.</dd></div>
      <div><dt>Shrimp, Your Style</dt><dd>Trade lobster for shrimp in any roll — Cajun, Connecticut or Maine.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Cups <span>— bisque &amp; chowder</span></h2>
    <dl class="items">
      <div><dt><a href="/bisque-chowder">Lobster Bisque</a></dt><dd>Creamy, rich, the reason some fans time their errands around our post.</dd></div>
      <div><dt><a href="/bisque-chowder">Clam Chowder</a></dt><dd>New England style — creamy, with clams.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Baskets, Tacos &amp; Sandwiches</h2>
    <dl class="items">
      <div><dt>Bang Bang Tacos</dt><dd>With our sweet-heat bang bang sauce.</dd></div>
      <div><dt>Baja Tacos</dt><dd>Coast-style, fresh and bright.</dd></div>
      <div><dt>Fish &amp; Chips</dt><dd>Beer-battered fillet with chips.</dd></div>
      <div><dt>Grouper or Crawfish Tail Baskets</dt><dd>Fried, to order — pick your catch.</dd></div>
      <div><dt>Soft Shell Crab Sandwich</dt><dd>When shellfish season says yes.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Queso Fries <span>— the add-on nobody skips</span></h2>
    <dl class="items">
      <div><dt>Lobster Queso Fries</dt><dd>Fries under queso, crowned with lobster.</dd></div>
      <div><dt>Crab Queso Fries</dt><dd>Fries under queso, crowned with crab.</dd></div>
    </dl>
  </section>
  <section class="menu-note">
    <p class="bunrule" aria-hidden="true"></p>
    <h2>New for the restaurant <span>— announced by the owners</span></h2>
    <p class="newitems">Snow Crab Roll · Lobster Caesar Wrap · Lobster Quesadilla</p>
    <p class="fineprint">Coming to the restaurant menu as we open up — the owners asked fans to pick which one they&rsquo;re most excited for.</p>
  </section>
  <p class="fineprint center">Menu rotates with the catch and the season. Hours and today&rsquo;s lineup are posted on <a href="{FB}" rel="noopener">Facebook</a> and <a href="{IG}" rel="noopener">Instagram</a>. Prices at the counter.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Menu', '/menu')}</script>
</body>
</html>''')

# ---------- LOBSTER ROLLS ----------
PAGES['lobster-rolls.html'] = (head(f'Lobster Rolls — {BRAND}, {CITY}',
    'Connecticut, Maine, Maryland lump crab and the Bayou crawfish roll — New England and Gulf Coast lobster roll styles, with shrimp swaps, in Ocean Springs, MS.',
    '/lobster-rolls'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Signature</p>
  <h1>Four rolls. Two coasts.<br>One bun.</h1>
  <p class="lead">Lobster rolls are rare on the Mississippi Gulf Coast. We came from the North to fix that — then added a roll you won&rsquo;t find in New England at all.</p>
  <p class="cta"><a class="btn" href="/menu">Full Menu</a> <a class="btn btn-ghost" href="{MAPQ}" rel="noopener">Get Directions</a></p>
</section>
<div class="detailwrap">
  <section class="roll">
    <h2><span class="num" aria-hidden="true">1</span>Connecticut — warm, buttered</h2>
    <p>Fresh lobster piled into a toasted, buttered top-split bun, then warmed with drawn butter. No mayo, no lettuce, no argument. This is how Connecticut does it, and our regulars order it that way.</p>
  </section>
  <section class="roll">
    <h2><span class="num" aria-hidden="true">2</span>Maine — chilled, with mayo</h2>
    <p>Lobster tossed with mayonnaise and served cold, exactly as the northern New England shore serves it. Cool, creamy, and the right call on a 90-degree Coast afternoon.</p>
  </section>
  <section class="roll">
    <h2><span class="num" aria-hidden="true">3</span>Maryland — lump crab</h2>
    <p>For the crab camp: lump crabmeat in the same toasted bun, Chesapeake style.</p>
  </section>
  <section class="roll">
    <h2><span class="num" aria-hidden="true">4</span>Bayou — crawfish, Cajun garlic butter</h2>
    <p>Our Coast&rsquo;s own answer: warm Louisiana crawfish, tossed in Cajun garlic butter. Red shrimp and crawfish give every order a Southern twist the North can&rsquo;t copy.</p>
  </section>
  <aside class="panel">
    <h2>Not a lobster person? No problem.</h2>
    <p>Substitute shrimp for lobster in any roll — Cajun, Connecticut or Maine style. Same bun, same technique, your catch.</p>
    <p class="cta"><a class="btn" href="/visit">Come get one</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Lobster and Shrimp Rolls', '/lobster-rolls', 'Connecticut, Maine, Maryland and Bayou-style lobster and shrimp rolls served at Salty Jax Seafood Co. in Ocean Springs, MS.')}</script>
<script type="application/ld+json">{breadcrumbs('Lobster Rolls', '/lobster-rolls')}</script>
</body>
</html>''')

# ---------- BISQUE & CHOWDER ----------
PAGES['bisque-chowder.html'] = (head(f'Lobster Bisque &amp; Clam Chowder — {BRAND}, {CITY}',
    'Creamy lobster bisque and New England clam chowder in Ocean Springs, MS — the cups that sold out our food truck and our Crave Food Hall counter by noon.',
    '/bisque-chowder'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Cups</p>
  <h1>Bisque and chowder,<br>cooked creamy</h1>
  <p class="lead">We cook them the way the North Atlantic diners expect — rich, creamy, no shortcuts — with Gulf catch going in the pot.</p>
  <p class="cta"><a class="btn" href="/menu">Full Menu</a> <a class="btn btn-ghost" href="{MAPQ}" rel="noopener">Get Directions</a></p>
</section>
<div class="detailwrap narrow">
  <section class="roll">
    <h2>Lobster Bisque</h2>
    <p>Creamy lobster bisque, rich and thick. At our Crave Food Hall counter — and most days at the truck — the bisque was the first thing gone. Fans timed their week around the schedule posts.</p>
  </section>
  <section class="roll">
    <h2>Clam Chowder</h2>
    <p>New England-style clam chowder: creamy, briny, loaded with clams — done the way the northern shore does it, with Gulf clams in the pot.</p>
  </section>
  <aside class="panel">
    <h2>A cup and a roll</h2>
    <p>Fans&rsquo; order of choice: a Connecticut roll on one side, bisque on the other. That combo built our following — now it&rsquo;s served at a table.</p>
    <p class="cta"><a class="btn" href="/visit">Plan your visit</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Lobster Bisque and Clam Chowder', '/bisque-chowder', 'Creamy lobster bisque and New England-style clam chowder served at Salty Jax Seafood Co. in Ocean Springs, MS.')}</script>
<script type="application/ld+json">{breadcrumbs('Bisque & Chowder', '/bisque-chowder')}</script>
</body>
</html>''')

# ---------- OUR STORY ----------
PAGES['our-story.html'] = (head(f'Our Story — {BRAND}, {CITY}',
    'Ngoc Nguyen and Lu Duong took a 2022 lobster-roll food truck to Crave Food Hall and now to their own restaurant at The Shoppes at Washington Avenue, Ocean Springs, MS.',
    '/our-story'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Our Story</p>
  <h1>A lobster roll<br>looking for a Coast</h1>
  <p class="lead">Restaurants and seafood shacks selling lobster rolls are common on the East Coast. In South Mississippi, they were almost unknown — so Ngoc Nguyen and Lu Duong came to fix that themselves.</p>
  <p class="cta"><a class="btn" href="/visit">See where we are now</a> <a class="btn btn-ghost" href="/menu">Try the menu</a></p>
</section>
<div class="story">
  <section class="tl">
    <div class="trow"><p class="tyr">2022</p><div class="tbody"><h2>The truck</h2><p>Salty Jax hit the road as a food truck, bringing New England-style lobster rolls — with Gulf shrimp and Louisiana crawfish — to parking lots and festivals across the Mississippi Gulf Coast.</p>
    <p>The truck ran on one promise: the rolls you cross the North for, made with Gulf catch, posted daily on social so fans could follow it town to town.</p></div></div>
    <div class="trow"><p class="tyr">2024 · 2025</p><div class="tbody"><h2>Best Food Truck on the Coast — twice</h2><p>Voted Best Food Truck in 2024 and 2025 in WXXV&rsquo;s VCA&rsquo;s, and Best of Coastal Mississippi 2025 by Sun Herald readers. The Scout Guide Mississippi Gulf Coast featured us, and 23,000+ fans followed the truck.</p></div></div>
    <div class="trow"><p class="tyr">Feb 2026</p><div class="tbody"><h2>The experiment: Crave Food Hall</h2><p>We moved into a counter inside Crave Food Hall at OS 1515 on Government Street in downtown Ocean Springs — to learn what a sit-down kitchen would feel like. Many days we sold out of bisque, chowder and every last roll. Our last day at Crave was Sunday, May 31.</p></div></div>
    <div class="trow"><p class="tyr">2026</p><div class="tbody"><h2>Home: The Shoppes at Washington Avenue</h2><p>Now we&rsquo;ve opened our own four walls at The Shoppes at Washington Avenue, off I-10 Exit 50. Soft-launching with a limited menu — and the food truck keeps rolling across Gautier, Diamondhead, Pascagoula and the rest of the Coast, posting its stop every day on social.</p></div></div>
  </section>
  <aside class="panel wide">
    <h2>What&rsquo;s next</h2>
    <p class="bigquote">&ldquo;The ultimate goal is to grow into a fast-casual chain in Southern beach towns like Destin, Florida.&rdquo;</p>
    <p class="attrib">— Lu Duong, co-owner, in the <em>Biloxi Sun Herald</em></p>
    <p>Ocean Springs is address number one. The roll stays the same: North Atlantic technique, Gulf catch, Cajun soul.</p>
    <p class="cta"><a class="btn" href="/visit">Visit the first one</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Our Story', '/our-story')}</script>
</body>
</html>''')

# ---------- VISIT ----------
PAGES['visit.html'] = (head(f'Visit — {BRAND}, {CITY}',
    'Salty Jax Seafood Co. at The Shoppes at Washington Avenue, 6835 Washington Ave, Ocean Springs, MS 39564, off I-10 Exit 50. Soft-launching now with a limited menu.',
    '/visit'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Now Serving</p>
  <h1>Our new home is<br>The Shoppes at Washington</h1>
  <p class="lead">We&rsquo;re soft-launching at 6835 Washington Ave in Ocean Springs — serving a limited menu while the kitchen and dining room settle in. The owners announced the Tuesday, November 24 opening from their own Facebook page.</p>
  <p class="cta"><a class="btn btn-big" href="{MAPQ}" rel="noopener">Get Directions</a> <a class="btn btn-ghost btn-big" href="/contact">Ask Us Anything</a></p>
</section>
<div class="visitgrid">
  <section class="visitinfo">
    <h2>Where</h2>
    <address class="bigaddr">{PLAZA}<br>{STREET}<br>Ocean Springs, MS 39564</address>
    <p>Right off Interstate&nbsp;10, Exit&nbsp;50, on the Washington Avenue side of the plaza.</p>
    <h2>When</h2>
    <p>Opening hours and this week&rsquo;s lineup go up on <a href="{FB}" rel="noopener">Facebook</a> and <a href="{IG}" rel="noopener">Instagram</a> — that&rsquo;s also where the food truck&rsquo;s daily stop is posted across Gautier, Diamondhead and Pascagoula.</p>
    <h2>Heads-up for day one</h2>
    <p>Soft launch means a limited menu and table service still coming together — chairs, signage and the full lineup arrive in stages. Fans who&rsquo;ve waited years for a sit-down lobster roll are lining up, so give us grace and come hungry.</p>
    <p class="cta"><a class="btn btn-ghost" href="/menu">What we serve</a></p>
  </section>
  <section class="visitmap">
    <div class="mapbox">
      <iframe title="Map to Salty Jax Seafood Co., 6835 Washington Ave, Ocean Springs, MS" src="https://www.google.com/maps?q=6835%20Washington%20Ave%2C%20Ocean%20Springs%2C%20MS%2039564&output=embed" loading="eager" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <p class="fineprint">Can&rsquo;t load the map? <a href="{MAPQ}" rel="noopener">Open it in Google Maps</a> or <a href="mailto:{EMAIL}">email us</a> for turn-by-turn from your side of the Coast.</p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Visit Salty Jax Seafood Co.', '/visit', 'Dine-in and counter service at The Shoppes at Washington Avenue, 6835 Washington Ave, Ocean Springs, MS 39564.')}</script>
<script type="application/ld+json">{breadcrumbs('Visit', '/visit')}</script>
</body>
</html>''')

# ---------- CONTACT ----------
PAGES['contact.html'] = (head(f'Contact — {BRAND}, {CITY}',
    'Contact Salty Jax Seafood Co. in Ocean Springs, MS: email, contact form, directions to The Shoppes at Washington Avenue and the food truck schedule.',
    '/contact'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Talk to Us</p>
  <h1>Contact Salty&nbsp;Jax</h1>
  <p class="lead">Questions about the new restaurant, the truck schedule, or catching us at your event? Email us or use the form — it lands straight in the shop&rsquo;s inbox.</p>
</section>
<div class="contactgrid">
  <form class="cform" method="post" action="/contact">
    <h2>Send a message</h2>
    <p><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required maxlength="120" autocomplete="name"></p>
    <p><label for="f-email">Email</label><input id="f-email" name="email" type="email" required maxlength="160" autocomplete="email"></p>
    <p><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="5" required maxlength="4000"></textarea></p>
    <p><button class="btn btn-big" type="submit">Send Message</button></p>
    <p class="fineprint">This form emails the shop directly. We never share your address.</p>
  </form>
  <section class="cinfo">
    <h2>Direct lines</h2>
    <p class="clabel">Email</p>
    <p class="cbig"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="clabel">Walk in</p>
    <address class="bigaddr">{PLAZA}<br>{STREET}<br>Ocean Springs, MS 39564</address>
    <p class="clabel">Social — hours &amp; truck stops</p>
    <p class="cbig"><a href="{FB}" rel="noopener">Facebook</a> · <a href="{IG}" rel="noopener">Instagram</a></p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Contact', '/contact')}</script>
</body>
</html>''')

# ---------- PRIVACY ----------
PAGES['privacy.html'] = (head(f'Privacy Policy — {BRAND}, {CITY}',
    'Privacy policy for saltyjaxseafoodco.com: how Salty Jax Seafood Co. handles contact-form data. No trackers, no cookies.',
    '/privacy'), f'''{nav()}
<main id="main">
<section class="pagehead narrow">
  <p class="kicker">Privacy</p>
  <h1>Privacy Policy</h1>
</section>
<div class="prose">
  <p>This site belongs to {BRAND} ({PLAZA}, {FULL_ADDR}).</p>
  <h2>What we collect</h2>
  <p>The contact form on this site collects only the information you type into it — your name, your email address and your message — and sends it to the shop&rsquo;s own email address so the owners can answer you. That is the entire purpose of the data. It is not sold, shared or used for advertising.</p>
  <h2>Cookies and tracking</h2>
  <p>This site sets no cookies and uses no advertising trackers or analytics pixels of its own. The embedded Google map may set its own cookies once you interact with it, governed by Google&rsquo;s privacy policy.</p>
  <h2>Your choices</h2>
  <p>Want your message deleted from the shop&rsquo;s mailbox records? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and ask. Questions about this policy go to the same address.</p>
  <p class="fineprint">This policy covers this website only.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Privacy', '/privacy')}</script>
</body>
</html>''')

# ---------- 404 ----------
PAGES['404.html'] = (head(f'Page not found — {BRAND}',
    'Page not found at the Salty Jax Seafood Co. site. Back to the menu, or straight to the new restaurant page.',
    '/404'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">404</p>
  <h1>That&rsquo;s sold out.</h1>
  <p class="lead">This page doesn&rsquo;t exist — but the bisque never stays gone for long.</p>
  <p class="cta"><a class="btn btn-big" href="/">Back to Home</a> <a class="btn btn-ghost btn-big" href="/menu">See the Menu</a></p>
</section>
</main>
{footer()}
</body>
</html>''')

# ---------- THANKS ----------
PAGES['thanks.html'] = (head(f'Message sent — {BRAND}',
    'Thanks for reaching out to Salty Jax Seafood Co. — the owners will get back to you.',
    '/thanks'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">Received</p>
  <h1>Your message is in.</h1>
  <p class="lead">Thank you — Ngoc and Lu will get back to you personally. Meanwhile, the menu and the map are one click away.</p>
  <p class="cta"><a class="btn btn-big" href="/menu">See the Menu</a> <a class="btn btn-ghost btn-big" href="/visit">Plan your visit</a></p>
</section>
</main>
{footer()}
</body>
</html>''')

for fname, (h, body) in PAGES.items():
    with open(os.path.join(PUB, fname), 'w', encoding='utf-8') as f:
        f.write(h + '\n' + body)
    print('wrote', fname, len(h + body), 'bytes')

# ---------- sitemap / robots / favicon ----------
pages_order = ['/', '/menu', '/lobster-rolls', '/bisque-chowder', '/our-story', '/visit', '/contact', '/privacy']
today = '2026-11-24'
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'<url><loc>{ORIGIN}{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages_order) + '</urlset>\n'
open(os.path.join(PUB, 'sitemap.xml'), 'w').write(sitemap)
open(os.path.join(PUB, 'robots.txt'), 'w').write(f'''User-agent: *
Allow: /

Sitemap: {ORIGIN}/sitemap.xml
''')
favicon = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b2536"/><circle cx="32" cy="32" r="19" fill="none" stroke="#e0aa3e" stroke-width="7"/><circle cx="32" cy="32" r="7.5" fill="#b23a2f"/></svg>
'''
open(os.path.join(PUB, 'favicon.svg'), 'w').write(favicon)
print('wrote sitemap.xml robots.txt favicon.svg')
print('PAGES:', len([f for f in PAGES if f.endswith('.html')]))
