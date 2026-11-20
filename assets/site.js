(function(){
"use strict";
var $=function(id){return document.getElementById(id)||document.createElement("div")};

/* ---------- Orações ---------- */
var P={
 sinal:{t:"Sinal da Cruz",x:"Em nome do Pai, do Filho e do Espírito Santo. Amém."},
 pai:{t:"Pai Nosso",x:"Pai nosso que estais nos céus, santificado seja o vosso nome; venha a nós o vosso reino, seja feita a vossa vontade, assim na terra como no céu.\nO pão nosso de cada dia nos dai hoje; perdoai-nos as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém."},
 ave:{t:"Ave Maria",x:"Ave Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus.\nSanta Maria, Mãe de Deus, rogai por nós, pecadores, agora e na hora de nossa morte. Amém."},
 gloria:{t:"Glória ao Pai",x:"Glória ao Pai, ao Filho e ao Espírito Santo.\nComo era no princípio, agora e sempre. Amém."},
 credo:{t:"Credo (Símbolo dos Apóstolos)",x:"Creio em Deus Pai todo-poderoso, criador do céu e da terra; e em Jesus Cristo, seu único Filho, nosso Senhor; que foi concebido pelo poder do Espírito Santo; nasceu da Virgem Maria; padeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado; desceu à mansão dos mortos; ressuscitou ao terceiro dia; subiu aos céus, está sentado à direita de Deus Pai todo-poderoso, donde há de vir a julgar os vivos e os mortos.\nCreio no Espírito Santo, na santa Igreja Católica, na comunhão dos santos, na remissão dos pecados, na ressurreição da carne, na vida eterna. Amém."},
 salve:{t:"Salve Rainha",x:"Salve, Rainha, Mãe de misericórdia, vida, doçura e esperança nossa, salve! A vós bradamos, os degredados filhos de Eva; a vós suspiramos, gemendo e chorando neste vale de lágrimas.\nEia, pois, advogada nossa, esses vossos olhos misericordiosos a nós volvei; e depois deste desterro mostrai-nos Jesus, bendito fruto do vosso ventre, ó clemente, ó piedosa, ó doce sempre Virgem Maria.\nRogai por nós, santa Mãe de Deus, para que sejamos dignos das promessas de Cristo. Amém."},
 fatima:{t:"Ó meu Jesus",x:"Ó meu Jesus, perdoai-nos, livrai-nos do fogo do inferno, levai as almas todas para o céu e socorrei principalmente as que mais precisarem."},
 anjo:{t:"Santo Anjo",x:"Santo Anjo do Senhor, meu zeloso guardador, se a ti me confiou a piedade divina, sempre me rege, me guarda, me governa e me ilumina. Amém."},
 contricao:{t:"Ato de Contrição",x:"Meu Deus, eu me arrependo de todo o coração de vos ter ofendido, porque sois tão bom e amável. Prometo, com a vossa graça, nunca mais pecar. Meu Jesus, misericórdia!"},
 espirito:{t:"Vinde, Espírito Santo",x:"Vinde, Espírito Santo, enchei os corações dos vossos fiéis e acendei neles o fogo do vosso amor. Enviai o vosso Espírito e tudo será criado, e renovareis a face da terra.\nOremos: Ó Deus, que instruístes os corações dos vossos fiéis com a luz do Espírito Santo, fazei que apreciemos retamente todas as coisas segundo o mesmo Espírito e gozemos sempre da sua consolação. Por Cristo, Senhor nosso. Amém."},
 miguel:{t:"São Miguel Arcanjo",x:"São Miguel Arcanjo, defendei-nos no combate, sede o nosso refúgio contra as maldades e ciladas do demônio. Ordene-lhe Deus, instantemente o pedimos, e vós, príncipe da milícia celeste, pela virtude divina, precipitai no inferno a Satanás e aos outros espíritos malignos que andam pelo mundo para perder as almas. Amém."}
};
P.angelus={t:"Angelus (O Anjo do Senhor)",r:"Reza-se às 6h, ao meio-dia e às 18h, fora do Tempo Pascal.",x:"℣. O anjo do Senhor anunciou a Maria.\n℟. E ela concebeu do Espírito Santo.\nAve Maria…\n\n℣. Eis aqui a serva do Senhor.\n℟. Faça-se em mim segundo a vossa palavra.\nAve Maria…\n\n℣. E o Verbo se fez carne.\n℟. E habitou entre nós.\nAve Maria…\n\n℣. Rogai por nós, santa Mãe de Deus.\n℟. Para que sejamos dignos das promessas de Cristo.\n\nOremos: Infundi, Senhor, a vossa graça em nossas almas, para que nós, que pela anunciação do anjo conhecemos a encarnação de Cristo, vosso Filho, pela sua paixão e cruz sejamos conduzidos à glória da ressurreição. Pelo mesmo Cristo, Senhor nosso. Amém."};
P.regina={t:"Rainha do Céu (Regina Caeli)",r:"Substitui o Angelus no Tempo Pascal.",x:"Rainha do céu, alegrai-vos, aleluia.\nPorque aquele que merecestes trazer em vosso seio, aleluia.\nRessuscitou como disse, aleluia.\nRogai a Deus por nós, aleluia.\n\n℣. Alegrai-vos e exultai, ó Virgem Maria, aleluia.\n℟. Porque o Senhor ressuscitou verdadeiramente, aleluia.\n\nOremos: Ó Deus, que vos dignastes alegrar o mundo com a ressurreição do vosso Filho, Jesus Cristo, Senhor nosso, concedei-nos, vos suplicamos, que por sua Mãe, a Virgem Maria, alcancemos as alegrias da vida eterna. Por Cristo, Senhor nosso. Amém."};
P.lembrai={t:"Lembrai-vos",x:"Lembrai-vos, ó piíssima Virgem Maria, que nunca se ouviu dizer que algum daqueles que têm recorrido à vossa proteção, implorado a vossa assistência e reclamado o vosso socorro, fosse por vós desamparado.\nAnimado eu, pois, com igual confiança, a vós, ó Virgem entre todas singular, como a Mãe recorro, de vós me valho e, gemendo sob o peso dos meus pecados, me prostro a vossos pés. Não rejeiteis as minhas súplicas, ó Mãe do Filho de Deus humanado, mas dignai-vos de as ouvir propícia e de me alcançar o que vos rogo. Amém."};
P.protecao={t:"À vossa proteção",x:"À vossa proteção recorremos, santa Mãe de Deus; não desprezeis as nossas súplicas em nossas necessidades, mas livrai-nos sempre de todos os perigos, ó Virgem gloriosa e bendita. Amém."};
P.consagracao={t:"Consagração a Nossa Senhora",x:"Ó minha Senhora, ó minha Mãe, eu me ofereço todo a vós, e em prova da minha devoção para convosco, vos consagro neste dia meus olhos, meus ouvidos, minha boca, meu coração e inteiramente todo o meu ser. E porque assim sou vosso, ó incomparável Mãe, guardai-me e defendei-me como coisa e propriedade vossa. Amém."};
P.alma={t:"Alma de Cristo",r:"Tradicionalmente rezada depois da comunhão.",x:"Alma de Cristo, santificai-me.\nCorpo de Cristo, salvai-me.\nSangue de Cristo, inebriai-me.\nÁgua do lado de Cristo, lavai-me.\nPaixão de Cristo, confortai-me.\nÓ bom Jesus, ouvi-me.\nDentro de vossas chagas, escondei-me.\nNão permitais que eu me separe de vós.\nDo espírito maligno, defendei-me.\nNa hora da minha morte, chamai-me e mandai-me ir para vós, para que com vossos santos vos louve por todos os séculos dos séculos. Amém."};
var groups=[
 ["Orações de todo dia",["sinal","pai","ave","gloria","credo","anjo"]],
 ["A Nossa Senhora",["salve","angelus","regina","lembrai","protecao","consagracao"]],
 ["A Jesus Cristo",["alma","contricao","fatima"]],
 ["Ao Espírito Santo e aos anjos",["espirito","miguel"]]
];
var box=$("prayers"),cats=$("p-cats");
function jump(label,el){
  var c=document.createElement("button");c.type="button";c.className="chip";c.textContent=label;
  c.addEventListener("click",function(){el.scrollIntoView({block:"start"})});cats.appendChild(c);
}
if(box.querySelector(".cat-h"))Array.prototype.forEach.call(box.querySelectorAll(".cat-h"),function(w,i){jump(groups[i][0],w)});
else groups.forEach(function(g){
  var w=document.createElement("div");w.className="stack cat-h";
  var h=document.createElement("h2");h.textContent=g[0];w.appendChild(h);
  g[1].forEach(function(k){
    var a=document.createElement("article");a.className="prayer";
    var t=document.createElement("h3");t.textContent=P[k].t;a.appendChild(t);
    if(P[k].r){var r=document.createElement("p");r.className="r";r.textContent=P[k].r;a.appendChild(r)}
    var p=document.createElement("p");p.textContent=P[k].x;a.appendChild(p);w.appendChild(a);
  });
  box.appendChild(w);jump(g[0],w);
});
jump("Via-Sacra",$("via-sacra"));
jump("História das orações",$("about-oracoes"));

/* ---------- Terço ---------- */
var M={
 gozosos:{n:"Gozosos",m:[["A Anunciação do Anjo a Maria","Lc 1,26-38"],["A Visitação de Maria a Isabel","Lc 1,39-56"],["O Nascimento de Jesus em Belém","Lc 2,1-20"],["A Apresentação de Jesus no Templo","Lc 2,22-38"],["A perda e o encontro de Jesus no Templo","Lc 2,41-50"]]},
 luminosos:{n:"Luminosos",m:[["O Batismo de Jesus no Jordão","Mt 3,13-17"],["As Bodas de Caná","Jo 2,1-11"],["O anúncio do Reino de Deus","Mc 1,14-15"],["A Transfiguração do Senhor","Mt 17,1-8"],["A instituição da Eucaristia","Mt 26,26-28"]]},
 dolorosos:{n:"Dolorosos",m:[["A agonia de Jesus no Horto","Mt 26,36-46"],["A flagelação de Jesus","Jo 19,1"],["A coroação de espinhos","Mt 27,27-31"],["Jesus carrega a cruz até o Calvário","Lc 23,26-32"],["A crucifixão e morte de Jesus","Lc 23,33-46"]]},
 gloriosos:{n:"Gloriosos",m:[["A Ressurreição de Jesus","Mt 28,1-10"],["A Ascensão de Jesus ao céu","At 1,6-11"],["A vinda do Espírito Santo","At 2,1-13"],["A Assunção de Nossa Senhora","Tradição da Igreja"],["A coroação de Nossa Senhora","Ap 12,1"]]}
};
var byDay=["gloriosos","gozosos","dolorosos","gloriosos","luminosos","dolorosos","gozosos"];
var ord=["1º","2º","3º","4º","5º"];
var steps=[],pos=0,curSet="gozosos";
function build(set){
  var s=[];
  function add(k,rub,bead){s.push({t:P[k].t,x:P[k].x,r:rub||"",b:bead||null})}
  add("sinal","Início");add("credo","Segurando o crucifixo");add("pai","Primeira conta");
  for(var i=1;i<=3;i++)add("ave","Pela fé, pela esperança e pela caridade",[i,3]);
  add("gloria","");
  M[set].m.forEach(function(m,j){
    s.push({t:ord[j]+" mistério: "+m[0],x:"Contemple este mistério em silêncio por um instante.",r:m[1]});
    add("pai",ord[j]+" mistério");
    for(var i=1;i<=10;i++)add("ave",ord[j]+" mistério: "+m[0],[i,10]);
    add("gloria",ord[j]+" mistério");add("fatima",ord[j]+" mistério");
  });
  add("salve","Conclusão");add("sinal","Fim do terço");
  return s;
}
function draw(){
  var s=steps[pos];
  $("r-step").textContent="Mistérios "+M[curSet].n+" · passo "+(pos+1)+" de "+steps.length;
  $("r-title").textContent=s.t;$("r-rubric").textContent=s.r;$("r-text").textContent=s.x;
  var b=$("r-beads");b.textContent="";
  if(s.b){for(var i=1;i<=s.b[1];i++){var d=document.createElement("i");d.className="bead"+(i<=s.b[0]?" done":"");b.appendChild(d)}}
  $("r-bar").style.width=((pos+1)/steps.length*100)+"%";
  $("r-prev").disabled=pos===0;
  $("r-next").textContent=pos===steps.length-1?"Recomeçar":"Próxima conta";
}
function setSet(k){
  curSet=k;steps=build(k);pos=0;
  Array.prototype.forEach.call($("sets").children,function(c){c.setAttribute("aria-pressed",c.dataset.k===k?"true":"false")});
  draw();
}
Object.keys(M).forEach(function(k){
  var c=document.createElement("button");c.type="button";c.className="chip";c.dataset.k=k;c.textContent=M[k].n;
  c.addEventListener("click",function(){setSet(k)});$("sets").appendChild(c);
});
$("r-next").addEventListener("click",function(){pos=pos===steps.length-1?0:pos+1;draw()});
$("r-prev").addEventListener("click",function(){if(pos>0){pos--;draw()}});

/* ---------- Tempo litúrgico ---------- */
function D(y,m,d){return new Date(y,m,d,12)}
function addDays(dt,n){var x=new Date(dt);x.setDate(x.getDate()+n);return x}
function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return D(y,mo-1,da)}
function season(now){
  var y=now.getFullYear(),t=D(y,now.getMonth(),now.getDate()).getTime();
  var E=easter(y),ash=addDays(E,-46),pent=addDays(E,49);
  var d24=D(y,11,24),adv=addDays(d24,-d24.getDay()-21);
  var j2=D(y,0,2),epi=addDays(j2,(7-j2.getDay())%7),bap=addDays(epi,epi.getDate()>=7?1:7);
  if(t>=D(y,11,25).getTime()||t<=bap.getTime())return["Tempo do Natal","branco","Branco"];
  if(t>=adv.getTime())return["Tempo do Advento","roxo","Roxo"];
  if(t>=ash.getTime()&&t<addDays(E,-3).getTime())return["Tempo da Quaresma","roxo","Roxo"];
  if(t>=addDays(E,-3).getTime()&&t<E.getTime())return t===addDays(E,-2).getTime()?["Tríduo Pascal","vermelho","Vermelho"]:["Tríduo Pascal","branco","Branco"];
  if(t===pent.getTime())return["Domingo de Pentecostes","vermelho","Vermelho"];
  if(t>=E.getTime()&&t<pent.getTime())return["Tempo Pascal","branco","Branco"];
  return["Tempo Comum","verde","Verde"];
}
var now=new Date(),S=season(now),todaySet=byDay[now.getDay()];
if(S[1]!=="verde")document.documentElement.setAttribute("data-season",S[1]);
try{$("t-date").textContent=now.toLocaleDateString("pt-BR",{weekday:"long",day:"numeric",month:"long",year:"numeric"})}catch(e){}
$("t-season").textContent=S[0];$("t-color").textContent=S[2];$("t-myst").textContent=M[todaySet].n;
$("t-pray").addEventListener("click",function(){location.href="/terco/"});
setSet(todaySet);

/* ---------- Liturgia diária ---------- */
function advent(y){var d24=D(y,11,24);return addDays(d24,-d24.getDay()-21)}
function baptism(y){var j2=D(y,0,2),epi=addDays(j2,(7-j2.getDay())%7);return [epi,addDays(epi,epi.getDate()>=7?1:7)]}
function litYear(now){var y=now.getFullYear(),t=D(y,now.getMonth(),now.getDate());return t>=advent(y)?y+1:y}
function cycles(end){return [["C","A","B"][end%3],end%2?"I":"II"]}
var EVG={A:"Mateus",B:"Marcos",C:"Lucas"};
function litDay(now){
  var y=now.getFullYear(),t=D(y,now.getMonth(),now.getDate()),sun=t.getDay()===0,DAY=864e5;
  function wk(from){return Math.floor((t-from)/DAY/7)+1}
  function eq(d){return t.getTime()===d.getTime()}
  function lab(n,tempo,dom){return sun?n+"º Domingo "+dom:n+"ª Semana "+tempo}
  var E=easter(y),ash=addDays(E,-46),pent=addDays(E,49),adv=advent(y),ep=baptism(y),epi=ep[0],bap=ep[1];
  var W="branco",V="roxo",R="vermelho",G="verde";
  if(t>=D(y,11,25)||t<=bap){
    var x="Tempo do Natal",c=W,dd=t.getDate(),mm=t.getMonth();
    var hf=(function(){var yy=mm===11?y:y-1,n=D(yy,11,25);for(var i=1;i<=6;i++){var s=addDays(n,i);if(s.getDay()===0)return s}return D(yy,11,30)})();
    if(mm===11&&dd===25)x="Natal do Senhor";
    else if(mm===0&&dd===1)x="Santa Maria, Mãe de Deus";
    else if(eq(epi))x="Epifania do Senhor";
    else if(eq(bap))x="Batismo do Senhor";
    else if(eq(hf))x="Sagrada Família";
    else if(mm===11&&dd<=31)x="Oitava do Natal";
    return [x,"Tempo do Natal",c];
  }
  if(t>=adv){var n=wk(adv);return [lab(n,"do Advento","do Advento"),"Tempo do Advento",sun&&n===3?"roxo ou rosa":V]}
  if(t<ash){var b0=bap.getDay()===1?addDays(bap,-1):bap;return [lab(wk(b0),"do Tempo Comum","do Tempo Comum"),"Tempo Comum",G]}
  if(t<addDays(E,-3)){
    if(eq(ash))return ["Quarta-feira de Cinzas","Tempo da Quaresma",V];
    var l1=addDays(ash,4);if(t<l1)return ["Depois das Cinzas","Tempo da Quaresma",V];
    var q=wk(l1);
    if(q===6)return [sun?"Domingo de Ramos e da Paixão do Senhor":"Semana Santa","Tempo da Quaresma",sun?R:V];
    return [lab(q,"da Quaresma","da Quaresma"),"Tempo da Quaresma",sun&&q===4?"roxo ou rosa":V];
  }
  if(t<E){
    if(eq(addDays(E,-3)))return ["Quinta-feira Santa","Tríduo Pascal (à noite)",W];
    if(eq(addDays(E,-2)))return ["Sexta-feira da Paixão do Senhor","Tríduo Pascal",R];
    return ["Sábado Santo (à noite, Vigília Pascal)","Tríduo Pascal",W];
  }
  if(t<=pent){
    if(eq(E))return ["Domingo de Páscoa","Tempo Pascal",W];
    if(eq(pent))return ["Domingo de Pentecostes","Tempo Pascal",R];
    if(eq(addDays(E,42)))return ["Ascensão do Senhor","Tempo Pascal",W];
    var p=wk(E);
    if(p===1)return ["Oitava da Páscoa","Tempo Pascal",W];
    if(sun&&p===2)return ["2º Domingo da Páscoa (da Divina Misericórdia)","Tempo Pascal",W];
    return [lab(p,"da Páscoa","da Páscoa"),"Tempo Pascal",W];
  }
  var ck=addDays(adv,-7),s0=addDays(t,-t.getDay()),o=34-Math.round((ck-s0)/DAY/7);
  if(eq(addDays(pent,7)))return ["Santíssima Trindade","Tempo Comum",W];
  if(eq(addDays(pent,11)))return ["Corpo e Sangue de Cristo (Corpus Christi)","Tempo Comum",W];
  if(eq(addDays(pent,19)))return ["Sagrado Coração de Jesus","Tempo Comum",W];
  if(eq(ck))return ["Nosso Senhor Jesus Cristo, Rei do Universo","Tempo Comum",W];
  return [lab(o,"do Tempo Comum","do Tempo Comum"),"Tempo Comum",G];
}
(function(){
  var day=document.getElementById("l-day");if(!day)return;
  var L=litDay(now),cy=cycles(litYear(now));
  try{$("l-date").textContent=now.toLocaleDateString("pt-BR",{weekday:"long",day:"numeric",month:"long",year:"numeric"})}catch(e){}
  day.textContent=L[0];$("l-season").textContent=L[1];
  $("l-color").textContent=L[2].charAt(0).toUpperCase()+L[2].slice(1);
  $("l-sun").textContent="Ano "+cy[0]+" ("+EVG[cy[0]]+")";
  $("l-fer").textContent=cy[1]==="I"?"Ano ímpar (I)":"Ano par (II)";
  var tb=document.getElementById("l-cycles");
  if(tb){tb.textContent="";var y0=litYear(now);
    for(var y=y0;y<y0+4;y++){var c=cycles(y),a=advent(y-1),tr=document.createElement("tr");
      [(y-1)+"–"+y,("0"+a.getDate()).slice(-2)+"/"+("0"+(a.getMonth()+1)).slice(-2)+"/"+a.getFullYear(),"Ano "+c[0]+" ("+EVG[c[0]]+")",c[1]==="I"?"Ano I (ímpar)":"Ano II (par)"]
      .forEach(function(v){var td=document.createElement("td");td.textContent=v;tr.appendChild(td)});
      if(y===y0)tr.className="next";tb.appendChild(tr)}}
  /* Página oficial da CNBB: só é carregada quando a pessoa pede */
  var box=document.getElementById("cnbb-box"),btn=document.getElementById("cnbb-load"),auto=document.getElementById("cnbb-auto"),KEY="cath-cnbb";
  if(!box||!btn)return;
  function load(){
    if(document.getElementById("cnbb-frame"))return;
    var f=document.createElement("iframe");
    f.id="cnbb-frame";f.className="cnbb-frame";f.title="Liturgia diária da CNBB (site oficial)";
    f.src="https://liturgiadiaria.edicoescnbb.com.br/";
    f.setAttribute("sandbox","allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox");
    f.setAttribute("referrerpolicy","strict-origin-when-cross-origin");
    f.setAttribute("loading","lazy");
    btn.hidden=true;box.appendChild(f);
  }
  try{auto.checked=localStorage.getItem(KEY)==="1"}catch(e){}
  auto.addEventListener("change",function(){try{if(auto.checked)localStorage.setItem(KEY,"1");else localStorage.removeItem(KEY)}catch(e){}if(auto.checked)load()});
  btn.addEventListener("click",load);
  if(auto.checked)load();
})();

/* ---------- Calendário ---------- */
function movable(y){
  var E=easter(y),d24=D(y,11,24),adv=addDays(d24,-d24.getDay()-21);
  return [["Quarta-feira de Cinzas",addDays(E,-46)],["Domingo de Ramos",addDays(E,-7)],["Quinta-feira Santa",addDays(E,-3)],
   ["Sexta-feira Santa",addDays(E,-2)],["Domingo de Páscoa",E],["Ascensão do Senhor",addDays(E,42)],["Pentecostes",addDays(E,49)],
   ["Santíssima Trindade",addDays(E,56)],["Corpus Christi",addDays(E,60)],["Sagrado Coração de Jesus",addDays(E,68)],
   ["Cristo Rei",addDays(adv,-7)],["1º Domingo do Advento",adv]];
}
(function(){
  var today=D(now.getFullYear(),now.getMonth(),now.getDate()).getTime(),marked=false,cal=$("cal");
  [now.getFullYear(),now.getFullYear()+1].forEach(function(y){
    var w=document.createElement("div");w.className="stack";
    var h=document.createElement("h2");h.textContent="Datas móveis de "+y;w.appendChild(h);
    var t=document.createElement("table"),tb=document.createElement("tbody");
    movable(y).forEach(function(m){
      var tr=document.createElement("tr"),a=document.createElement("td"),b=document.createElement("td");
      a.className="dt";
      try{a.textContent=m[1].toLocaleDateString("pt-BR",{weekday:"short",day:"numeric",month:"short"})}catch(e){a.textContent=m[1].getDate()+"/"+(m[1].getMonth()+1)}
      b.textContent=m[0];
      if(m[1].getTime()<today)tr.className="past";
      else if(!marked){tr.className="next";marked=true;b.textContent=m[0]+" · próxima"}
      tr.appendChild(a);tr.appendChild(b);tb.appendChild(tr);
    });
    t.appendChild(tb);w.appendChild(t);cal.appendChild(w);
  });
})();

/* ---------- Bíblia ---------- */
var B=[
 ["Antigo Testamento · Pentateuco",[["Gênesis",50],["Êxodo",40],["Levítico",27],["Números",36],["Deuteronômio",34]]],
 ["Antigo Testamento · Livros históricos",[["Josué",24],["Juízes",21],["Rute",4],["1 Samuel",31],["2 Samuel",24],["1 Reis",22],["2 Reis",25],["1 Crônicas",29],["2 Crônicas",36],["Esdras",10],["Neemias",13],["Tobias",14],["Judite",16],["Ester",16],["1 Macabeus",16],["2 Macabeus",15]]],
 ["Antigo Testamento · Livros sapienciais",[["Jó",42],["Salmos",150],["Provérbios",31],["Eclesiastes",12],["Cântico dos Cânticos",8],["Sabedoria",19],["Eclesiástico",51]]],
 ["Antigo Testamento · Livros proféticos",[["Isaías",66],["Jeremias",52],["Lamentações",5],["Baruc",6],["Ezequiel",48],["Daniel",14],["Oseias",14],["Joel",3],["Amós",9],["Abdias",1],["Jonas",4],["Miqueias",7],["Naum",3],["Habacuc",3],["Sofonias",3],["Ageu",2],["Zacarias",14],["Malaquias",4]]],
 ["Novo Testamento · Evangelhos e Atos",[["Mateus",28],["Marcos",16],["Lucas",24],["João",21],["Atos dos Apóstolos",28]]],
 ["Novo Testamento · Cartas de São Paulo",[["Romanos",16],["1 Coríntios",16],["2 Coríntios",13],["Gálatas",6],["Efésios",6],["Filipenses",4],["Colossenses",4],["1 Tessalonicenses",5],["2 Tessalonicenses",3],["1 Timóteo",6],["2 Timóteo",4],["Tito",3],["Filêmon",1],["Hebreus",13]]],
 ["Novo Testamento · Cartas católicas e Apocalipse",[["Tiago",5],["1 Pedro",5],["2 Pedro",3],["1 João",5],["2 João",1],["3 João",1],["Judas",1],["Apocalipse",22]]]
];
/* Páginas da Bíblia: um endereço por livro (/biblia/<livro>/) e por capítulo (/biblia/<livro>/<n>/),
   geradas pelo build.py. Aqui ficam só a busca e o "continuar a leitura". */
(function(){
  var body=document.body,here=body.getAttribute("data-biblia");
  try{if(here)localStorage.setItem("cath-ler",JSON.stringify({u:location.pathname,t:here}))}catch(e){}
  var rs=document.getElementById("b-resume");
  if(rs){try{var l=JSON.parse(localStorage.getItem("cath-ler")||"null");
    if(l&&l.u){var a=document.createElement("a");a.href=l.u;a.textContent=l.t;rs.textContent="Continuar a leitura: ";rs.appendChild(a);rs.hidden=false}}catch(e){}}
  var form=document.getElementById("b-search");if(!form)return;
  var bible=null,loading=null;
  function norm(x){return x.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase()}
  function load(){
    if(bible)return Promise.resolve(bible);
    if(!loading)loading=fetch("/assets/biblia.json").then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){bible=d;return d});
    return loading;
  }
  form.addEventListener("submit",function(ev){
    ev.preventDefault();
    var q=norm($("b-q").value.trim()),out=$("b-results"),cnt=$("b-count");out.textContent="";
    if(q.length<3){cnt.textContent="Digite pelo menos 3 letras.";return}
    cnt.textContent="Buscando…";
    load().then(function(d){
      var total=0,max=60;
      d.forEach(function(bk){bk.c.forEach(function(vs,c){vs.forEach(function(v){
        if(norm(v[1]).indexOf(q)<0)return;
        total++;if(total>max)return;
        var a=document.createElement("a"),ref=document.createElement("b");
        a.href="/biblia/"+bk.s+"/"+(c+1)+"/#v"+v[0];
        ref.textContent=bk.n+" "+(c+1)+","+v[0];a.appendChild(ref);a.appendChild(document.createTextNode(v[1]));
        out.appendChild(a);
      })})});
      cnt.textContent=total===0?"Nenhum versículo encontrado.":(total+(total===1?" versículo encontrado":" versículos encontrados")+(total>max?", mostrando os "+max+" primeiros.":"."));
    }).catch(function(){cnt.textContent="Não foi possível carregar a busca agora. Verifique a conexão e tente de novo."});
  });
})();

