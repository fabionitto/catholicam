#!/usr/bin/env python3
"""Gera o site estático do Catholicam a partir de _src/site.html.

Edite sempre _src/site.html (e, se quiser, os textos de SEO abaixo); depois rode:
    python3 build.py
Saída: uma página por seção (/<secao>/index.html, a inicial em /index.html), uma página
por oração (/oracoes/<oracao>/), uma por grupo de mistérios do terço (/terco/misterios-<grupo>/),
uma por livro e por capítulo da Bíblia (/biblia/<livro>/<capitulo>/), 404.html, sitemap.xml,
robots.txt e os arquivos comuns em /assets/ (site.css, site.js, lit.js e biblia.json, usado na busca).
O calendário litúrgico (cor do dia, que também colore o site) fica em _src/lit.js e é copiado para /assets/lit.js.
O /assets/qrcode.min.js (qrcodejs 1.0.0, licença MIT) fica no repositório e não é gerado.
Precisa de Python 3 e Node.js (o Node lê as listas de orações, frases e mistérios do script da página).
Textos extras das orações (título do Google, descrição, outros nomes, versões, história, latim,
orações rezadas junto ("junto") e perguntas frequentes ("faq", também em FAQPage no JSON-LD)): _src/oracoes_info.json.
Liturgia diária (/liturgia/): o texto das leituras não é copiado (direitos da CNBB); a página mostra o
site oficial da CNBB num iframe que só carrega quando o visitante pede.
Frase do dia (página inicial): versículo do Evangelho da Missa, dito por Jesus ou por Maria, escolhido no build
(veja "Frase do dia a partir do Evangelho da Missa" abaixo; o build busca os dias novos na internet).
Texto da Bíblia: _src/biblia.json (baixado de BIBLIA_FONTE na primeira vez, se não existir).
Apresentação de cada livro da Bíblia (página do livro e descrição do Google): _src/biblia_intro.json.
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
 "liturgia": ("Liturgia diária: leituras da Missa de hoje (CNBB)",
            "As leituras da Missa de hoje na liturgia diária da CNBB, o tempo litúrgico e a cor do dia, e como funcionam os anos A, B e C e o ano par e ímpar."),
 "calendario": ("Calendário litúrgico: Páscoa e datas móveis",
            "As datas móveis do ano litúrgico (Cinzas, Páscoa, Pentecostes, Corpus Christi, Advento), os dias de preceito no Brasil e as regras de jejum e abstinência."),
 "catequese": ("Catequese católica e como se confessar",
            "Um caminho de catequese por etapas, da Primeira Eucaristia à Crisma e ao catecumenato de adultos, e um guia prático para a Confissão com exame de consciência."),
 "musicas": ("Músicas católicas: cantos da Missa e hinos em latim",
            "O que se canta em cada momento da Missa, os hinos tradicionais em latim (Salve Regina, Regina Caeli, Tantum Ergo) e os cantos católicos mais conhecidos."),
 "livros": ("Livros católicos: clássicos e documentos da Igreja",
            "Uma estante de leitura espiritual: clássicos da espiritualidade católica e os principais documentos da Igreja para começar."),
 "apoiar": ("Doação por Pix: apoie o Catholicam, site católico",
            "Faça uma doação por Pix, de qualquer valor, para manter o Catholicam: um site católico sem anúncios, sem patrocinadores e sem rastreamento."),
 "projeto": ("Sobre o Catholicam: site católico sem anúncios",
            "Quem somos e como funciona o Catholicam, um site católico sem anúncios e sem rastreamento, mantido por quem reza."),
 "sugestoes": ("Sugestões e correções para o Catholicam",
            "Envie uma sugestão, avise sobre um erro no conteúdo ou peça uma oração que falta no Catholicam, site católico sem anúncios."),
}
# Página de sugestões: CSP própria e rígida (só scripts e estilos do site; envio só para o Web3Forms).
# O GitHub Pages não deixa configurar headers, então a política vai num <meta>, logo no começo do <head>.
SUG_CSP = ('<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\'; '
           "style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://api.web3forms.com; "
           "form-action 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'\">\n"
           '<meta name="referrer" content="strict-origin-when-cross-origin">')
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
    for _q in _v.get("faq", []):
        assert len(_q) == 2 and _q[0].endswith("?"), f"faq de {_k}: cada item é [pergunta?, resposta]"
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
def full_title(t):
    """Título com " · Catholicam" no fim, só se não passar de 65 caracteres (o Google corta perto disso)."""
    return t if len(t) + len(" · Catholicam") > 65 else t + " · Catholicam"
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
/* acordeões (<details>) das listas longas: o texto fica no HTML, só recolhido */
.acc{border-top:1px solid var(--line)}
.acc>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:.75rem;padding:.85rem .35rem;border-radius:4px;transition:background-color .15s}
.acc>summary::-webkit-details-marker{display:none}
.acc>summary:hover{background:var(--surface)}
.acc>summary>h2,.acc>summary>h3{flex:1;margin:0;font-family:var(--ui);font-size:1.12rem;font-weight:700;letter-spacing:0;text-transform:none;color:var(--ink);line-height:1.3}
.acc>summary:hover>h2,.acc>summary:hover>h3{color:var(--accent)}
.acc>summary::after{content:"";flex:none;width:.5rem;height:.5rem;margin-right:.3rem;border-right:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:translateY(-.15rem) rotate(45deg);transition:transform .2s}
.acc[open]>summary::after{transform:translateY(.1rem) rotate(-135deg)}
.acc-body{max-width:70ch;line-height:1.65;padding:.15rem .35rem 1.3rem;display:flex;flex-direction:column;gap:.9rem}
.acc-body.block,.acc-body.prayer{border-top:0;padding-top:.15rem}
.acc-actions{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;font-family:var(--ui);font-size:.92rem}
.acc-copy{font:inherit;color:var(--muted);background:none;border:1px solid var(--line);border-radius:999px;padding:.3rem .8rem;cursor:pointer}
.acc-copy:hover{color:var(--accent);border-color:var(--accent)}
.acc-tools{position:sticky;top:var(--hdr,0px);z-index:4;background:var(--bg);padding:.65rem 0;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:.5rem;font-family:var(--ui)}
.acc-row{display:flex;flex-wrap:wrap;gap:.5rem}
.acc-row input{flex:1 1 12rem;min-width:0;font:inherit;font-size:1rem;padding:.5rem .7rem;border:1px solid var(--line);border-radius:4px;background:var(--surface);color:var(--ink)}
.acc-az{display:flex;gap:.3rem;overflow-x:auto;padding-bottom:.15rem}
.acc-az .chip{flex:none;min-width:2.25rem;padding:.25rem .55rem}
.acc-count{margin:0;font-size:.88rem;color:var(--muted)}
mark.acc-hit{background:#ffe08a;color:#17202a;border-radius:2px}
.acc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
details.acc,.acc [id]{scroll-margin-top:calc(var(--hdr,0px) + var(--tools,0px) + .75rem)}
@media (min-width:720px){.acc-az{flex-wrap:wrap;overflow:visible}}
@media (prefers-reduced-motion:reduce){.acc>summary,.acc>summary::after{transition:none}}
@media print{.acc-tools,.acc-copy,.acc>summary::after{display:none}}
"""
head = head.replace("</style>", EXTRA_CSS + "</style>", 1)
# CSS num arquivo próprio (/assets/site.css), que o navegador guarda entre uma página e outra
css_m = re.search(r"<style>\n?(.*?)</style>\n?", head, re.S)
SITE_CSS = css_m.group(1)
css_ver = hashlib.sha256(SITE_CSS.encode()).hexdigest()[:10]
# Calendário litúrgico (/assets/lit.js): vai no <head>, sem defer, para a cor do dia ser aplicada antes da primeira pintura
LIT_JS = (SRC / "lit.js").read_text(encoding="utf-8")
lit_ver = hashlib.sha256(LIT_JS.encode()).hexdigest()[:10]
head = head.replace(css_m.group(0), f'<link rel="stylesheet" href="/assets/site.css?v={css_ver}">\n')
head = head.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="theme-color" content="#2f6b45">\n'
    f'<script src="/assets/lit.js?v={lit_ver}"></script>\n'
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
SITE_JS = js_m.group(1) + r"""
/* ---------- Acordeões: busca, filtro A-Z, link direto (gerado pelo build.py) ---------- */
(function(){
var items=[].slice.call(document.querySelectorAll("details.acc"));
if(!items.length)return;
var root=document.documentElement,hdr=document.querySelector("header.site"),tools=document.querySelector(".acc-tools");
function sizes(){
  root.style.setProperty("--hdr",(hdr&&getComputedStyle(hdr).position==="sticky"?hdr.offsetHeight:0)+"px");
  root.style.setProperty("--tools",(tools?tools.offsetHeight:0)+"px");
}
sizes();addEventListener("resize",sizes);
function fold(s){var o="";for(var i=0;i<s.length;i++){var d=s[i].normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();o+=d.length===1?d:s[i].toLowerCase()}return o}
/* botão "Copiar link direto" dentro de cada item aberto */
function copyText(u,done){
  function old(){var t=document.createElement("textarea");t.value=u;t.setAttribute("readonly","");t.style.position="fixed";t.style.opacity="0";
    document.body.appendChild(t);t.select();try{document.execCommand("copy")}catch(e){}document.body.removeChild(t);done()}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(done,old);else old();
}
function actions(d){
  var b=d.querySelector(".acc-body");if(!d.id||!b||b.querySelector(".acc-copy"))return;
  var row=b.querySelector(".acc-actions");
  if(!row){row=document.createElement("div");row.className="acc-actions";b.appendChild(row)}
  var btn=document.createElement("button");btn.type="button";btn.className="acc-copy";btn.textContent="Copiar link direto";
  btn.addEventListener("click",function(){
    copyText(location.origin+location.pathname+"#"+d.id,function(){
      btn.textContent="Link copiado";setTimeout(function(){btn.textContent="Copiar link direto"},2000)});
  });
  row.appendChild(btn);
}
items.forEach(function(d){d.addEventListener("toggle",function(){if(d.open)actions(d)});if(d.open)actions(d)});
/* busca, letras, expandir e recolher */
var q,count,letter="",auto=[],data=items.map(function(d){return{d:d,l:d.getAttribute("data-l")||"",all:fold(d.textContent)}});
function unmark(){[].slice.call(document.querySelectorAll("mark.acc-hit")).forEach(function(m){var p=m.parentNode;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize()})}
function mark(el,nq){
  var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null),ns=[],n;
  while((n=w.nextNode()))if(!n.parentNode.closest(".acc-actions"))ns.push(n);
  ns.forEach(function(n){
    var s=n.nodeValue,f=fold(s),i=f.indexOf(nq),last=0,frag=null;
    while(i>=0){
      frag=frag||document.createDocumentFragment();
      frag.appendChild(document.createTextNode(s.slice(last,i)));
      var m=document.createElement("mark");m.className="acc-hit";m.textContent=s.slice(i,i+nq.length);frag.appendChild(m);
      last=i+nq.length;i=f.indexOf(nq,last);
    }
    if(frag){frag.appendChild(document.createTextNode(s.slice(last)));n.parentNode.replaceChild(frag,n)}
  });
}
function apply(){
  var nq=fold(q.value.trim()),shown=0;
  unmark();auto.forEach(function(d){d.open=false});auto=[];
  data.forEach(function(x){
    var ok=(!letter||x.l===letter)&&(!nq||x.all.indexOf(nq)>=0);
    x.d.hidden=!ok;if(!ok)return;shown++;
    if(nq.length>1){mark(x.d,nq);if(!x.d.open){x.d.open=true;auto.push(x.d)}}
  });
  [].slice.call(document.querySelectorAll("div.cat-h")).forEach(function(g){if(g.querySelector("details.acc"))g.hidden=!g.querySelector("details.acc:not([hidden])")});
  count.textContent="Mostrando "+shown+" de "+items.length+(items.length===1?" item":" itens");
}
function reset(){
  if(!tools)return;q.value="";letter="";
  [].forEach.call(tools.querySelectorAll("[data-l]"),function(x){x.setAttribute("aria-pressed",x.getAttribute("data-l")===""?"true":"false")});
  apply();
}
if(tools){
  q=tools.querySelector("input");count=tools.querySelector(".acc-count");
  var tm;q.addEventListener("input",function(){clearTimeout(tm);tm=setTimeout(apply,120)});
  tools.addEventListener("click",function(e){
    var b=e.target.closest("button");if(!b)return;
    if(b.hasAttribute("data-l")){
      letter=b.getAttribute("data-l");
      [].forEach.call(tools.querySelectorAll("[data-l]"),function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});
      apply();
    }else if(b.hasAttribute("data-acc")){
      var o=b.getAttribute("data-acc")==="open";items.forEach(function(d){if(!d.hidden)d.open=o});auto=[];
    }
  });
}
/* link direto: /pagina/#item abre o item e rola até ele */
function go(smooth){
  var id;try{id=decodeURIComponent(location.hash.slice(1))}catch(e){return}
  var t=id&&document.getElementById(id);if(!t)return;
  for(var e=t;e;e=e.parentElement)if(e.hidden){reset();break}
  for(e=t;e;e=e.parentElement)if(e.tagName==="DETAILS")e.open=true;
  smooth=smooth&&!matchMedia("(prefers-reduced-motion: reduce)").matches;
  requestAnimationFrame(function(){sizes();t.scrollIntoView({behavior:smooth?"smooth":"auto",block:"start"})});
}
addEventListener("hashchange",function(){go(true)});
go(false);
/* ao abrir a página por um link direto, confere a posição de novo depois que fontes e imagens carregam */
if(location.hash)addEventListener("load",function(){setTimeout(function(){go(true)},50)});
/* impressão: imprime tudo aberto */
addEventListener("beforeprint",function(){items.forEach(function(d){if(!d.open){d.open=true;d.setAttribute("data-print","")}})});
addEventListener("afterprint",function(){items.forEach(function(d){if(d.hasAttribute("data-print")){d.open=false;d.removeAttribute("data-print")}})});
})();
"""
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
# apresentação curta de cada livro (página /biblia/<livro>/)
BOOK_INTRO = json.loads((SRC / "biblia_intro.json").read_text(encoding="utf-8"))
assert set(BOOK_INTRO) == {b["s"] for b in BOOKS}, f"biblia_intro.json não bate com os livros: {set(BOOK_INTRO) ^ {b['s'] for b in BOOKS}}"
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

