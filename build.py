#!/usr/bin/env python3
"""Gera o site estático do Catholicam a partir de _src/site.html.

Edite sempre _src/site.html (e, se quiser, os textos de SEO abaixo); depois rode:
    python3 build.py
Saída: uma página por seção (/<secao>/index.html, a inicial em /index.html), uma página
por oração (/oracoes/<oracao>/), 404.html, sitemap.xml e robots.txt.
Precisa de Python 3 e Node.js (o Node lê as listas de orações e frases do script da página).
"""
import hashlib, html, json, re, subprocess, datetime, pathlib

BASE = "https://catholicam.com.br"
ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
src = (SRC / "site.html").read_text(encoding="utf-8")

# ---------------------------------------------------------------- textos de SEO
# título da aba / do Google (até ~60 caracteres) e descrição (até ~155 caracteres)
SEO = {
 "inicio": ("Catholicam: orações, Bíblia, terço e doutrina católica",
            "Site católico sem anúncios: orações, Bíblia, terço guiado, partes da Missa, doutrina, santos, Nossa Senhora e calendário litúrgico."),
 "doutrina": ("Doutrina católica: Credo, sacramentos e mandamentos",
            "O que a Igreja Católica crê, celebra e vive: o Credo, os sete sacramentos, os dez mandamentos, as virtudes e as obras de misericórdia."),
 "doutrina-social": ("Doutrina Social da Igreja: princípios e documentos",
            "Os princípios da Doutrina Social da Igreja sobre trabalho, economia, política e bem comum, o que a Igreja diz do capitalismo e do socialismo, e as encíclicas."),
 "frases": ("Frases de santos, de Jesus e de Maria, com a fonte",
            "Frases de Jesus, de Nossa Senhora e dos santos, cada uma com a fonte para conferir, e as frases que circulam atribuídas por engano."),
 "maria": ("Nossa Senhora: dogmas marianos, festas e Aparecida",
            "Quem é Maria para a Igreja Católica: os quatro dogmas marianos, as festas de Nossa Senhora, Nossa Senhora Aparecida e as aparições reconhecidas."),
 "santos": ("Santos católicos: canonização e santos do Brasil",
            "O que é um santo, a comunhão dos santos, por que a Igreja venera imagens, como alguém é canonizado e quem são os santos do Brasil."),
 "oracoes": ("Orações católicas: Pai Nosso, Ave Maria, Credo e mais",
            "As orações católicas com o texto usado no Brasil: Pai Nosso, Ave Maria, Credo, Salve Rainha, Santo Anjo, São Miguel Arcanjo, Angelus e a Via-Sacra."),
 "terco": ("Como rezar o terço: terço guiado e mistérios do dia",
            "Reze o Santo Terço conta por conta, com os mistérios gozosos, luminosos, dolorosos e gloriosos e os mistérios de cada dia da semana."),
 "biblia": ("Bíblia católica online: os 73 livros, com busca",
            "Leia a Bíblia católica online: os 73 livros do Antigo e do Novo Testamento, capítulo por capítulo, com busca por palavras."),
 "missa": ("Partes da Missa: respostas dos fiéis e posturas",
            "As partes da Santa Missa passo a passo, o que os fiéis respondem em cada momento, quando ficar de pé, sentado ou de joelhos, e as cores litúrgicas."),
 "calendario": ("Calendário litúrgico: Páscoa e datas móveis",
            "As datas móveis do ano litúrgico (Cinzas, Páscoa, Pentecostes, Corpus Christi, Advento), os dias de preceito no Brasil e as regras de jejum e abstinência."),
 "catequese": ("Catequese católica e como se confessar",
            "Um caminho de catequese por etapas, da Primeira Eucaristia à Crisma e ao catecumenato de adultos, e um guia prático para a Confissão com exame de consciência."),
 "musicas": ("Músicas católicas: cantos da Missa e hinos em latim",
            "O que se canta em cada momento da Missa, os hinos tradicionais em latim (Salve Regina, Regina Caeli, Tantum Ergo) e os cantos católicos mais conhecidos."),
 "livros": ("Livros católicos: clássicos e documentos da Igreja",
            "Uma estante de leitura espiritual: clássicos da espiritualidade católica e os principais documentos da Igreja para começar."),
 "apoiar": ("Apoie o Catholicam com uma doação por Pix",
            "O Catholicam não tem anúncios nem patrocinadores. Ajude a manter o site com uma doação por Pix, de qualquer valor."),
 "projeto": ("Sobre o Catholicam: site católico sem anúncios",
            "Quem somos e como funciona o Catholicam, um site católico sem anúncios e sem rastreamento, mantido por quem reza."),
}
# páginas de cada oração: endereço e título para o Google
PRAYERS = {
 "sinal": ("sinal-da-cruz", "Sinal da Cruz: a oração completa"),
 "pai": ("pai-nosso", "Pai Nosso: oração completa"),
 "ave": ("ave-maria", "Ave Maria: oração completa"),
 "gloria": ("gloria-ao-pai", "Glória ao Pai: oração completa"),
 "credo": ("credo", "Credo (Símbolo dos Apóstolos): oração completa"),
 "salve": ("salve-rainha", "Salve Rainha: oração completa"),
 "fatima": ("o-meu-jesus", "Ó meu Jesus, a oração de Fátima do terço"),
 "anjo": ("santo-anjo", "Oração do Santo Anjo da Guarda"),
 "contricao": ("ato-de-contricao", "Ato de Contrição: oração completa"),
 "espirito": ("vinde-espirito-santo", "Vinde, Espírito Santo: oração completa"),
 "miguel": ("sao-miguel-arcanjo", "Oração a São Miguel Arcanjo"),
 "angelus": ("angelus", "Angelus (O Anjo do Senhor): oração completa"),
 "regina": ("regina-caeli", "Rainha do Céu (Regina Caeli): oração completa"),
 "lembrai": ("lembrai-vos", "Lembrai-vos: oração a Nossa Senhora"),
 "protecao": ("a-vossa-protecao", "À vossa proteção: oração a Nossa Senhora"),
 "consagracao": ("consagracao-a-nossa-senhora", "Consagração a Nossa Senhora: oração completa"),
 "alma": ("alma-de-cristo", "Alma de Cristo: oração completa"),
}
IN_ROSARY = {"sinal", "credo", "pai", "ave", "gloria", "fatima", "salve"}