/* ---------- Festas fixas (Maria e santos) ---------- */
var MES=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
function feasts(id,list){
  var tb=$(id),tm=now.getMonth()+1,td=now.getDate(),nx=-1;
  list.forEach(function(f,i){if(nx<0&&(f[0]>tm||(f[0]===tm&&f[1]>=td)))nx=i});
  if(nx<0)nx=0;
  list.forEach(function(f,i){
    var tr=document.createElement("tr"),a=document.createElement("td"),b=document.createElement("td");
    a.className="dt";a.textContent=(f[1]===1?"1º":f[1])+" de "+MES[f[0]-1];
    b.textContent=f[2]+(i===nx?" · próxima":"");
    if(i===nx)tr.className="next";
    tr.appendChild(a);tr.appendChild(b);tb.appendChild(tr);
  });
}
feasts("f-maria",[[1,1,"Santa Maria, Mãe de Deus"],[2,11,"Nossa Senhora de Lourdes"],[3,25,"Anunciação do Senhor"],[5,13,"Nossa Senhora de Fátima"],[5,31,"Visitação de Nossa Senhora"],[7,16,"Nossa Senhora do Carmo"],[8,15,"Assunção de Nossa Senhora"],[8,22,"Nossa Senhora Rainha"],[9,8,"Natividade de Nossa Senhora"],[9,15,"Nossa Senhora das Dores"],[10,7,"Nossa Senhora do Rosário"],[10,12,"Nossa Senhora Aparecida, Padroeira do Brasil"],[11,21,"Apresentação de Nossa Senhora"],[12,8,"Imaculada Conceição"],[12,12,"Nossa Senhora de Guadalupe"]]);
feasts("f-santos",[[1,20,"São Sebastião"],[3,19,"São José, esposo de Maria"],[4,23,"São Jorge"],[5,22,"Santa Rita de Cássia"],[6,13,"Santo Antônio de Pádua"],[6,24,"Nascimento de São João Batista"],[6,29,"São Pedro e São Paulo"],[7,11,"São Bento"],[7,26,"São Joaquim e Sant'Ana"],[8,28,"Santo Agostinho"],[9,29,"São Miguel, São Gabriel e São Rafael, arcanjos"],[10,1,"Santa Teresinha do Menino Jesus"],[10,4,"São Francisco de Assis"],[10,28,"São Simão e São Judas Tadeu"],[12,13,"Santa Luzia"]]);

