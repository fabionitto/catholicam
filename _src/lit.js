/* Catholicam · calendário litúrgico (Igreja no Brasil), calculado no navegador para qualquer data.
   Este arquivo vai no <head> de todas as páginas: assim a cor do site já nasce com a cor litúrgica do dia.
   Inclui os tempos, as datas móveis, as solenidades e as festas (com as transferências próprias do Brasil:
   Ascensão, São Pedro e São Paulo, Assunção e Todos os Santos no domingo). Memórias de santos não entram.
   Teste de outra data: acrescente ?dia=AAAA-MM-DD ao endereço. */
function D(y,m,d){return new Date(y,m,d,12)}
function addDays(dt,n){var x=new Date(dt);x.setDate(x.getDate()+n);return x}
function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return D(y,mo-1,da)}
function advent(y){var d24=D(y,11,24);return addDays(d24,-d24.getDay()-21)}
function baptism(y){var j2=D(y,0,2),epi=addDays(j2,(7-j2.getDay())%7);return [epi,addDays(epi,epi.getDate()>=7?1:7)]}
function litYear(now){var y=now.getFullYear(),t=D(y,now.getMonth(),now.getDate());return t>=advent(y)?y+1:y}
function cycles(end){return [["C","A","B"][end%3],end%2?"I":"II"]}
var LIT_NAMES={verde:"Verde",roxo:"Roxo",branco:"Branco",vermelho:"Vermelho",rosa:"Rosa",preto:"Preto"};
var LIT_META={verde:"#2f6b45",roxo:"#5b3a86",branco:"#e6b422",vermelho:"#a3262a",rosa:"#a63d6e",preto:"#3d434a"};
/* Solenidades e festas de data fixa (ou transferida) do ano y: [nome, cor, grau]. Grau menor vence. */
function litFixed(y){
  var E=easter(y),palm=addDays(E,-7),out={},W="branco",R="vermelho";
  function sunOnOrAfter(dt){return addDays(dt,(7-dt.getDay())%7)}
  function put(dt,name,c,rank,alt){out[dt.getMonth()+"-"+dt.getDate()]=[name,c,rank,alt]}
  function inHoly(dt){return dt>=palm&&dt<=addDays(E,7)}
  /* graus: 3 solenidade, 5 festa do Senhor, 7 festa da Virgem ou de santo */
  [[0,25,"Conversão de São Paulo, Apóstolo",W],[1,22,"Cátedra de São Pedro, Apóstolo",W],[3,25,"São Marcos, Evangelista",R],
   [4,3,"São Filipe e São Tiago, Apóstolos",R],[4,14,"São Matias, Apóstolo",R],[4,31,"Visitação de Nossa Senhora",W],
   [6,3,"São Tomé, Apóstolo",R],[6,22,"Santa Maria Madalena",W],[6,25,"São Tiago, Apóstolo",R],[7,10,"São Lourenço, Diácono e Mártir",R],
   [7,24,"São Bartolomeu, Apóstolo",R],[8,8,"Natividade de Nossa Senhora",W],[8,21,"São Mateus, Apóstolo e Evangelista",R],
   [8,29,"São Miguel, São Gabriel e São Rafael, Arcanjos",W],[9,18,"São Lucas, Evangelista",R],[9,28,"São Simão e São Judas, Apóstolos",R],
   [10,30,"Santo André, Apóstolo",R],[11,26,"Santo Estêvão, Primeiro Mártir",R],[11,27,"São João, Apóstolo e Evangelista",W],
   [11,28,"Santos Inocentes, Mártires",R]
  ].forEach(function(f){put(D(y,f[0],f[1]),f[2],f[3],7)});
  [[1,2,"Apresentação do Senhor",W],[7,6,"Transfiguração do Senhor",W],[8,14,"Exaltação da Santa Cruz",R],
   [10,9,"Dedicação da Basílica do Latrão",W]].forEach(function(f){put(D(y,f[0],f[1]),f[2],f[3],5)});
  var jo=D(y,2,19);if(inHoly(jo))jo=addDays(palm,-1);else if(jo.getDay()===0)jo=addDays(jo,1);
  put(jo,"São José, Esposo da Virgem Maria",W,3);
  var an=D(y,2,25);if(inHoly(an))an=addDays(E,8);else if(an.getDay()===0)an=addDays(an,1);
  put(an,"Anunciação do Senhor",W,3);
  var jb=D(y,5,24);if(+jb===+addDays(E,68))jb=D(y,5,23);else if(+jb===+addDays(E,60))jb=D(y,5,25);
  put(jb,"Natividade de São João Batista",W,3);
  put(sunOnOrAfter(D(y,5,29)),"São Pedro e São Paulo, Apóstolos",R,3);
  put(sunOnOrAfter(D(y,7,15)),"Assunção de Nossa Senhora",W,3);
  put(D(y,9,12),"Nossa Senhora da Conceição Aparecida, Padroeira do Brasil",W,3);
  var n2=D(y,10,2);
  put(n2.getDay()===0?D(y,10,1):sunOnOrAfter(D(y,10,1)),"Todos os Santos",W,3);
  put(n2,"Comemoração de Todos os Fiéis Defuntos (Finados)","roxo",3,"preto");
  var ic=D(y,11,8);if(ic.getDay()===0)ic=D(y,11,9);
  put(ic,"Imaculada Conceição de Nossa Senhora",W,3);
  return out;
}
/* O dia litúrgico: {n: celebração, s: tempo, c: cor (verde, roxo, branco, vermelho, rosa, preto), alt: cor alternativa, k: nome da cor, r: grau} */
function litDay(now){
  var y=now.getFullYear(),t=D(y,now.getMonth(),now.getDate()),sun=t.getDay()===0,DAY=864e5;
  function wk(from){return Math.floor((t-from)/DAY/7)+1}
  function eq(d){return t.getTime()===d.getTime()}
  function lab(n,tempo){return sun?n+"º Domingo "+tempo:n+"ª Semana "+tempo}
  var E=easter(y),ash=addDays(E,-46),pent=addDays(E,49),adv=advent(y),ep=baptism(y),epi=ep[0],bap=ep[1];
  var W="branco",V="roxo",R="vermelho",G="verde",b;
  function base(){
    if(t>=D(y,11,25)||t<=bap){
      var x="Tempo do Natal",dd=t.getDate(),mm=t.getMonth(),r=13;
      var hf=(function(){var yy=mm===11?y:y-1,n=D(yy,11,25);for(var i=1;i<=6;i++){var s=addDays(n,i);if(s.getDay()===0)return s}return D(yy,11,30)})();
      if(mm===11&&dd===25){x="Natal do Senhor";r=2}
      else if(mm===0&&dd===1){x="Santa Maria, Mãe de Deus";r=3}
      else if(eq(epi)){x="Epifania do Senhor";r=2}
      else if(eq(bap)){x="Batismo do Senhor";r=5}
      else if(eq(hf)){x="Sagrada Família de Jesus, Maria e José";r=5}
      else if(mm===11){x="Oitava do Natal";r=9}
      else if(sun){x="Domingo do Tempo do Natal";r=6}
      return [x,"Tempo do Natal",W,r];
    }
    if(t>=adv){var n=wk(adv);return [lab(n,"do Advento"),"Tempo do Advento",sun&&n===3?"rosa":V,sun?2:(t>=D(y,11,17)?9:13),sun&&n===3?V:0]}
    if(t<ash){var b0=bap.getDay()===1?addDays(bap,-1):bap;return [lab(wk(b0),"do Tempo Comum"),"Tempo Comum",G,sun?6:13]}
    if(t<addDays(E,-3)){
      if(eq(ash))return ["Quarta-feira de Cinzas","Tempo da Quaresma",V,2];
      var l1=addDays(ash,4);if(t<l1)return ["Depois das Cinzas","Tempo da Quaresma",V,9];
      var q=wk(l1);
      if(q===6)return sun?["Domingo de Ramos e da Paixão do Senhor","Semana Santa",R,2]:["Semana Santa","Semana Santa",V,2];
      return [lab(q,"da Quaresma"),"Tempo da Quaresma",sun&&q===4?"rosa":V,sun?2:9,sun&&q===4?V:0];
    }
    if(t<E){
      if(eq(addDays(E,-3)))return ["Quinta-feira Santa (à noite, Missa da Ceia do Senhor)","Tríduo Pascal",W,1];
      if(eq(addDays(E,-2)))return ["Sexta-feira da Paixão do Senhor","Tríduo Pascal",R,1];
      return ["Sábado Santo (à noite, Vigília Pascal)","Tríduo Pascal",V,1];
    }
    if(t<=pent){
      if(eq(E))return ["Domingo de Páscoa da Ressurreição do Senhor","Tempo Pascal",W,1];
      if(eq(pent))return ["Domingo de Pentecostes","Tempo Pascal",R,2];
      if(eq(addDays(E,42)))return ["Ascensão do Senhor","Tempo Pascal",W,2];
      var p=wk(E);
      if(p===1)return ["Oitava da Páscoa","Tempo Pascal",W,2];
      if(sun&&p===2)return ["2º Domingo da Páscoa (da Divina Misericórdia)","Tempo Pascal",W,2];
      return [lab(p,"da Páscoa"),"Tempo Pascal",W,sun?2:13];
    }
    var ck=addDays(adv,-7),s0=addDays(t,-t.getDay()),o=34-Math.round((ck-s0)/DAY/7);
    if(eq(addDays(pent,7)))return ["Santíssima Trindade","Tempo Comum",W,3];
    if(eq(addDays(pent,11)))return ["Corpo e Sangue de Cristo (Corpus Christi)","Tempo Comum",W,3];
    if(eq(addDays(pent,19)))return ["Sagrado Coração de Jesus","Tempo Comum",W,3];
    if(eq(ck))return ["Nosso Senhor Jesus Cristo, Rei do Universo","Tempo Comum",W,3];
    return [lab(o,"do Tempo Comum"),"Tempo Comum",G,sun?6:13];
  }
  b=base();
  var f=litFixed(y)[t.getMonth()+"-"+t.getDate()];
  if(f&&f[2]<b[3])b=[f[0],b[1],f[1],f[2],f[3]||0];
  return {n:b[0],s:b[1],c:b[2],alt:b[4]||"",r:b[3],k:LIT_NAMES[b[2]]+(b[4]?" (ou "+LIT_NAMES[b[4]].toLowerCase()+")":"")};
}
var LIT_NOW=(function(){
  var n=new Date(),m=/[?&]dia=(\d{4})-(\d{2})-(\d{2})/.exec(location.search);
  if(m)n=new Date(+m[1],m[2]-1,+m[3],new Date().getHours(),new Date().getMinutes());
  return n;
})();
var LIT=litDay(LIT_NOW);
(function(){
  var r=document.documentElement;r.setAttribute("data-season",LIT.c);
  var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute("content",LIT_META[LIT.c]);
})();
