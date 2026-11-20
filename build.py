#!/usr/bin/env python3
"""Gera o site estático do Catholicam a partir de _src/site.html.

Edite sempre _src/site.html (e, se quiser, os textos de SEO abaixo); depois rode:
    python3 build.py
Saída: uma página por seção (/<secao>/index.html, a inicial em /index.html), uma página
por oração (/oracoes/<oracao>/), uma por grupo de mistérios do terço (/terco/misterios-<grupo>/),
uma por livro e por capítulo da Bíblia (/biblia/<livro>/<capitulo>/), 404.html, sitemap.xml,
robots.txt e os arquivos comuns em /assets/ (site.css, site.js e biblia.json, usado na busca).
O /assets/qrcode.min.js (qrcodejs 1.0.0, licença MIT) fica no repositório e não é gerado.
Precisa de Python 3 e Node.js (o Node lê as listas de orações, frases e mistérios do script da página).
Textos extras das orações (título do Google, descrição, outros nomes, versões, história, latim): _src/oracoes_info.json.
Texto da Bíblia: _src/biblia.json (baixado de BIBLIA_FONTE na primeira vez, se não existir).
"""
import hashlib, html, json, re, subprocess, datetime, pathlib, unicodedata, urllib.request

BASE = "https://catholicam.com.br"
ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
src = (SRC / "site.html").read_text(encoding="utf-8")
INFO = json.loads((SRC / "oracoes_info.json").read_text(encoding="utf-8"))
BIBLIA_FONTE = "https://raw.githubusercontent.com/Dancrf/biblia-db/main/biblia.json"
BIBLIA_TRAD = "tradução do Pe. Matos Soares (1956)"
bib_file = SRC / "biblia.json"
if not bib_file.exists():
    bib_file.write_bytes(urllib.request.urlopen(BIBLIA_FONTE).read())
BIBLE = json.loads(bib_file.read_text(encoding="utf-8"))

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
# endereço de cada oração. Título do Google, título da página (h1), descrição, outros nomes,
# outras versões e links "veja também" ficam em _src/oracoes_info.json.
PRAYERS = {
 "sinal": "sinal-da-cruz", "pai": "pai-nosso", "ave": "ave-maria", "gloria": "gloria-ao-pai",
 "credo": "credo", "salve": "salve-rainha", "fatima": "o-meu-jesus", "anjo": "santo-anjo",
 "contricao": "ato-de-contricao", "espirito": "vinde-espirito-santo", "miguel": "sao-miguel-arcanjo",
 "angelus": "angelus", "regina": "regina-caeli", "lembrai": "lembrai-vos", "protecao": "a-vossa-protecao",
 "consagracao": "consagracao-a-nossa-senhora", "alma": "alma-de-cristo",
}
for _k, _v in INFO.items():
    for _c in ("titulo", "h1", "descricao", "historia", "quando"):
        assert _v.get(_c), f"oracoes_info.json: falta {_c} em {_k}"
    assert len(_v["titulo"]) <= 60, f"título longo demais ({_k}): o Google corta perto de 60 caracteres"
    assert len(_v["descricao"]) <= 160, f"descrição longa demais ({_k}): o Google corta perto de 160 caracteres"
IN_ROSARY = {"sinal", "credo", "pai", "ave", "gloria", "fatima", "salve"}

# ---------------------------------------------------------------- partes da fonte
head = src[:src.index("</head>")]
main_open = src.index('<main class="wrap" id="conteudo">') + len('<main class="wrap" id="conteudo">')
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
m0, m1 = js.index("var M={"), js.index("var ord=")
b0, b1 = js.index("var B=["), js.index("/* Páginas da Bíblia")
data = json.loads(subprocess.run(["node", "-e", js[p0:p1] + js[q0:q1] + js[m0:m1] + js[b0:b1]
                                  + ";process.stdout.write(JSON.stringify({P:P,groups:groups,Q:Q,M:M,byDay:byDay,B:B}))"],
                                 capture_output=True, text=True, check=True).stdout)