# ---------------------------------------------------------------- Frase do dia a partir do Evangelho da Missa
# Para cada dia, a API pública liturgia.up.railway.app (dados da liturgia diária da CNBB) diz qual é o Evangelho.
# O build escolhe nele um versículo dito por Jesus (ou por Maria) e guarda só a citação em
# _src/frase_liturgia.json; o texto vem da Bíblia do site (Matos Soares), não do Lecionário (direitos da CNBB).
# O resultado vai para /assets/frase-do-dia/AAAA-MM.json, que a página inicial lê; sem o dia no arquivo,
# fica a frase da lista (Q). Os dias novos (até FRASE_DIAS à frente) são buscados a cada build;
# para pular a busca, rode com CATHOLICAM_SEM_LITURGIA=1.
LIT_API = "https://liturgia.up.railway.app/v2/?dia={d}&mes={m}&ano={a}"
FRASE_DIAS = 400
frase_file = SRC / "frase_liturgia.json"
VERSE_MARK = re.compile(r"(\d{1,3})[a-d]?(?=[“‘\"A-ZÀ-ÖØ-Þa-zà-öø-ÿ—–])")
QUOTE_KEYS = re.compile(r"vos digo|eu sou|bem-aventurad|reino|meu pai|vosso pai|\bamor\b|\bamai|\bfé\b|vida eterna|"
                        r"\bsenhor\b|\bdeus\b|\bpaz\b|perdo|misericórdia|\bluz\b|salv|\bcrê|segue-me|permanec", re.I)