# ---------------------------------------------------------------- partes da fonte
head = src[:src.index("</head>")]
main_open = src.index('<main class="wrap">') + len('<main class="wrap">')
main_close = src.index("</main>")
header = src[src.index("<body>") + len("<body>"):main_open]
footer_script = src[main_close:]
sec_re = re.compile(r'(<!--[^\n]*-->\s*)?<section class="view(?: on)?" data-view="([a-z-]+)">.*?</section>', re.S)
sections = [(m.group(2), m.group(0)) for m in sec_re.finditer(src[main_open:main_close])]
views = [v for v, _ in sections]
missing = set(views) - set(SEO)
assert not missing, f"faltam textos de SEO para: {missing}"

def url(v): return "/" if v == "inicio" else f"/{v}/"
def esc(s): return html.escape(s, quote=True)
def text(s): return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
def fix_links(s):
    return re.sub(r'href="#([a-z-]+)"', lambda m: f'href="{url(m.group(1))}"' if m.group(1) in views else m.group(0), s)

# listas de orações e frases, lidas do próprio script da página
js = footer_script
p0, p1 = js.index("var P={"), js.index('var box=$("prayers")')
q0, q1 = js.index("var Q=["), js.index("function qfig")
data = json.loads(subprocess.run(["node", "-e", js[p0:p1] + js[q0:q1] + ";process.stdout.write(JSON.stringify({P:P,groups:groups,Q:Q}))"],
                                 capture_output=True, text=True, check=True).stdout)
P, GROUPS, Q = data["P"], data["groups"], data["Q"]
assert set(P) == set(PRAYERS), f"orações sem endereço: {set(P) ^ set(PRAYERS)}"
group_of = {k: g[0] for g in GROUPS for k in g[1]}
def purl(k): return f"/oracoes/{PRAYERS[k][0]}/"

# ---------------------------------------------------------------- cabeçalho comum
EXTRA_CSS = """
.crumb{font-family:var(--ui);font-size:.92rem;color:var(--muted);margin:1.2rem 0 0}
.crumb a{color:var(--muted)}
.prayer h3 a{color:inherit;text-decoration:none}
.prayer h3 a:hover{color:var(--accent);text-decoration:underline}
.related{list-style:none;padding:0;margin:0}
.related li{padding:.45rem 0;border-bottom:1px solid var(--line)}
"""
head = head.replace("</style>", EXTRA_CSS + "</style>", 1)
# fontes sem bloquear a renderização
fonts = re.search(r'<link href="(https://fonts.googleapis.com/css2[^"]+)" rel="stylesheet">', head)
head = head.replace(fonts.group(0),
    f'<link rel="preload" as="style" href="{fonts.group(1)}">\n'
    f'<link rel="stylesheet" href="{fonts.group(1)}" media="print" onload="this.media=\'all\'">\n'
    f'<noscript><link rel="stylesheet" href="{fonts.group(1)}"></noscript>')