P, GROUPS, Q, M, BYDAY, BGROUPS = data["P"], data["groups"], data["Q"], data["M"], data["byDay"], data["B"]
assert set(INFO) == set(P), f"oracoes_info.json não bate com as orações: {set(INFO) ^ set(P)}"
assert set(P) == set(PRAYERS), f"orações sem endereço: {set(P) ^ set(PRAYERS)}"
group_of = {k: g[0] for g in GROUPS for k in g[1]}
def purl(k): return f"/oracoes/{PRAYERS[k]}/"

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
# CSS num arquivo próprio (/assets/site.css), que o navegador guarda entre uma página e outra
css_m = re.search(r"<style>\n?(.*?)</style>\n?", head, re.S)
SITE_CSS = css_m.group(1)
css_ver = hashlib.sha256(SITE_CSS.encode()).hexdigest()[:10]
head = head.replace(css_m.group(0), f'<link rel="stylesheet" href="/assets/site.css?v={css_ver}">\n')
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
QR_TAG = '<script src="/assets/qrcode.min.js"></script>\n'
assert QR_TAG in script
# JavaScript num arquivo próprio (/assets/site.js)
js_m = re.search(r"<script>\n(.*?)</script>\n", script, re.S)
SITE_JS = js_m.group(1)
js_ver = hashlib.sha256(SITE_JS.encode()).hexdigest()[:10]
script = script.replace(js_m.group(0), f'<script src="/assets/site.js?v={js_ver}" defer></script>\n')
script_noqr = script.replace(QR_TAG, "")
header_f = fix_links(header)

# ---------------------------------------------------------------- Bíblia: livros, endereços e referências
def slugify(t):
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

BOOKS = []  # {n: nome curto, s: endereço, g: grupo, caps: [[(num, texto), ...], ...]}
_flat = [(b[0], b[1], g[0]) for g in BGROUPS for b in g[1]]
assert len(_flat) == len(BIBLE) == 73
for (name, nch, grp), bk in zip(_flat, BIBLE):
    assert len(bk["capitulos"]) == nch, (name, nch, len(bk["capitulos"]))
    BOOKS.append({"n": name, "s": slugify(name), "g": grp,
                  "caps": [[(v["numero"], v["texto"]) for v in c["versiculos"]] for c in bk["capitulos"]]})
assert len({b["s"] for b in BOOKS}) == 73
def burl(b, c=None): return f"/biblia/{b['s']}/" + (f"{c}/" if c else "")

# Salmos: o texto segue a numeração grega/Vulgata; entre parênteses, a hebraica, usada em muitas Bíblias
def salmo_hebraico(n):
    if n <= 8 or n >= 148: return str(n)
    if n == 9: return "9-10"
    if n <= 112 or 116 <= n <= 145: return str(n + 1)
    if n == 113: return "114-115"
    return "116" if n in (114, 115) else "147"
def cap_name(b, c):
    if b["n"] == "Salmos":
        h = salmo_hebraico(c)
        return f"Salmo {c}" + (f" ({h})" if h != str(c) else "")
    return f"{b['n']} {c}"

# abreviaturas usadas no Brasil -> livro (Salmos fica de fora: a numeração das citações varia)
ABBR = dict(zip("Gn Ex Lv Nm Dt Js Jz Rt 1Sm 2Sm 1Rs 2Rs 1Cr 2Cr Esd Ne Tb Jt Est 1Mc 2Mc Jó Sl Pr Ecl Ct Sb Eclo Is Jr Lm Br Ez Dn Os Jl Am Ab Jn Mq Na Hab Sf Ag Zc Ml "
                "Mt Mc Lc Jo At Rm 1Cor 2Cor Gl Ef Fl Cl 1Ts 2Ts 1Tm 2Tm Tt Fm Hb Tg 1Pd 2Pd 1Jo 2Jo 3Jo Jd Ap".split(), BOOKS))
del ABBR["Sl"]
REF_RE = re.compile(r"(?<![\w-])(" + "|".join(sorted((re.escape(a).replace("\\ ", " ") for a in ABBR), key=len, reverse=True))
                    + r")\s?(\d+),(\d+)((?:-\d+)?)")