CONJ = re.compile(r"^(Mas|Pois|Porque|Porém|E|Então|Portanto|Por isso|Assim|Ora|Que|Também|Contudo|Todavia|Logo|Já)\b")
NAO_NOMES = {"Jesus", "Deus", "Senhor", "Espírito", "Santo", "Templo", "Reino", "Pai", "Filho", "Homem", "Lei", "Escritura",
             "Escrituras", "Naquele", "Naqueles", "Em", "Na", "No", "Nesse", "Neste", "Diante", "Depois", "Então", "Quando",
             "Ao", "Os", "As", "O", "A", "E", "Mas", "Por", "Ele", "Eles", "Enquanto", "Tendo", "Vendo", "Ouvindo", "Logo"}

FALA_V = (r"(?:disse|diz|dizia|dizendo|respondeu|respondia|perguntou|falou|falava|declarou|exclamou|ensinava|ensinou|"
          r"ordenou|replicou|acrescentou|rezou|orou|clamou|chamou|prosseguiu|continuou|explicou|advertiu|contou)")

def _sujeito(frase, nome):
    """O nome é quem fala: "Jesus disse", "Jesus lhe respondeu", "disse-lhes Jesus", "Maria, então, disse"."""
    n = r"\b" + nome + r"\b(?:,\s*(?:então|porém|logo|depois),)?"
    return re.search(r"(?<!\ba )(?<!\bde )(?<!\bao )(?<!\bcom )(?<!\bpara )(?<!\bviu )(?<!\bque )" + n + r"[^,.;:!?]{0,45}?\b" + FALA_V + r"\b", frase) \
        or re.search(r"\b" + FALA_V + r"(?:-(?:lhes?|o|a|os|as))?\s+" + nome + r"\b", frase)