/* ---------- Frases ---------- */
var Q=[
 ["Jesus Cristo","Eu sou o caminho, a verdade e a vida.","Jo 14,6"],
 ["Jesus Cristo","Amai-vos uns aos outros como eu vos amei.","Jo 15,12"],
 ["Jesus Cristo","Vinde a mim, todos os que estais cansados e oprimidos, e eu vos aliviarei.","Mt 11,28"],
 ["Jesus Cristo","Buscai em primeiro lugar o Reino de Deus e a sua justiça.","Mt 6,33"],
 ["Jesus Cristo","Bem-aventurados os misericordiosos, porque alcançarão misericórdia.","Mt 5,7"],
 ["Jesus Cristo","Eu sou a ressurreição e a vida.","Jo 11,25"],
 ["Jesus Cristo","Dai a César o que é de César e a Deus o que é de Deus.","Mt 22,21"],
 ["Jesus Cristo","Tudo o que fizestes a um destes meus irmãos mais pequeninos, a mim o fizestes.","Mt 25,40"],
 ["Jesus Cristo","Pai, perdoa-lhes, porque não sabem o que fazem.","Lc 23,34"],
 ["Jesus Cristo","Eu estarei convosco todos os dias, até o fim dos tempos.","Mt 28,20"],
 ["Maria","Eis aqui a serva do Senhor; faça-se em mim segundo a tua palavra.","Lc 1,38"],
 ["Maria","A minha alma engrandece o Senhor, e o meu espírito exulta em Deus, meu Salvador.","Lc 1,46-47"],
 ["Maria","Fazei tudo o que ele vos disser.","Jo 2,5"],
 ["São Paulo","Já não sou eu que vivo, é Cristo que vive em mim.","Gl 2,20"],
 ["Santo Irineu de Lião","A glória de Deus é o homem vivo, e a vida do homem é a visão de Deus.","Contra as Heresias IV, 20, 7"],
 ["Santo Agostinho","Fizeste-nos para ti, e inquieto está o nosso coração enquanto não repousa em ti.","Confissões I, 1"],
 ["Santo Agostinho","Tarde te amei, ó beleza tão antiga e tão nova, tarde te amei!","Confissões X, 27"],
 ["São Jerônimo","Ignorar as Escrituras é ignorar Cristo.","Comentário a Isaías, prólogo"],
 ["São Bento","Nada antepor ao amor de Cristo.","Regra 4, 21"],
 ["São Francisco de Assis","Louvado sejas, meu Senhor, com todas as tuas criaturas.","Cântico das Criaturas"],
 ["Santo Tomás de Aquino","A graça não destrói a natureza, mas a aperfeiçoa.","Suma Teológica I, q. 1, a. 8"],
 ["Santa Catarina de Sena","Se fordes o que deveis ser, ateareis fogo em toda a Itália.","Carta 368"],
 ["Santo Inácio de Loyola","Em tudo amar e servir.","Exercícios Espirituais, 233"],
 ["Santa Teresa de Jesus","Nada te perturbe, nada te espante. Tudo passa. Só Deus basta.","Poesias"],
 ["São João da Cruz","No entardecer da vida, seremos julgados pelo amor.","Ditos de Luz e Amor, 59"],
 ["São João Maria Vianney","O sacerdócio é o amor do coração de Jesus.","Citado no Catecismo, 1589"],
 ["Santa Teresinha do Menino Jesus","No coração da Igreja, minha Mãe, eu serei o amor.","História de uma Alma, manuscrito B"],
 ["Santa Teresinha do Menino Jesus","Passarei o meu céu fazendo o bem na terra.","Últimas conversas, 17 de julho de 1897"],
 ["São João Paulo II","Não tenhais medo! Abri as portas a Cristo!","Homilia de 22 de outubro de 1978"]
];
function qfig(q){
  var f=document.createElement("figure"),b=document.createElement("blockquote"),c=document.createElement("figcaption"),n=document.createElement("b");
  f.className="quote";b.textContent=q[1];n.textContent=q[0];c.appendChild(n);c.appendChild(document.createTextNode(" · "+q[2]));
  f.appendChild(b);f.appendChild(c);return f;
}
(function(){
  var box=$("quotes"),cats=$("q-cats");
  function chip(label,el){var c=document.createElement("button");c.type="button";c.className="chip";c.textContent=label;
    c.addEventListener("click",function(){el.scrollIntoView({block:"start"})});cats.appendChild(c)}
  [["Palavras de Jesus",function(q){return q[0]==="Jesus Cristo"}],["Palavras de Maria",function(q){return q[0]==="Maria"}],["Palavras dos santos",function(q){return q[0]!=="Jesus Cristo"&&q[0]!=="Maria"}]].forEach(function(g,i){
    var pre=box.querySelectorAll(".cat-h");if(pre.length){chip(g[0],pre[i]);return}
    var w=document.createElement("div");w.className="stack cat-h";
    var h=document.createElement("h2");h.textContent=g[0];w.appendChild(h);
    Q.filter(g[1]).forEach(function(q){w.appendChild(qfig(q))});
    box.appendChild(w);chip(g[0],w);
  });
  chip("Atribuídas por engano",$("q-erradas"));
  var doy=Math.floor((D(now.getFullYear(),now.getMonth(),now.getDate())-D(now.getFullYear(),0,1))/864e5),q=Q[doy%Q.length];
  $("qd-q").textContent=q[1];
  var a=$("qd-a"),n=document.createElement("b");a.textContent="";n.textContent=q[0];a.appendChild(n);a.appendChild(document.createTextNode(" · "+q[2]));
})();

