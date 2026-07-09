/* ===== shared helpers ===== */
const CATS = {
  profession:  {label:"Practitioners",   sub:"named magic-workers",            color:"var(--c-profession)", glyph:"✶"},
  act:         {label:"Acts of magic",   sub:"verbs & workings",               color:"var(--c-act)",        glyph:"❧"},
  divination:  {label:"Divination",      sub:"seeing & foretelling",           color:"var(--c-divination)", glyph:"◉"},
  alchemy:     {label:"Alchemy",         sub:"the art of transformation",      color:"var(--c-alchemy)",    glyph:"🜍"},
  quality:     {label:"Qualities",       sub:"the arcane & eldritch",          color:"var(--c-quality)",    glyph:"✧"},
  item:        {label:"Classical items", sub:"historical magical objects",     color:"var(--c-item)",       glyph:"⚱"},
  book:        {label:"History of the book", sub:"names for the written work", color:"var(--c-book)",       glyph:"❦"},
};
const CAT_ORDER = ["profession","act","divination","alchemy","quality","item","book"];

// MTG colour identity
const WUBRG = ["W","U","B","R","G","C"];
const COLORHEX = {W:"#f8f0d8",U:"#5aa9e6",B:"#5b5566",R:"#e0704f",G:"#68b46a",C:"#b9b3c9"};
const COLORNAME = {W:"White",U:"Blue",B:"Black",R:"Red",G:"Green",C:"Colorless"};
function colorBar(dist,h){
  const tot=WUBRG.reduce((a,c)=>a+(dist[c]||0),0)||1;
  const segs=WUBRG.filter(c=>dist[c]).map(c=>`<span title="${COLORNAME[c]} ${Math.round(100*dist[c]/tot)}%" style="width:${100*dist[c]/tot}%;background:${COLORHEX[c]}"></span>`).join("");
  return `<div class="cbar" style="height:${h||14}px">${segs}</div>`;
}
// origin-language palette for the loanword atlas
const LANGHEX = {"Greek":"#57c7c7","Latin":"#d4a24a","Old English":"#8a7dff","Old Norse":"#7d9bff",
  "French":"#e0708a","Arabic":"#6fbf7f","Persian":"#c98be0","Celtic":"#67c98a","Germanic":"#c99a6a",
  "Siberian":"#e0a15a","Hebrew":"#b98be0","Unknown":"#6f6690"};
function langColor(l){ return LANGHEX[l]||"#9c90bb"; }

async function getJSON(url){ const r = await fetch(url); if(!r.ok) throw new Error(url); return r.json(); }
function esc(s){ return (s||"").replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function pips(colors){
  if(!colors||!colors.length) return '<span class="pips"><span class="pip C"></span></span>';
  return '<span class="pips">'+colors.map(c=>`<span class="pip ${c}"></span>`).join("")+'</span>';
}
function catTag(cat){
  const m=CATS[cat]||{label:cat,color:"var(--muted)"};
  return `<span class="cat" style="background:${m.color}">${m.label}</span>`;
}
const CHART_PAGES = new Set(["charts.html","insights.html","timeline.html","colors.html","origins.html","mosaic.html"]);
function nav(active){
  const links=[["index.html","Terms"],["histories.html","Histories"],["timeline-history.html","Timeline"],["atlas.html","Atlas"],["charts.html","Charts"],["about.html","About"]];
  const isChart=CHART_PAGES.has(active);
  return `<nav class="topnav">
    <a class="brand" href="index.html">✶ The Vocabulary of Magic</a>
    <span class="spacer"></span>
    ${links.map(([h,t])=>{const on=(h===active)||(h==="charts.html"&&isChart);return `<a class="nav ${on?'active':''}" href="${h}">${t}</a>`;}).join("")}
  </nav>`;
}
function foot(){
  return `<footer>
    Card data &amp; images via <a href="https://scryfall.com" target="_blank" rel="noopener">Scryfall</a> ·
    counts &amp; analysis: <b>MTGMAGICWORDS</b> · card names &amp; text © Wizards of the Coast ·
    a word study of the origins &amp; etymology of magic, cited to Ted's magic databases &amp; library.
  </footer>`;
}
function mountChrome(active){
  document.body.insertAdjacentHTML("afterbegin", nav(active));
  document.body.insertAdjacentHTML("beforeend", foot());
}