def ref_target(m):
    b = ABBR[m.group(1)]; c, v = int(m.group(2)), int(m.group(3))
    if not (1 <= c <= len(b["caps"])): return None
    return burl(b, c) + f"#v{v}"
def linkify(escaped):
    """Transforma citações como "Jo 14,6" em links para o capítulo (recebe texto já escapado)."""
    def r(m):
        t = ref_target(m)
        return f'<a href="{t}">{m.group(0)}</a>' if t else m.group(0)
    return REF_RE.sub(r, escaped)
def passage(ref):
    """Texto de uma citação simples ("Lc 1,26-38") a partir da Bíblia do site."""
    m = REF_RE.fullmatch(ref.strip())
    if not m: return None
    b = ABBR[m.group(1)]; c, v0 = int(m.group(2)), int(m.group(3))
    v1 = int(m.group(4)[1:]) if m.group(4) else v0
    vs = [(n, t) for n, t in b["caps"][c - 1] if v0 <= n <= v1]
    return vs or None

# ---------------------------------------------------------------- conteúdo pré-montado
def prayer_article(k, link=True, tag="h3", title=None):
    p = P[k]
    t = f'<a href="{purl(k)}">{esc(p["t"])}</a>' if link else esc(title or p["t"])
    r = f'<p class="r">{esc(p["r"])}</p>' if p.get("r") else ""
    return f'<article class="prayer"><{tag}>{t}</{tag}>{r}<p>{esc(p["x"])}</p></article>'

prayers_html = "".join(
    f'<div class="stack cat-h"><h2>{esc(g[0])}</h2>' + "".join(prayer_article(k) for k in g[1]) + "</div>" for g in GROUPS)

def qfig(q):
    return f'<figure class="quote"><blockquote>{esc(q[1])}</blockquote><figcaption><b>{esc(q[0])}</b> · {linkify(esc(q[2]))}</figcaption></figure>'
QG = [("Palavras de Jesus", lambda q: q[0] == "Jesus Cristo"), ("Palavras de Maria", lambda q: q[0] == "Maria"),
      ("Palavras dos santos", lambda q: q[0] not in ("Jesus Cristo", "Maria"))]
quotes_html = "".join(f'<div class="stack cat-h"><h2>{n}</h2>' + "".join(qfig(q) for q in Q if f(q)) + "</div>" for n, f in QG)

def fill(body, div_id, inner):
    tag = f'<div id="{div_id}" class="stack"></div>'
    assert tag in body, div_id
    return body.replace(tag, f'<div id="{div_id}" class="stack">{inner}</div>')