head = head.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="theme-color" content="#2f6b45">\n'
    '<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">')

def page_head(title, desc, path, jsonld, extra=""):
    canon = BASE + path
    meta = (f"<title>{esc(title)}</title>\n"
            f'<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="canonical" href="{canon}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="Catholicam">\n'
            f'<meta property="og:locale" content="pt_BR">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{canon}">\n'
            f'<meta property="og:image" content="{BASE}/og.png">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n')
    return head.replace("<title>Catholicam</title>", meta) + extra

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": "Catholicam", "url": BASE + "/", "logo": BASE + "/apple-touch-icon.png"}
SITE = {"@type": "WebSite", "@id": BASE + "/#site", "name": "Catholicam", "url": BASE + "/", "inLanguage": "pt-BR", "publisher": {"@id": BASE + "/#org"}}

# ---------------------------------------------------------------- script comum
script = footer_script
def sub1(old, new):
    global script
    assert script.count(old) == 1, old
    script = script.replace(old, new)
sub1('var $=function(id){return document.getElementById(id)};',
     'var $=function(id){return document.getElementById(id)||document.createElement("div")};')
sub1('setSet(todaySet);location.hash="terco"', 'location.href="/terco/"')
sub1('var h=$("b-hit");', 'var h=document.getElementById("b-hit");')
sub1('idb("readonly",function(s){return s.get("biblia")})',
     'if(document.getElementById("b-text"))idb("readonly",function(s){return s.get("biblia")})')
# orações e frases já vêm prontas no HTML: o script só cria os atalhos
sub1('groups.forEach(function(g){\n  var w=document.createElement("div");w.className="stack cat-h";',
     'if(box.querySelector(".cat-h"))Array.prototype.forEach.call(box.querySelectorAll(".cat-h"),function(w,i){jump(groups[i][0],w)});\n'
     'else groups.forEach(function(g){\n  var w=document.createElement("div");w.className="stack cat-h";')
sub1('.forEach(function(g){\n    var w=document.createElement("div");w.className="stack cat-h";',
     '.forEach(function(g,i){\n    var pre=box.querySelectorAll(".cat-h");if(pre.length){chip(g[0],pre[i]);return}\n'
     '    var w=document.createElement("div");w.className="stack cat-h";')
r0 = script.index("/* ---------- Rotas ---------- */")
r1 = script.index("})();\n</script>", r0)
script = script[:r0] + """/* ---------- Página atual no menu ---------- */
Array.prototype.forEach.call(document.querySelectorAll("#nav a"),function(a){
  var h=a.getAttribute("href"),p=location.pathname;
  if(h===p||(h!=="/"&&p.indexOf(h)===0))a.setAttribute("aria-current","page");
});
""" + script[r1:]
for k in ["location.hash", "hashchange"]:
    assert k not in script, k
script = fix_links(script)
QR_TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n'
assert QR_TAG in script
script_noqr = script.replace(QR_TAG, "")
header_f = fix_links(header)

# ---------------------------------------------------------------- conteúdo pré-montado
def prayer_article(k, link=True, tag="h3"):
    p = P[k]
    t = f'<a href="{purl(k)}">{esc(p["t"])}</a>' if link else esc(p["t"])
    r = f'<p class="r">{esc(p["r"])}</p>' if p.get("r") else ""
    return f'<article class="prayer"><{tag}>{t}</{tag}>{r}<p>{esc(p["x"])}</p></article>'

prayers_html = "".join(
    f'<div class="stack cat-h"><h2>{esc(g[0])}</h2>' + "".join(prayer_article(k) for k in g[1]) + "</div>" for g in GROUPS)

def qfig(q):
    return f'<figure class="quote"><blockquote>{esc(q[1])}</blockquote><figcaption><b>{esc(q[0])}</b> · {esc(q[2])}</figcaption></figure>'
QG = [("Palavras de Jesus", lambda q: q[0] == "Jesus Cristo"), ("Palavras de Maria", lambda q: q[0] == "Maria"),
      ("Palavras dos santos", lambda q: q[0] not in ("Jesus Cristo", "Maria"))]
quotes_html = "".join(f'<div class="stack cat-h"><h2>{n}</h2>' + "".join(qfig(q) for q in Q if f(q)) + "</div>" for n, f in QG)