def _inicia(frase, nome):
    """A frase começa com o nome como sujeito ("Jesus foi...", "Naquele tempo, Jesus...", "Então Jesus...")."""
    return re.match(r"\s*(?:[^,]{0,25},\s*)?(?:Então\s+|E\s+|Depois\s+)?" + nome + r"\b(?!,)", frase)

def _nomes(frase):
    """Nomes próprios no meio da frase (a primeira palavra não conta: é maiúscula por começar a frase)."""
    frase = frase.strip()
    return [m.group() for m in re.finditer(r"\b[A-ZÀ-Ý][a-zà-ÿ]+", frase) if m.start() > 0 and m.group() not in NAO_NOMES]

def _falante(antes):
    """Quem fala na citação que começa depois do texto `antes` (desde a última fala)."""
    antes = VERSE_MARK.sub(" ", antes)
    frases = [f for f in re.split(r"(?<=[.!?])\s+", antes.strip()) if f]
    ultima = frases[-1] if frases else ""
    for nome, rot in (("Jesus", "Jesus Cristo"), ("Maria", "Maria")):
        if _sujeito(ultima, nome): return rot
    nomes = _nomes(ultima)
    if not nomes and re.search(r"\b(ele|disse|respondeu|dizia|falou|declarou|ensinava)\b", ultima, re.I):
        outros = [w for f in frases for w in _nomes(f)]
        if any(_inicia(f, "Jesus") for f in frases) and not outros: return "Jesus Cristo"
    return None