# títulos com âncora (id) e sumário "Nesta página" nas páginas longas
def add_ids(body):
    used = set(re.findall(r'id="([^"]+)"', body))
    def r(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if "id=" in attrs or not text(inner): return m.group(0)
        base = slugify(text(inner))[:60] or "secao"; i, sid = 2, base
        while sid in used: sid, i = f"{base}-{i}", i + 1
        used.add(sid)
        return f'<{tag}{attrs} id="{sid}">{inner}</{tag}>'
    return re.sub(r"<(h[23])([^>]*)>(.*?)</\1>", r, body, flags=re.S)
def add_toc(body):
    hs = re.findall(r'<h2[^>]* id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(hs) < 4: return body
    toc = ('<nav class="toc-page" aria-label="Nesta página"><b>Nesta página</b><ul>'
           + "".join(f'<li><a href="#{i}">{esc(text(t))}</a></li>' for i, t in hs) + "</ul></nav>")
    m = re.search(r'<p class="lede">.*?</p>', body, re.S) or re.search(r"</h1>", body)
    return body[:m.end()] + toc + body[m.end():]

# lista de livros da Bíblia (página /biblia/)
books_html = "".join(
    f'<div class="stack"><h2>{esc(g[0])}</h2><div class="books">'
    + "".join(f'<a class="book" href="{burl(b)}"><span>{esc(b["n"])}</span><small>{len(b["caps"])}</small></a>'
              for b in BOOKS if b["g"] == g[0]) + "</div></div>" for g in BGROUPS)

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
        if v == "oracoes":
            ld["@graph"].append({"@type": "ItemList", "name": "Orações católicas", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": P[k]["t"], "url": BASE + purl(k)}
                for i, k in enumerate(k for g in GROUPS for k in g[1])]})
    sec = fix_links(body).replace('<section class="view"', '<section class="view on"', 1)
    if v == "oracoes": sec = fill(sec, "prayers", prayers_html)
    if v == "frases": sec = fill(sec, "quotes", quotes_html)
    if v == "biblia": sec = fill(sec, "books", books_html)
    if v not in ("inicio",): sec = add_ids(sec)
    if v not in ("inicio", "oracoes", "frases", "biblia"): sec = add_toc(sec)
    pages[url(v)] = (page_head(title, desc, url(v), ld, legacy if v == "inicio" else "") + "</head>\n<body>" + header_f
                     + "\n\n" + sec + "\n\n" + (script if v == "apoiar" else script_noqr))

def prayer_text(t):
    return "".join(f"<p>{esc(par).replace(chr(10), '<br>')}</p>" for par in t.split("\n\n"))
for k in PRAYERS:
    p, path, grp, info = P[k], purl(k), group_of[k], INFO[k]
    desc = info["descricao"]
    siblings = [s for g in GROUPS if g[0] == grp for s in g[1] if s != k]
    extra = ""
    if info.get("nomes"):
        extra += f'<p class="r">Outros nomes: {esc(", ".join(info["nomes"]))}.</p>'
    if k in IN_ROSARY:
        extra += '<p>Esta oração faz parte do <a href="/terco/">Santo Terço</a>. Reze o terço guiado, conta por conta.</p>'
    more = ""
    for nome_v, texto_v in info.get("versoes", []):
        more += (f'<div class="stack"><h2>{esc(p["t"])}: {esc(nome_v.lower() if nome_v.startswith("Versão") else nome_v)}</h2>'
                 f'<article class="prayer">{prayer_text(texto_v)}</article></div>\n')
    more += ('<div class="stack"><h2 id="historia">Origem e história</h2>'
             + "".join(f"<p>{linkify(esc(t))}</p>" for t in info["historia"])
             + f'<p><b>Quando rezar:</b> {esc(info["quando"])}</p></div>\n')
    if info.get("latim"):
        more += ('<div class="stack"><h2 id="latim">Em latim</h2>'
                 f'<p class="latin" lang="la">{esc(info["latim"]).replace(chr(10), "<br>")}</p></div>\n')
    if info.get("veja"):
        more += ('<div class="stack"><h2 id="veja-tambem">Veja também</h2><ul class="related">'
                 + "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in info["veja"]) + "</ul></div>\n")
    body = (f'<section class="view on" data-view="oracao">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/oracoes/">Orações</a> › {esc(p["t"])}</nav>\n'
            f'<div class="stack">{prayer_article(k, link=False, tag="h1", title=info["h1"])}{extra}</div>\n' + more +
            f'<div class="stack"><h2>{esc(grp)}</h2><ul class="related">'
            + "".join(f'<li><a href="{purl(s)}">{esc(INFO[s]["h1"])}</a></li>' for s in siblings)
            + f'</ul><p><a href="/oracoes/">Ver todas as orações católicas</a></p></div>\n</section>')
    oracao = {"@type": "CreativeWork", "@id": BASE + path + "#oracao", "name": p["t"], "genre": "Oração católica",
              "inLanguage": "pt-BR", "text": re.sub(r"\s+", " ", p["x"]).strip(), "isPartOf": {"@id": BASE + "/#site"}}
    if info.get("nomes"): oracao["alternateName"] = info["nomes"]
    if info.get("latim"):
        oracao["translationOfWork"] = {"@type": "CreativeWork", "inLanguage": "la", "text": re.sub(r"\s+", " ", info["latim"]).strip()}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": BASE + path, "name": info["h1"], "url": BASE + path, "description": desc, "inLanguage": "pt-BR",
         "isPartOf": {"@id": BASE + "/#site"}, "mainEntity": {"@id": BASE + path + "#oracao"}},
        oracao,
        crumbs_ld([("Início", "/"), ("Orações", "/oracoes/"), (p["t"], path)])]}
    pages[path] = (page_head(f'{info["titulo"]} · Catholicam', desc, path, ld) + "</head>\n<body>" + header_f
                   + "\n\n" + body + "\n\n" + script_noqr)