def fill(body, div_id, inner):
    tag = f'<div id="{div_id}" class="stack"></div>'
    assert tag in body, div_id
    return body.replace(tag, f'<div id="{div_id}" class="stack">{inner}</div>')

# ---------------------------------------------------------------- gravação
pages = {}  # caminho -> html
legacy = ('<script>(function(){var h=location.hash.slice(1),v=%s;'
          'if(v.indexOf(h)>=0&&h!=="inicio")location.replace("/"+h+"/")})()</script>\n') % json.dumps(views)

for v, body in sections:
    title, desc = SEO[v]
    if v != "inicio":
        title += " · Catholicam"
    h1 = text(re.search(r"<h1>(.*?)</h1>", body, re.S).group(1))
    if v == "inicio":
        ld = {"@context": "https://schema.org", "@graph": [ORG, SITE]}
    else:
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "name": h1, "url": BASE + url(v), "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
            crumbs_ld([("Início", "/"), (h1, url(v))])]}
    sec = fix_links(body).replace('<section class="view"', '<section class="view on"', 1)
    if v == "oracoes": sec = fill(sec, "prayers", prayers_html)
    if v == "frases": sec = fill(sec, "quotes", quotes_html)
    pages[url(v)] = (page_head(title, desc, url(v), ld, legacy if v == "inicio" else "") + "</head>\n<body>" + header_f
                     + "\n\n" + sec + "\n\n" + (script if v == "apoiar" else script_noqr))

for k, (slug, seo_title) in PRAYERS.items():
    p, path, grp = P[k], purl(k), group_of[k]
    first = re.sub(r"\s+", " ", p["x"]).strip()
    desc = f'Texto completo da oração {p["t"]}, como se reza no Brasil: “{first}'
    desc = (desc[:150].rsplit(" ", 1)[0] + "…”") if len(desc) > 152 else desc + "”"
    siblings = [s for g in GROUPS if g[0] == grp for s in g[1] if s != k]
    extra = ""
    if k in IN_ROSARY:
        extra += '<p>Esta oração faz parte do <a href="/terco/">Santo Terço</a>. Reze o terço guiado, conta por conta.</p>'
    body = (f'<section class="view on" data-view="oracao">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/oracoes/">Orações</a> › {esc(p["t"])}</nav>\n'
            f'<div class="stack">{prayer_article(k, link=False, tag="h1")}{extra}</div>\n'
            f'<div class="stack"><h2>{esc(grp)}</h2><ul class="related">'
            + "".join(f'<li><a href="{purl(s)}">{esc(P[s]["t"])}</a></li>' for s in siblings)
            + f'</ul><p><a href="/oracoes/">Ver todas as orações</a></p></div>\n</section>')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": p["t"], "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
        crumbs_ld([("Início", "/"), ("Orações", "/oracoes/"), (p["t"], path)])]}
    pages[path] = (page_head(f"{seo_title} · Catholicam", desc, path, ld) + "</head>\n<body>" + header_f
                   + "\n\n" + body + "\n\n" + script_noqr)

nf = ('<section class="view on" data-view="404"><div class="stack"><h1>Página não encontrada</h1>'
      '<p class="lede">O endereço não existe ou mudou. Veja o sumário abaixo ou volte ao <a href="/">início</a>.</p></div>'
      '<ul class="related">' + "".join(f'<li><a href="{url(v)}">{esc(SEO[v][0])}</a></li>' for v in views if v != "inicio") + "</ul></section>")
nf_html = (head.replace("<title>Catholicam</title>", '<title>Página não encontrada · Catholicam</title>\n<meta name="robots" content="noindex">')
           + "</head>\n<body>" + header_f + "\n\n" + nf + "\n\n" + script_noqr)

def write(path, content):
    out = ROOT / (path.strip("/") + "/index.html" if path != "/" else "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")

for path, content in pages.items():
    write(path, content)
(ROOT / "404.html").write_text(nf_html, encoding="utf-8")

# lastmod só muda quando o conteúdo da página muda
lm_file = SRC / "lastmod.json"
lm = json.loads(lm_file.read_text()) if lm_file.exists() else {}
today = datetime.date.today().isoformat()
for path, content in pages.items():
    h = hashlib.sha256(content.encode()).hexdigest()[:16]
    if lm.get(path, {}).get("hash") != h:
        lm[path] = {"hash": h, "date": today}
lm = {p: lm[p] for p in pages}
lm_file.write_text(json.dumps(lm, indent=1, ensure_ascii=False) + "\n")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>{lm[p]['date']}</lastmod></url>\n" for p in pages)
    + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
print(f"{len(pages)} páginas geradas + 404.html")
