#!/usr/bin/env python3
"""
Static portfolio site generator.

Edit content.py with your info, then run:
    python3 generate_site.py

Output lands in ./output/ — open output/index.html in a browser,
or serve it with:  python3 -m http.server --directory output
"""
import shutil
from pathlib import Path
from content import CONFIG

ROOT = Path(__file__).parent
OUT = ROOT / "output"


def grid_guides(cols=12):
    return '<div class="grid-guides" aria-hidden="true">' + "<span></span>" * cols + "</div>"


def build_nav():
    links = "\n".join(
        f'<li><a href="{l["href"]}">{l["label"]}</a></li>' for l in CONFIG["nav"]
    )
    return f"""
<nav class="nav">
  <a href="#top" class="nav-logo">{CONFIG["name"].split()[0]}<span>.</span></a>
  <ul class="nav-links">
    {links}
  </ul>
  <a href="#contact" class="nav-cta">Let's talk</a>
  <button class="nav-toggle" aria-label="Toggle menu">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
</nav>
"""


def build_hero():
    first, *rest = CONFIG["name"].split(" ", 1)
    last = rest[0] if rest else ""
    return f"""
<header class="hero" id="top">
  {grid_guides()}
  <div class="hero-coords">N 37.77 &middot; W 122.41 &middot; {CONFIG["location"].upper()}</div>
  <div class="hero-eyebrow eyebrow">A {CONFIG["title"].upper()}</div>
  <h1 class="hero-name">{first} <em>{last}</em>.</h1>
  <div class="hero-bottom">
    <p class="hero-tagline">{CONFIG["tagline"]}</p>
    <div class="hero-scroll"><span class="dot"></span> Scroll to explore</div>
  </div>
</header>
"""


def build_stats():
    stats = "\n".join(
        f"""<div class="stat">
      <div class="stat-number">{s['number']}</div>
      <div class="stat-label">{s['label']}</div>
    </div>"""
        for s in CONFIG["stats"]
    )
    return f'<section class="stats reveal">{stats}</section>'


def build_about():
    creds = "\n".join(
        f"""<div class="credential">
      <div class="credential-year">{c['year']}</div>
      <div>
        <div class="credential-title">{c['title']}</div>
        <div class="credential-org">{c['org']}</div>
        <div class="credential-desc">{c['desc']}</div>
      </div>
    </div>"""
        for c in CONFIG["credentials"]
    )
    return f"""
<section class="section" id="about">
  {grid_guides()}
  <div class="section-head reveal">
    <div>
      <div class="eyebrow">More about me</div>
      <h2 class="section-title">Credentials</h2>
    </div>
    <div class="section-count">01 / 05</div>
  </div>
  <div class="about-grid reveal">
    <p class="about-bio">{CONFIG['about_bio']}</p>
    <div class="about-list">
      {creds}
    </div>
  </div>
</section>
"""


def build_work():
    projects = "\n".join(
        f"""<a class="project reveal" href="#">
      <div class="project-code">{p['code']}</div>
      <div class="project-main">
        <div class="project-title">{p['title']}<span class="project-arrow">&#8599;</span></div>
        <div class="project-desc">{p['desc']}</div>
      </div>
      <div class="project-cat">{p['category']}</div>
    </a>"""
        for p in CONFIG["projects"]
    )
    return f"""
<section class="section" id="work">
  {grid_guides()}
  <div class="section-head reveal">
    <div>
      <div class="eyebrow">Showcase</div>
      <h2 class="section-title">Projects</h2>
    </div>
    <div class="section-count">02 / 05</div>
  </div>
  <div class="work-list">
    {projects}
  </div>
</section>
"""


def build_services():
    services = "\n".join(
        f"""<div class="service reveal">
      <div class="service-num">{s['num']}</div>
      <div class="service-title">{s['title']}</div>
      <div class="service-desc">{s['desc']}</div>
    </div>"""
        for s in CONFIG["services"]
    )
    return f"""
<section class="section" id="services">
  {grid_guides()}
  <div class="section-head reveal">
    <div>
      <div class="eyebrow">Specialization</div>
      <h2 class="section-title">Services Offering</h2>
    </div>
    <div class="section-count">03 / 05</div>
  </div>
  <div class="services-grid">
    {services}
  </div>
</section>
"""


def build_contact():
    socials = "\n".join(
        f'<a href="{s["href"]}">{s["label"]}</a>' for s in CONFIG["socials"]
    )
    return f"""
<section class="section contact" id="contact">
  {grid_guides()}
  <div class="contact-inner reveal">
    <div class="eyebrow">Stay with me</div>
    <h2 class="contact-title">Let's <span class="accent">work</span> together.</h2>
    <a class="contact-email" href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>
    <div class="contact-meta">
      <div class="contact-meta-block">
        <div class="eyebrow">Phone</div>
        <div>{CONFIG['phone']}</div>
      </div>
      <div class="contact-meta-block">
        <div class="eyebrow">Based in</div>
        <div>{CONFIG['location']}</div>
      </div>
      <div class="contact-meta-block">
        <div class="eyebrow">Profiles</div>
        {socials}
      </div>
    </div>
  </div>
</section>
"""


def build_footer():
    return f"""
<footer class="footer">
  <span>&copy; <span id="year"></span> {CONFIG['name']}. All rights reserved.</span>
  <a class="footer-top" href="#top" aria-label="Back to top">&uarr;</a>
</footer>
"""


def build_html():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{CONFIG['name']} — {CONFIG['title']}</title>
<meta name="description" content="{CONFIG['name']} is a {CONFIG['title'].lower()} based in {CONFIG['location']}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{build_nav()}
<main>
{build_hero()}
{build_stats()}
{build_about()}
{build_work()}
{build_services()}
{build_contact()}
</main>
{build_footer()}
<script src="script.js"></script>
</body>
</html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(build_html(), encoding="utf-8")
    shutil.copy(ROOT / "styles_template.css", OUT / "styles.css")
    shutil.copy(ROOT / "script_template.js", OUT / "script.js")
    print(f"Site generated in {OUT}/")
    print("Open output/index.html in a browser, or run:")
    print("    python3 -m http.server --directory output")


if __name__ == "__main__":
    main()