# ---------------------------------------------------------------- mistérios do terço
DIAS = ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado"]
ORD = ["1º", "2º", "3º", "4º", "5º"]
SET_ORDER = ["gozosos", "luminosos", "dolorosos", "gloriosos"]
assert set(SET_ORDER) == set(M)
def murl(k): return f"/terco/misterios-{k}/"
DIAS_PL = {"domingo": "aos domingos", "sábado": "aos sábados"}
def dias_de(k):
    d = [DIAS[i] for i, x in enumerate(BYDAY) if x == k]
    d = d[1:] + d[:1] if d and d[0] == "domingo" else d  # domingo por último
    return " e ".join(DIAS_PL.get(x, "às " + x.replace("-feira", "s-feiras")) for x in d)
for k in SET_ORDER:
    mset, path = M[k], murl(k)
    nome = mset["n"].lower()
    dias = dias_de(k)
    items = ""
    for j, (titulo, ref) in enumerate(mset["m"]):
        vs = passage(ref)
        refh = linkify(esc(ref))
        txt = ""
        if vs:
            txt = ('<div class="passage">' + "".join(f'<p><span class="vn">{n}</span>{esc(t)}</p>' for n, t in vs) + "</div>")
        items += (f'<div class="stack"><h2 id="misterio-{j+1}">{ORD[j]} mistério: {esc(titulo)}</h2>'
                  f'<p class="r">{refh}</p>{txt}</div>\n')
    outros = " · ".join(f'<a href="{murl(o)}">Mistérios {M[o]["n"].lower()}</a>' for o in SET_ORDER if o != k)
    title = f"Mistérios {nome} do terço, com os textos da Bíblia"
    resumo = ", ".join(t[0][0].lower() + t[0][1:] for t in mset["m"][:3])
    desc = f"Os cinco mistérios {nome} do Santo Terço, rezados {dias}: {resumo}... com o texto bíblico de cada um."
    if len(desc) > 158: desc = desc[:155].rsplit(" ", 1)[0] + "…"
    body = (f'<section class="view on" data-view="misterios">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/terco/">Terço</a> › Mistérios {nome}</nav>\n'
            f'<div class="stack"><h1>Mistérios {nome}</h1><p class="lede">Rezados {dias}. '
            f'Em cada mistério se reza um Pai Nosso, dez Ave-Marias e um Glória ao Pai, contemplando a passagem do Evangelho.</p>'
            f'<p><a class="btn" href="/terco/">Rezar o terço guiado</a></p></div>\n'
            + items +
            f'<div class="stack"><h2 id="outros">Outros mistérios</h2><p>{outros}</p></div>\n</section>')
    body = add_toc(body)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": f"Mistérios {nome}", "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
        crumbs_ld([("Início", "/"), ("Terço", "/terco/"), (f"Mistérios {nome}", path)])]}
    pages[path] = (page_head(f"{title} · Catholicam", desc, path, ld) + "</head>\n<body>" + header_f
                   + "\n\n" + body + "\n\n" + script_noqr)

