#!/usr/bin/env python3
"""Gera o site estático do Catholicam a partir de _src/site.html.

Cada seção (<section class="view" data-view="...">) vira uma página própria:
  inicio -> /index.html ; demais -> /<secao>/index.html
Também gera sitemap.xml e robots.txt. Rode:  python3 build.py
Edite sempre _src/site.html, nunca os index.html gerados.
"""
import html, re, datetime, pathlib

BASE = "https://catholicam.com.br"
ROOT = pathlib.Path(__file__).parent
src = (ROOT / "_src" / "site.html").read_text(encoding="utf-8")

head_end = src.index("</head>")
head = src[:head_end]
main_open = src.index('<main class="wrap">') + len('<main class="wrap">')
main_close = src.index("</main>")
header = src[src.index("<body>") + len("<body>"):main_open]
footer_script = src[main_close:]

sec_re = re.compile(r'(<!--[^\n]*-->\s*)?<section class="view(?: on)?" data-view="([a-z-]+)">.*?</section>', re.S)
sections = [(m.group(2), m.group(0)) for m in sec_re.finditer(src[main_open:main_close])]
views = [v for v, _ in sections]

def url(v):
    return "/" if v == "inicio" else f"/{v}/"

def fix_links(s):
    return re.sub(r'href="#([a-z-]+)"', lambda m: f'href="{url(m.group(1))}"' if m.group(1) in views else m.group(0), s)

def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

# descrições: sumário da página inicial, ou o primeiro parágrafo "lede" da seção
toc = {m.group(1): text(m.group(2)) for m in re.finditer(
    r'<a href="#([a-z-]+)"><span class="t">.*?<span class="d">(.*?)</span>', src)}

def describe(v, body):
    if v in toc:
        return toc[v]
    m = re.search(r'<p class="lede">(.*?)</p>', body, re.S)
    d = text(m.group(1)) if m else "Catholicam: a fé católica, inteira e sem anúncios."
    return d if len(d) <= 160 else d[:157].rsplit(" ", 1)[0] + "…"

# script: elementos de outras seções não existem mais na página
script = footer_script
script = script.replace('var $=function(id){return document.getElementById(id)};',
                        'var $=function(id){return document.getElementById(id)||document.createElement("div")};')
script = script.replace('setSet(todaySet);location.hash="terco"', 'location.href="/terco/"')
script = script.replace('var h=$("b-hit");', 'var h=document.getElementById("b-hit");')
script = script.replace('idb("readonly",function(s){return s.get("biblia")})',
                        'if(document.getElementById("b-text"))idb("readonly",function(s){return s.get("biblia")})')
route_start = script.index("/* ---------- Rotas ---------- */")
route_end = script.index("})();\n</script>", route_start)
script = script[:route_start] + """/* ---------- Página atual no menu ---------- */
Array.prototype.forEach.call(document.querySelectorAll("#nav a"),function(a){
  if(a.getAttribute("href")===location.pathname)a.setAttribute("aria-current","page");
});
""" + script[route_end:]
for k in ["setSet(todaySet);location.hash", "location.hash", "hashchange"]:
    assert k not in script, k
script = fix_links(script)
header_f = fix_links(header)

# links antigos (catholicam.com.br/#missa) continuam funcionando
legacy = ('<script>(function(){var h=location.hash.slice(1),v=%s;'
          'if(v.indexOf(h)>=0&&h!=="inicio")location.replace("/"+h+"/")})()</script>\n') % repr(views).replace("'", '"')

today = datetime.date.today().isoformat()
for v, body in sections:
    h1 = text(re.search(r"<h1>(.*?)</h1>", body, re.S).group(1))
    title = "Catholicam · " + h1.rstrip(".") if v == "inicio" else f"{h1} · Catholicam"
    desc = describe(v, body)
    if v == "inicio":
        desc = text(re.search(r'<p class="lede">(.*?)</p>', body, re.S).group(1))
    canon = BASE + url(v)
    meta = (f'<meta name="description" content="{html.escape(desc)}">\n'
            f'<link rel="canonical" href="{canon}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="Catholicam">\n'
            f'<meta property="og:title" content="{html.escape(title)}">\n'
            f'<meta property="og:description" content="{html.escape(desc)}">\n'
            f'<meta property="og:url" content="{canon}">\n'
            f'<meta property="og:locale" content="pt_BR">\n')
    h = head.replace("<title>Catholicam</title>", f"<title>{html.escape(title)}</title>\n" + meta)
    if v == "inicio":
        h += legacy
    sec = fix_links(body).replace('<section class="view"', '<section class="view on"', 1)
    page = h + "</head>\n<body>" + header_f + "\n\n" + sec + "\n\n" + script
    out = ROOT / ("index.html" if v == "inicio" else f"{v}/index.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")

(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{url(v)}</loc><lastmod>{today}</lastmod></url>\n" for v in views)
    + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
print(f"{len(views)} páginas geradas:", ", ".join(url(v) for v in views))