def _versiculos(ref, texto):
    """Divide o texto da CNBB em [(capítulo, versículo, quem fala, fração do versículo na fala, tem citação dentro)]."""
    m = re.match(r"\s*(Mt|Mc|Lc|Jo)\s*(\d+)\s*,\s*(\d+)", ref)
    if not m: return None, []
    livro, cap, prev = m.group(1), int(m.group(2)), int(m.group(3))
    aspas = iter("“”" * texto.count('"'))
    texto = re.sub('"', lambda _: next(aspas), texto)  # alguns dias vêm com aspas retas
    sem_aspas = "“" not in texto
    marks = list(VERSE_MARK.finditer(texto))
    out, fala, ultimo_fim = [], None, 0
    for i, mk in enumerate(marks):
        v, s1 = int(mk.group(1)), mk.end()
        fim = marks[i + 1].start() if i + 1 < len(marks) else len(texto)
        if v < prev: cap += 1
        prev = v
        conta = {}
        for k in range(s1, fim):
            ch = texto[k]
            if ch == "“":
                fala = _falante(texto[ultimo_fim:k]) or "?"
            elif ch == "”":
                fala, ultimo_fim = None, k + 1
            elif fala and not ch.isspace():
                conta[fala] = conta.get(fala, 0) + 1
        tot = max(1, sum(1 for ch in texto[s1:fim] if not ch.isspace()))
        if sem_aspas: quem, frac = "Evangelho", 1.0
        elif len(conta) == 1 and next(iter(conta.values())) >= 15: quem, frac = next(iter(conta)), next(iter(conta.values())) / tot
        else: quem, frac = None, 0
        out.append((cap, v, quem if quem in ("Jesus Cristo", "Maria", "Evangelho") else None, frac, "‘" in texto[s1:fim]))
    return livro, out

def _limpa_ms(t):
    """Texto de um versículo da Bíblia do site, só com a fala."""
    t = re.sub(r"\s*\(ver nota\)", "", t).replace(" :", ":").strip()
    if t.count('"') == 1 and re.search(r':\s*"', t): t = t.split('"', 1)[1]
    elif t.count('"') == 2 and re.search(r':\s*"', t): t = t.split('"')[1]
    elif t.count('"') == 1 and t.rstrip().endswith('"'): t = t.rstrip()[:-1]
    elif t.count('"') == 1 and not re.search(r':\s*"', t): t = t.split('"')[0]
    elif '"' in t: return None
    t = re.sub(r"\s+", " ", t).strip()
    if t and t[-1] in ",;:": t = t[:-1] + "."
    return t

def escolhe_frase(evs):
    """Recebe [(referência, texto)] do Evangelho e devolve {"r": "Lc 21,3", "a": "Jesus Cristo"} ou None."""
    if not evs: return None
    livro, vs = _versiculos(*evs[0])
    if not livro: return None
    b = ABBR[livro]
    melhor, nota = None, -99
    for c, v, quem, frac, aninh in vs:
        if not quem or not (1 <= c <= len(b["caps"])): continue
        ms = dict(b["caps"][c - 1]).get(v)
        if frac < 0.5 and not (ms and re.search(r':\s*"', ms)): continue  # a fala é só parte do versículo e a Bíblia do site não a separa
        t = ms and _limpa_ms(ms)
        if not t or len(t) < 15 or len(t) > 200 or not t[0].isupper(): continue
        n = (2 if 40 <= len(t) <= 160 else 0) + min(3, len(QUOTE_KEYS.findall(t)))
        if t.endswith("?"): n -= 3
        if CONJ.match(t): n -= 2
        if aninh or "'" in t: n -= 3
        if re.search(r"\b" + FALA_V + r"\b", t): n -= 3  # narração dentro da fala (parábola: "e ele respondeu...")
        if quem == "Evangelho":
            if len(QUOTE_KEYS.findall(t)) < 2 or "Jesus" in t: continue  # sem falas no texto: só versículos de conteúdo, não narração
            n -= 1
        if n > nota: melhor, nota = {"r": f"{livro} {c},{v}", "a": quem}, n
    return melhor

def _busca(dia):
    url_api = LIT_API.format(d=dia.day, m=dia.month, a=dia.year)
    req = urllib.request.Request(url_api, headers={"User-Agent": "Catholicam-build/1.0"})
    for tentativa in range(3):
        try:
            j = json.loads(urllib.request.urlopen(req, timeout=25).read().decode("utf-8"))
            return [(e["referencia"], e["texto"]) for e in (j.get("leituras") or {}).get("evangelho") or []]
        except Exception:
            if tentativa == 2: raise

FRASE_VERSAO = 3  # mude ao alterar escolhe_frase(): o build busca tudo de novo
FRASE_CACHE = json.loads(frase_file.read_text(encoding="utf-8")) if frase_file.exists() else {}
if FRASE_CACHE.pop("versao", None) != FRASE_VERSAO: FRASE_CACHE = {}
_hoje = datetime.date.today()
_dias = [_hoje + datetime.timedelta(i) for i in range(-3, FRASE_DIAS)]
_falta = [d for d in _dias if d.isoformat() not in FRASE_CACHE]
if _falta and not __import__("os").environ.get("CATHOLICAM_SEM_LITURGIA"):
    from concurrent.futures import ThreadPoolExecutor
    def _um(d):
        try: return d, escolhe_frase(_busca(d)), True
        except Exception: return d, None, False
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(_um, _falta))
    falhas = 0
    for d, fr, ok in res:
        if ok: FRASE_CACHE[d.isoformat()] = fr
        else: falhas += 1
    print(f"Frase do dia: {len(_falta) - falhas} dias buscados na liturgia" + (f", {falhas} falharam (tenta de novo no próximo build)" if falhas else ""))