# ---------------------------------------------------------------- Bíblia: uma página por livro e por capítulo
def short(t, n=150):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"
flatcaps = [(bi, c) for bi, b in enumerate(BOOKS) for c in range(1, len(b["caps"]) + 1)]
for bi, b in enumerate(BOOKS):
    nch = len(b["caps"])
    path = burl(b)
    grid = '<div class="chapters">' + "".join(f'<a href="{burl(b, c)}">{c}</a>' for c in range(1, nch + 1)) + "</div>"
    first = b["caps"][0][0][1]
    caps_txt = "capítulo" if nch == 1 else "capítulos"
    desc = short(f"Leia {b['n']} na Bíblia católica, {nch} {caps_txt}, tradução do Pe. Matos Soares. Começa assim: “{first}", 152)
    if not desc.endswith("…"): desc += "”"
    body = (f'<section class="view on" data-view="biblia-livro">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/biblia/">Bíblia</a> › {esc(b["n"])}</nav>\n'
            f'<div class="stack"><h1>{esc(b["n"])}</h1><p class="lede">{esc(b["g"])} · {nch} {caps_txt}</p></div>\n'
            f'<div class="stack"><h2 id="capitulos">Capítulos</h2>{grid}</div>\n'
            f'<p><a href="/biblia/">Todos os livros da Bíblia</a></p>\n</section>')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": b["n"], "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
        crumbs_ld([("Início", "/"), ("Bíblia", "/biblia/"), (b["n"], path)])]}
    pages[path] = (page_head(f"{b['n']}: Bíblia católica online · Catholicam", desc, path, ld) + "</head>\n<body>" + header_f
                   + "\n\n" + body + "\n\n" + script_noqr)

for i, (bi, c) in enumerate(flatcaps):
    b = BOOKS[bi]; nch = len(b["caps"]); path = burl(b, c); nome = cap_name(b, c)
    verses, seen = [], set()
    for n, t in b["caps"][c - 1]:
        vid = f' id="v{n}"' if n not in seen else ""
        seen.add(n)
        verses.append(f'<p{vid}><a class="vn" href="#v{n}">{n}</a>{esc(t)}</p>')
    def link(j, cls, lab):
        if not (0 <= j < len(flatcaps)): return ""
        ob, oc = BOOKS[flatcaps[j][0]], flatcaps[j][1]
        return f'<a class="{cls}" href="{burl(ob, oc)}" rel="{cls}"><small>{lab}</small>{esc(cap_name(ob, oc))}</a>'
    pager = '<nav class="pager" aria-label="Capítulos">' + link(i - 1, "prev", "Anterior") + link(i + 1, "next", "Próximo") + "</nav>"
    grid = '<div class="chapters">' + "".join(
        f'<a href="{burl(b, k)}"' + (' aria-current="page"' if k == c else "") + f">{k}</a>" for k in range(1, nch + 1)) + "</div>"
    info = f"{esc(b['n'])} · capítulo {c} de {nch} · {BIBLIA_TRAD}"
    if b["n"] == "Salmos" and "(" in nome:
        info += " · numeração da Vulgata; entre parênteses, a numeração hebraica"
    desc = short(f"{nome} na Bíblia católica, tradução do Pe. Matos Soares: “{b['caps'][c-1][0][1]}", 152)
    if not desc.endswith("…"): desc += "”"
    body = (f'<section class="view on" data-view="biblia-capitulo">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/biblia/">Bíblia</a> › '
            f'<a href="{burl(b)}">{esc(b["n"])}</a> › Capítulo {c}</nav>\n'
            f'<div class="stack"><h1>{esc(nome)}</h1><p class="r">{info}</p></div>\n'
            f'<div class="reader"><div class="verses">{"".join(verses)}</div></div>\n'
            f'{pager}\n'
            f'<div class="stack"><h2 id="capitulos">Capítulos de {esc(b["n"])}</h2>{grid}'
            f'<p><a href="/biblia/">Todos os livros da Bíblia</a></p></div>\n</section>')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": nome, "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
        crumbs_ld([("Início", "/"), ("Bíblia", "/biblia/"), (b["n"], burl(b)), (f"Capítulo {c}", path)])]}
    pages[path] = (page_head(f"{nome}: Bíblia católica online · Catholicam", desc, path, ld)
                   + "</head>\n" + f'<body data-biblia="{esc(nome)}">' + header_f + "\n\n" + body + "\n\n" + script_noqr)

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
assets = ROOT / "assets"
assets.mkdir(exist_ok=True)
(assets / "site.css").write_text(SITE_CSS, encoding="utf-8")
(assets / "site.js").write_text(SITE_JS, encoding="utf-8")
(assets / "biblia.json").write_text(json.dumps(
    [{"n": b["n"], "s": b["s"], "c": [[[n, t] for n, t in cap] for cap in b["caps"]]} for b in BOOKS],
    ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
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