/* ---------- Menu e tamanho da letra ---------- */
var navEl=$("nav"),menuBtn=$("menu-btn");
function setMenu(open){navEl.classList.toggle("open",open);menuBtn.setAttribute("aria-expanded",open?"true":"false");menuBtn.textContent=open?"Fechar":"Menu"}
menuBtn.addEventListener("click",function(){setMenu(menuBtn.getAttribute("aria-expanded")!=="true")});
var FS=[100,112,125,140],fsi=0;
try{fsi=Math.max(0,FS.indexOf(+localStorage.getItem("cath-fs")))}catch(e){}
function setFs(i){fsi=Math.max(0,Math.min(FS.length-1,i));document.documentElement.style.fontSize=FS[fsi]+"%";
  $("fs-down").disabled=fsi===0;$("fs-up").disabled=fsi===FS.length-1;try{localStorage.setItem("cath-fs",FS[fsi])}catch(e){}}
$("fs-down").addEventListener("click",function(){setFs(fsi-1)});
$("fs-up").addEventListener("click",function(){setFs(fsi+1)});
setFs(fsi);

/* ---------- Doação: preencha os campos abaixo ----------
   chave: a chave Pix aleatória da conta (o código com letras, números e hífens)
   copiaecola: o código "Pix Copia e Cola" do QR Code estático gerado no app, sem valor definido
   O QR Code da página é desenhado a partir do copiaecola. */