_corte = (_hoje - datetime.timedelta(40)).isoformat()
FRASE_CACHE = {k: FRASE_CACHE[k] for k in sorted(FRASE_CACHE) if k >= _corte}
frase_file.write_text(json.dumps({"versao": FRASE_VERSAO, **FRASE_CACHE}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
FRASES_MES = {}
for k, fr in FRASE_CACHE.items():
    if not fr: continue
    m = REF_RE.fullmatch(fr["r"])
    b, c, v = ABBR[m.group(1)], int(m.group(2)), int(m.group(3))
    t = _limpa_ms(dict(b["caps"][c - 1])[v])
    FRASES_MES.setdefault(k[:7], {})[str(int(k[8:]))] = {"q": t, "a": fr["a"], "r": fr["r"], "u": burl(b, c) + f"#v{v}"}

# ---------------------------------------------------------------- conteúdo pré-montado
def prayer_article(k, link=True, tag="h3", title=None):
    p = P[k]
    t = f'<a href="{purl(k)}">{esc(p["t"])}</a>' if link else esc(title or p["t"])
    r = f'<p class="r">{esc(p["r"])}</p>' if p.get("r") else ""
    return f'<article class="prayer"><{tag}>{t}</{tag}>{r}<p>{esc(p["x"])}</p></article>'

def initial(t):
    """Letra inicial do título, sem acento (usada no filtro A-Z)."""
    m = re.search(r"[a-z]", slugify(t))
    return m.group(0).upper() if m else "#"

def prayer_acc(k):
    """Oração da lista em acordeão: o texto completo fica no HTML, só recolhido."""
    p = P[k]
    r = f'<p class="r">{esc(p["r"])}</p>' if p.get("r") else ""
    return (f'<details class="acc" id="{PRAYERS[k]}" data-l="{initial(p["t"])}"><summary><h3>{esc(p["t"])}</h3></summary>'
            f'<div class="acc-body prayer">{r}<p>{esc(p["x"])}</p>'
            f'<p class="acc-actions"><a href="{purl(k)}">Origem, quando rezar e latim</a></p></div></details>')

prayers_html = "".join(
    f'<div class="stack cat-h"><h2>{esc(g[0])}</h2>' + "".join(prayer_acc(k) for k in g[1]) + "</div>" for g in GROUPS)

def qfig(q):
    return f'<figure class="quote"><blockquote>{esc(q[1])}</blockquote><figcaption><b>{esc(q[0])}</b> · {linkify(esc(q[2]))}</figcaption></figure>'
QG = [("Palavras de Jesus", lambda q: q[0] == "Jesus Cristo"), ("Palavras de Maria", lambda q: q[0] == "Maria"),
      ("Palavras dos santos", lambda q: q[0] not in ("Jesus Cristo", "Maria"))]
quotes_html = "".join(f'<details class="acc cat-h" id="{slugify(n)}" data-l="{initial(n)}"><summary><h2>{n}</h2></summary>'
                      '<div class="acc-body">' + "".join(qfig(q) for q in Q if f(q)) + "</div></details>" for n, f in QG)

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
        if body[max(0, m.start() - 9):m.start()] == "<summary>": return m.group(0)  # título de acordeão: o id fica no <details>
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

# acordeões: cada bloco de primeiro nível que começa com <h2> vira <details><summary><h2>…</h2></summary>.
# O texto não muda e continua no HTML (só recolhido), então o Google lê tudo. Blocos interativos
# (terço guiado, calendário, liturgia, Pix, busca da Bíblia) continuam abertos como antes.
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "col", "area", "embed", "track"}
TAG_RE = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>", re.S)
def top_children(s):
    out, depth, start = [], 0, None
    for m in TAG_RE.finditer(s):
        if not m.group(2) or m.group(2).lower() in VOID or m.group(3): continue
        if m.group(1):
            depth -= 1
            if depth == 0: out.append((start, m.end()))
        else:
            if depth == 0: start = m.start()
            depth += 1
    assert depth == 0, "HTML desbalanceado"
    return out
LIVE_IDS = set(re.findall(r'\$\("([\w-]+)"\)', footer_script)) - {"about-oracoes", "via-sacra", "q-erradas"}
INTERACTIVE = re.compile(r"<(button|input|iframe|select|textarea|canvas|form)\b|" +
                         r'id="(' + "|".join(map(re.escape, sorted(LIVE_IDS))) + ')"')
BLOCK_RE = re.compile(r'<div([^>]*)>\s*<h2([^>]*)>(.*?)</h2>', re.S)
ACC_RE = re.compile(r'<details class="acc[^"]*" id="([^"]+)"[^>]*><summary>(.*?)</summary>(.*?)</details>', re.S)

def acc_toolbar(letters, n):
    az = "".join(f'<button type="button" class="chip" data-l="{l}" aria-pressed="false">{l}</button>' for l in letters)
    return ('<div class="acc-tools" role="search" aria-label="Buscar e filtrar nesta página">'
            '<div class="acc-row"><label class="acc-sr" for="acc-q">Buscar nesta página</label>'
            '<input id="acc-q" type="search" placeholder="Buscar nesta página" autocomplete="off" enterkeyhint="search">'
            '<button type="button" class="chip" data-acc="open">Expandir tudo</button>'
            '<button type="button" class="chip" data-acc="close">Recolher tudo</button></div>'
            + ('<div class="acc-az" role="group" aria-label="Filtrar pela letra inicial">'
               f'<button type="button" class="chip" data-l="" aria-pressed="true">Todas</button>{az}</div>' if len(letters) > 1 else "")
            + f'<p class="acc-count" aria-live="polite">Mostrando {n} de {n} itens</p></div>')

def accordionize(sec, path, min_items=3):
    """Devolve (seção com acordeões e barra de busca, ItemList para o JSON-LD ou None)."""
    o, c = sec.index(">", sec.index("<section")) + 1, sec.rindex("</section>")
    inner, out, last = sec[o:c], [], 0
    spans = top_children(inner)
    for a, b in spans:
        el = inner[a:b]
        m = BLOCK_RE.match(el)
        if not m or INTERACTIVE.search(el) or "<h1" in el: continue
        attrs, h2a, h2in = m.group(1), m.group(2), m.group(3)
        assert not re.sub(r'\s*(class|id)="[^"]*"', "", attrs).strip(), attrs
        cls = (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1]
        did = re.search(r'id="([^"]*)"', attrs)
        hid = re.search(r' id="([^"]*)"', h2a)
        if did: aid = did.group(1)
        elif hid: aid, h2a = hid.group(1), h2a.replace(hid.group(0), "")
        else: aid = slugify(text(h2in))
        rest = el[m.end():el.rindex("</div>")]
        out.append(inner[last:a] + f'<details class="acc" id="{aid}" data-l="{initial(text(h2in))}">'
                   f'<summary><h2{h2a}>{h2in}</h2></summary><div class="{(cls + " acc-body").strip()}">{rest}</div></details>')
        last = b
    new = inner[:0] + "".join(out) + inner[last:]
    found = ACC_RE.findall(new)
    if len(found) < min_items: return sec, None
    ids = [i for i, _, _ in found]
    assert len(set(ids)) == len(ids), f"ids repetidos em {path}"
    letters = sorted({initial(text(s)) for _, s, _ in found} - {"#"})
    first = top_children(new)[0][1]  # depois do bloco do título (h1)
    new = new[:first] + acc_toolbar(letters, len(found)) + new[first:]
    ld = {"@type": "ItemList", "name": "Tópicos desta página", "numberOfItems": len(found), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {
            "@type": "CreativeWork", "@id": BASE + path + "#" + aid, "url": BASE + path + "#" + aid,
            "name": text(s), "text": re.sub(r"\s+", " ", text(re.sub(r"<br\s*/?>|</p>|</li>|</td>", " ", body))).strip()}}
        for i, (aid, s, body) in enumerate(found)]}
    return sec[:o] + new + sec[c:], ld

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
        title = full_title(title)
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
    if v != "inicio":
        sec, acc_ld = accordionize(sec, url(v))
        if acc_ld and v != "oracoes":  # /oracoes/ já tem a ItemList com o endereço de cada oração
            ld["@graph"].append(acc_ld)
    ph = page_head(title, desc, url(v), ld, legacy if v == "inicio" else "")
    if v == "sugestoes":
        assert ph.count('<meta charset="utf-8">') == 1 and "<script>" not in ph and " style=" not in sec + header_f + script_noqr
        ph = ph.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + SUG_CSP, 1)
    pages[url(v)] = (ph + "</head>\n<body>" + header_f
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
    if info.get("junto"):  # orações rezadas em sequência (ex.: Glória ao Pai e Ó meu Jesus no terço)
        j = info["junto"]
        more += (f'<div class="stack"><h2 id="{slugify(j["h2"])[:60]}">{esc(j["h2"])}</h2><p>{linkify(esc(j["intro"]))}</p>'
                 + "".join(prayer_article(s, link=s != k) for s in j["ordem"]) + "</div>\n")
    for nome_v, texto_v in info.get("versoes", []):
        more += (f'<div class="stack"><h2>{esc(p["t"])}: {esc(nome_v.lower() if nome_v.startswith("Versão") else nome_v)}</h2>'
                 f'<article class="prayer">{prayer_text(texto_v)}</article></div>\n')
    more += ('<div class="stack"><h2 id="historia">Origem e história</h2>'
             + "".join(f"<p>{linkify(esc(t))}</p>" for t in info["historia"])
             + f'<p><b>Quando rezar:</b> {esc(info["quando"])}</p></div>\n')
    if info.get("latim"):
        more += ('<div class="stack"><h2 id="latim">Em latim</h2>'
                 f'<p class="latin" lang="la">{esc(info["latim"]).replace(chr(10), "<br>")}</p></div>\n')
    if info.get("faq"):
        more += ('<div class="stack"><h2 id="perguntas">Perguntas frequentes</h2>'
                 + "".join(f"<h3>{esc(q)}</h3><p>{linkify(esc(a))}</p>" for q, a in info["faq"]) + "</div>\n")
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
    if info.get("faq"):
        ld["@graph"].append({"@type": "FAQPage", "@id": BASE + path + "#perguntas", "inLanguage": "pt-BR", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in info["faq"]]})
    pages[path] = (page_head(full_title(info["titulo"]), desc, path, ld) + "</head>\n<body>" + header_f
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
            f'Em cada mistério se reza um <a href="{purl("pai")}">Pai Nosso</a>, dez <a href="{purl("ave")}">Ave-Marias</a>, '
            f'um <a href="{purl("gloria")}">Glória ao Pai</a> e o <a href="{purl("fatima")}">Ó meu Jesus</a>, contemplando a passagem do Evangelho.</p>'
            f'<p><a class="btn" href="/terco/">Rezar o terço guiado</a></p></div>\n'
            + items +
            f'<div class="stack"><h2 id="outros">Outros mistérios</h2><p>{outros}</p></div>\n</section>')
    body = add_toc(body)
    body, acc_ld = accordionize(body, path)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": f"Mistérios {nome}", "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"}},
        crumbs_ld([("Início", "/"), ("Terço", "/terco/"), (f"Mistérios {nome}", path)])] + ([acc_ld] if acc_ld else [])}
    pages[path] = (page_head(full_title(title), desc, path, ld) + "</head>\n<body>" + header_f
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
    caps_txt = "capítulo" if nch == 1 else "capítulos"
    intro = BOOK_INTRO[b["s"]]
    desc = short(f"{b['n']} na Bíblia católica online, {nch} {caps_txt}. {intro}", 155)
    # começo do livro (primeiros versículos), para a página não ser só a lista de capítulos
    inicio = "".join(f'<p><span class="vn">{n}</span>{esc(t)}</p>' for n, t in b["caps"][0][:3])
    viz = [x for x in BOOKS if x["g"] == b["g"] and x is not b]
    body = (f'<section class="view on" data-view="biblia-livro">\n'
            f'<nav class="crumb" aria-label="Caminho"><a href="/">Início</a> › <a href="/biblia/">Bíblia</a> › {esc(b["n"])}</nav>\n'
            f'<div class="stack"><h1>{esc(b["n"])}</h1><p class="lede">{esc(b["g"])} · {nch} {caps_txt}</p>'
            f'<p>{esc(intro)}</p><p><a class="btn" href="{burl(b, 1)}">Começar a ler: {esc(cap_name(b, 1))}</a></p></div>\n'
            f'<div class="stack"><h2 id="capitulos">Capítulos</h2>{grid}</div>\n'
            f'<div class="stack"><h2 id="inicio-do-livro">Como começa</h2><div class="passage">{inicio}</div>'
            f'<p class="r">{BIBLIA_TRAD[0].upper() + BIBLIA_TRAD[1:]}. <a href="{burl(b, 1)}">Continuar a leitura</a></p></div>\n'
            f'<div class="stack"><h2 id="outros-livros">Outros livros: {esc(b["g"].split(" · ")[-1])}</h2><div class="books">'
            + "".join(f'<a class="book" href="{burl(x)}"><span>{esc(x["n"])}</span><small>{len(x["caps"])}</small></a>' for x in viz)
            + '</div></div>\n'
            f'<p><a href="/biblia/">Todos os livros da Bíblia</a></p>\n</section>')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": b["n"], "url": BASE + path, "description": desc, "inLanguage": "pt-BR", "isPartOf": {"@id": BASE + "/#site"},
         "about": {"@type": "Book", "name": b["n"], "isPartOf": {"@type": "Book", "name": "Bíblia Sagrada"}}},
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
(assets / "lit.js").write_text(LIT_JS, encoding="utf-8")
(assets / "biblia.json").write_text(json.dumps(
    [{"n": b["n"], "s": b["s"], "c": [[[n, t] for n, t in cap] for cap in b["caps"]]} for b in BOOKS],
    ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
(ROOT / "404.html").write_text(nf_html, encoding="utf-8")
fd = assets / "frase-do-dia"
fd.mkdir(exist_ok=True)
for f in fd.glob("*.json"):
    if f.stem not in FRASES_MES: f.unlink()
for mes, dias in FRASES_MES.items():
    (fd / f"{mes}.json").write_text(json.dumps(dias, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

# lastmod só muda quando o conteúdo da página muda
lm_file = SRC / "lastmod.json"
lm = json.loads(lm_file.read_text()) if lm_file.exists() else {}
today = datetime.date.today().isoformat()
# (a versão dos arquivos comuns, ?v=..., não conta: mudar o CSS ou o JS não muda o conteúdo da página)
for path, content in pages.items():
    h = hashlib.sha256(re.sub(r"\?v=[0-9a-f]{10}", "", content).encode()).hexdigest()[:16]
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
