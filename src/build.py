"""Build the static e-portfolio: content/*.md -> site/*.html via pandoc."""
import html, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).parent
SITE = ROOT.parent
GROUPS = [
    ("Overview", [("index", "Home", ""), ("concepts", "Key concepts", ""), ("references", "References", "")]),
    ("Project", [("final-project", "Design vs implementation", ""), ("team", "Team work", "")]),
    ("Reflection", [("case-studies", "Case studies", ""), ("reflection", "Final reflection", ""),
                    ("forums", "Discussions", "")]),
    ("Units", [(f"unit{i}", None, str(i)) for i in range(1, 13)]),
]
TITLES = {md.stem: md.read_text().partition("\n")[0].removeprefix("# ").strip()
          for md in (ROOT / "content").glob("*.md")}
ORDER = [stem for _, items in GROUPS for stem, _, _ in items]


def label(stem, text):
    return text or TITLES[stem].split(": ", 1)[-1]


def eyebrow(stem):
    if stem.startswith("unit"):
        return f"Unit {stem[4:]}"
    return next(g for g, items in GROUPS if stem in [s for s, _, _ in items])


def nav_html(current):
    out = []
    for group, items in GROUPS:
        links = "".join(
            f'<a href="{s}.html"{" class=\"active\" aria-current=\"page\"" if s == current else ""}>'
            f'{f"<span class=num>{n}</span>" if n else ""}<span>{html.escape(label(s, t))}</span></a>'
            for s, t, n in items)
        out.append(f'<div class="nav-group"><h4>{group}</h4>{links}</div>')
    return "".join(out)


def pager(current):
    i = ORDER.index(current)
    parts = []
    if i > 0:
        p = ORDER[i - 1]
        parts.append(f'<a class="prev" href="{p}.html"><small>Previous</small>{html.escape(TITLES[p])}</a>')
    if i < len(ORDER) - 1:
        n = ORDER[i + 1]
        parts.append(f'<a class="next" href="{n}.html"><small>Next</small>{html.escape(TITLES[n])}</a>')
    return f'<nav class="pager">{"".join(parts)}</nav>'


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Intelligent Agents E-Portfolio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<link rel="stylesheet" href="style.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <a class="brand" href="index.html"><span class="mark">IA</span><span><span class="name">Ruwan Perera</span><span class="sub">Intelligent Agents e-portfolio</span></span></a>
  <button class="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">Menu</button>
  <nav>{nav}</nav>
</aside>
<main class="content">
<header class="page-head"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1></header>
{body}
{pager}
<footer class="footer"><span>Ruwan Perera · MSc Artificial Intelligence · University of Essex Online</span>
<button class="theme-btn" onclick="var d=document.documentElement,n=(d.dataset.theme||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))==='dark'?'light':'dark';d.dataset.theme=n;try{{localStorage.setItem('theme',n)}}catch(e){{}}">Toggle theme</button></footer>
</main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll()</script>
</body>
</html>
"""


def code_block(match):
    rel = match.group(1)
    text = (SITE / "code" / rel).read_text()
    lang = "python" if rel.endswith(".py") else "text"
    return (f'<details><summary>Show {html.escape(rel)}</summary>'
            f'<pre><code class="language-{lang}">{html.escape(text)}</code></pre></details>'
            f'<p class="download">Download: <a href="code/{rel}">{html.escape(rel)}</a></p>')


for md in sorted((ROOT / "content").glob("*.md")):
    raw = md.read_text()
    title, _, body_md = raw.partition("\n")
    title = title.removeprefix("# ").strip()
    body = subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"],
                          input=body_md, capture_output=True, text=True, check=True).stdout
    body = re.sub(r"<p>\{\{code:([^}]+)\}\}</p>", code_block, body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    (SITE / f"{md.stem}.html").write_text(TEMPLATE.format(title=html.escape(title), nav=nav_html(md.stem), body=body,
                                                                eyebrow=eyebrow(md.stem), pager=pager(md.stem)))
    print("built", md.stem)