var DOACAO={chave:"eebc70b6-2212-4283-8663-28017fb3ca2d",copiaecola:"00020126790014br.gov.bcb.pix0136eebc70b6-2212-4283-8663-28017fb3ca2d0217Doacao Catholicam27600016BR.COM.PAGSEGURO0136D9E87DD1-1C26-4092-A30D-24D5B59DB2C25204899953039865802BR5919FABIO HITSUKI NITTO6008BRASILIA62290525PAGS0000000002611151257996304495C"};
function copyTo(text,okMsg){
  var m=$("d-msg");
  try{navigator.clipboard.writeText(text).then(function(){m.textContent=okMsg},function(){m.textContent="Não foi possível copiar. Selecione o código acima e copie manualmente."})}
  catch(e){m.textContent="Não foi possível copiar. Selecione o código acima e copie manualmente."}
}
if(DOACAO.chave||DOACAO.copiaecola){
  $("d-none").hidden=true;$("d-box").hidden=false;
  if(DOACAO.copiaecola){
    $("d-cc-box").hidden=false;
    $("d-cc").addEventListener("click",function(){copyTo(DOACAO.copiaecola,"Código copiado. No app do banco, escolha Pix Copia e Cola, cole e informe o valor.")});
    try{if(window.QRCode){new QRCode($("d-qr"),{text:DOACAO.copiaecola,width:216,height:216,correctLevel:QRCode.CorrectLevel.M});$("d-qr-wrap").hidden=false}}catch(e){}
  }
  if(DOACAO.chave){
    $("d-key-box").hidden=false;$("d-key-btn").hidden=false;$("d-key").textContent=DOACAO.chave;
    $("d-copy").addEventListener("click",function(){copyTo(DOACAO.chave,"Chave copiada. No app do banco, escolha Pix com chave, cole e informe o valor.")});
  }
}
Array.prototype.forEach.call(document.querySelectorAll("button.to"),function(b){
  b.addEventListener("click",function(){var e=$(b.dataset.to);if(e)e.scrollIntoView({block:"start"})});
});

/* ---------- Página atual no menu ---------- */
Array.prototype.forEach.call(document.querySelectorAll("#nav a"),function(a){
  var h=a.getAttribute("href"),p=location.pathname;
  if(h===p||(h!=="/"&&p.indexOf(h)===0))a.setAttribute("aria-current","page");
});
})();

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
