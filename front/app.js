'use strict';

// ============================
// Configuração do SVG (tela)
// ============================
const SVG_W = 1000;
const SVG_H = 700;
// margem maior para "apertar" o mapa e caber na tela
const SVG_MARGIN = 150;
const SVG_USABLE_W = SVG_W - 2 * SVG_MARGIN;
const SVG_USABLE_H = SVG_H - 2 * SVG_MARGIN;

// ============================
// Estado global do grafo
// ============================
const state = {
  V: new Map(), // id -> {id,nome,x,y}
  E: [],        // {u,v,peso,motivo}
  path: [],
  cost: null
};

// ============================
// Referências ao DOM
// ============================
const svg        = document.getElementById('svg');
const origem     = document.getElementById('origem');
const destino    = document.getElementById('destino');
const rotaBox    = document.getElementById('rota');
const custoBox   = document.getElementById('custo');
const metaChips  = document.getElementById('metaChips');
const detalhesBox = document.getElementById('detalhesRota');

// Chip visual
function chip(label){
  const s = document.createElement('span');
  s.className = 'chip';
  s.textContent = label;
  return s;
}

// chave padrão pra arestas não-direcionadas
function edgeKey(u, v) {
  return [String(u), String(v)].sort().join('::');
}

// procura aresta (u,v) no estado
function getEdgeData(u, v) {
  return state.E.find(e =>
    (e.u === u && e.v === v) ||
    (e.u === v && e.v === u)
  ) || null;
}

// ============================================================
// ANIMAÇÃO do ponto na rota
// ============================================================
const animation = {
  frameId: null,
  marker: null,
  segments: [],
  totalLen: 0
};

function stopAnimation(){
  if (animation.frameId != null) cancelAnimationFrame(animation.frameId);
  if (animation.marker?.parentNode) animation.marker.remove();
  animation.frameId = null;
  animation.marker = null;
  animation.segments = [];
  animation.totalLen = 0;
}

function startAnimation(){
  stopAnimation();
  if (!state.path || state.path.length < 2) return;

  const pts = state.path.map(id => {
    const v = state.V.get(id);
    return {
      x: SVG_MARGIN + v.x * SVG_USABLE_W,
      y: SVG_MARGIN + v.y * SVG_USABLE_H
    };
  });

  const segments = [];
  let totalLen = 0;

  for (let i = 0; i < pts.length - 1; i++) {
    const p1 = pts[i];
    const p2 = pts[i+1];
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const len = Math.hypot(dx, dy);
    if (len > 0) {
      segments.push({ x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y, len });
      totalLen += len;
    }
  }

  animation.segments = segments;
  animation.totalLen = totalLen;

  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  marker.setAttribute('r', 10);
  marker.setAttribute('class', 'anim-marker');
  svg.appendChild(marker);
  animation.marker = marker;

  let startTime = null;
  const speed = 200; // px/s

  function step(t){
    if (!startTime) startTime = t;
    const elapsed = (t - startTime) / 1000;
    let d = elapsed * speed;

    if (d >= totalLen) {
      const last = segments.at(-1);
      marker.setAttribute('cx', last.x2);
      marker.setAttribute('cy', last.y2);
      stopAnimation();
      return;
    }

    let acc = 0;
    let i = 0;
    while (i < segments.length && acc + segments[i].len < d) {
      acc += segments[i].len;
      i++;
    }

    if (i >= segments.length) return;

    const seg = segments[i];
    const local = d - acc;
    const tNorm = local / seg.len;

    const x = seg.x1 + (seg.x2 - seg.x1)*tNorm;
    const y = seg.y1 + (seg.y2 - seg.y1)*tNorm;

    marker.setAttribute('cx', x);
    marker.setAttribute('cy', y);

    animation.frameId = requestAnimationFrame(step);
  }

  animation.frameId = requestAnimationFrame(step);
}

// ============================================================
// DIJKSTRA
// ============================================================
function dijkstra(start, goal){
  const adj = {};
  for (const v of state.V.keys()) adj[v] = [];

  for (const e of state.E) {
    const w = +e.peso;
    if (!Number.isFinite(w)) continue;
    adj[e.u].push([e.v, w]);
    adj[e.v].push([e.u, w]);
  }

  const dist = Object.fromEntries([...state.V.keys()].map(x=>[x,Infinity]));
  const prev = Object.fromEntries([...state.V.keys()].map(x=>[x,null]));

  dist[start] = 0;
  const pq = [[0, start]];

  const popMin = () => {
    let k = 0;
    for (let i = 1; i < pq.length; i++) if (pq[i][0] < pq[k][0]) k = i;
    return pq.splice(k, 1)[0];
  };

  while (pq.length) {
    const [d, u] = popMin();
    if (u === goal) break;
    if (d !== dist[u]) continue;
    for (const [v, w] of adj[u]) {
      const nd = d + w;
      if (nd < dist[v]) {
        dist[v] = nd;
        prev[v] = u;
        pq.push([nd, v]);
      }
    }
  }

  if (!isFinite(dist[goal])) return {path:[], cost:Infinity};

  const path = [];
  for (let cur = goal; cur != null; cur = prev[cur]) path.push(cur);
  return { path: path.reverse(), cost: dist[goal] };
}

// ============================================================
// CARREGAR GRAFO + PESOS
// ============================================================
async function carregarDoArquivoPadrao(){
  try {
    const [respG, respP] = await Promise.all([
      fetch('../dados/grafo_cidade.json'),
      fetch('../dados/pesos_atuais.json')
    ]);

    const grafo = await respG.json();
    const pesos = await respP.json();

    loadGraph(grafo, pesos);
  }
  catch(err){
    alert("Erro ao carregar os arquivos JSON.");
    console.error(err);
  }
}

// ============================================================
// MONTAR GRAFO EM MEMÓRIA
// ============================================================
function loadGraph(data, pesosData){
  state.V.clear();
  state.E = [];
  state.path = [];
  state.cost = null;
  stopAnimation();

  // normalização
  let xMin=1e9, xMax=-1e9, yMin=1e9, yMax=-1e9;

  for (const v of data.vertices) {
    xMin = Math.min(xMin, v.x);
    xMax = Math.max(xMax, v.x);
    yMin = Math.min(yMin, v.y);
    yMax = Math.max(yMax, v.y);
  }

  const dx = (xMax - xMin) || 1;
  const dy = (yMax - yMin) || 1;

  for (const v of data.vertices) {
    state.V.set(String(v.id), {
      id: String(v.id),
      nome: v.nome,
      x: (v.x - xMin) / dx,
      y: (v.y - yMin) / dy
    });
  }

  // pesos
  const pesosMap = new Map();
  for (const e of pesosData.arestas || []) {
    pesosMap.set(edgeKey(e.origem, e.destino), {
      peso: e.peso,
      motivo: e.motivo
    });
  }

  for (const e of data.arestas) {
    const u = String(e.origem);
    const v = String(e.destino);

    const meta = pesosMap.get(edgeKey(u, v)) || {};

    state.E.push({
      u, v,
      peso: meta.peso,
      motivo: meta.motivo || "—"
    });
  }

  fillCombos();
  render();
  showMeta();
  showResult();
}

// ============================================================
// UI
// ============================================================
function fillCombos(){
  origem.innerHTML = '';
  destino.innerHTML = '';

  const list = [...state.V.values()].sort((a,b)=>a.nome.localeCompare(b.nome));

  for (const v of list) {
    const o = document.createElement('option');
    o.value = v.id;
    o.textContent = v.nome;
    origem.appendChild(o);

    const d = document.createElement('option');
    d.value = v.id;
    d.textContent = v.nome;
    destino.appendChild(d);
  }
}

function showMeta(){
  metaChips.innerHTML = '';
  metaChips.append(
    chip(`${state.V.size} cidades`),
    chip(`${state.E.length} rotas`)
  );
}

function showResult(){
  rotaBox.innerHTML = '';
  detalhesBox.innerHTML = '';

  if (!state.path.length){
    custoBox.textContent = "Custo: —";
    return;
  }

  state.path.forEach((id,i)=>{
    rotaBox.append(chip(state.V.get(id).nome));
    if (i < state.path.length - 1) rotaBox.append(chip("→"));
  });

  const nomes = state.path.map(id => state.V.get(id).nome);
  const header = document.createElement("div");
  header.className = "rota-resumo";
  header.textContent = "Rota: " + nomes.join(" → ");
  detalhesBox.appendChild(header);

  const subt = document.createElement("div");
  subt.className = "rota-titulo-detalhes";
  subt.textContent = "Detalhes do percurso:";
  detalhesBox.appendChild(subt);

  const lista = document.createElement("ol");
  lista.className = "rota-lista";

  for (let i=0; i < state.path.length-1; i++){
    const u = state.path[i];
    const v = state.path[i+1];
    const e = getEdgeData(u, v);

    const li = document.createElement("li");
    li.innerHTML =
      `<strong>${state.V.get(u).nome} → ${state.V.get(v).nome}</strong><br>
       Peso: ${e.peso}<br>
       Condição: ${e.motivo}`;
    lista.appendChild(li);
  }

  detalhesBox.appendChild(lista);

  const ct = document.createElement('div');
  ct.className = "rota-custo-total";
  ct.textContent = "CUSTO TOTAL: " + Number(state.cost).toFixed(0);
  detalhesBox.appendChild(ct);

  custoBox.textContent = "Custo: " + Number(state.cost).toFixed(2);
}

// ============================================================
// GERAÇÃO DO MAPA
// ============================================================
function render(){
  svg.innerHTML = '';
  svg.setAttribute('viewBox', `0 0 ${SVG_W} ${SVG_H}`);

  for (const e of state.E) {
    const a = state.V.get(e.u);
    const b = state.V.get(e.v);

    const x1 = SVG_MARGIN + a.x * SVG_USABLE_W;
    const y1 = SVG_MARGIN + a.y * SVG_USABLE_H;
    const x2 = SVG_MARGIN + b.x * SVG_USABLE_W;
    const y2 = SVG_MARGIN + b.y * SVG_USABLE_H;

    const active = isEdgeActive(e.u, e.v);

    const g = line(x1,y1,x2,y2,active);
    const wt = weightLabel((x1+x2)/2, (y1+y2)/2, e.peso);

    svg.appendChild(g);
    svg.appendChild(wt);
  }

  for (const [id, v] of state.V) {
    const x = SVG_MARGIN + v.x * SVG_USABLE_W;
    const y = SVG_MARGIN + v.y * SVG_USABLE_H;
    const active = state.path.includes(id);
    svg.appendChild(node(id, x, y, active));
  }

  if (animation.marker) svg.appendChild(animation.marker);
}

function isEdgeActive(u, v){
  for (let i = 0; i < state.path.length - 1; i++){
    if ((state.path[i] === u && state.path[i+1] === v) ||
        (state.path[i] === v && state.path[i+1] === u)) return true;
  }
  return false;
}

function line(x1, y1, x2, y2, active){
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class', `edge${active?' active':''}`);

  const l = document.createElementNS('http://www.w3.org/2000/svg','line');
  l.setAttribute('x1', x1);
  l.setAttribute('y1', y1);
  l.setAttribute('x2', x2);
  l.setAttribute('y2', y2);

  g.appendChild(l);
  return g;
}

// ============================================================
// 🔥 PESOS COM FUNDO CIRCULAR (tema roxo dark)
// ============================================================
function weightLabel(x, y, w){
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class','edge weight');

  const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
  c.setAttribute('cx', x);
  c.setAttribute('cy', y);
  c.setAttribute('r', 13);
  c.setAttribute('class', 'weight-bg');

  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x', x);
  t.setAttribute('y', y + 4);
  t.setAttribute('text-anchor','middle');
  t.setAttribute('class', 'weight-text');
  t.textContent = String(w);

  g.appendChild(c);
  g.appendChild(t);
  return g;
}


// ============================
// NÓS DO GRAFO
// ============================
function node(id, x, y, active){
  const v = state.V.get(id);

  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class', `node${active?' active':''}`);
  g.setAttribute('data-id', id);
  g.setAttribute('transform', `translate(${x},${y})`);

  const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
  c.setAttribute('r', 16);

  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x', 0);
  t.setAttribute('y', 5);
  t.setAttribute('text-anchor', 'middle');
  t.textContent = v.nome;

  g.appendChild(c);
  g.appendChild(t);

  enableDrag(g);
  return g;
}

// ============================
// DRAG & DROP MANUAL
// ============================
function enableDrag(g){
  let drag = false, last = null;

  g.addEventListener('mousedown', e=>{
    drag = true;
    last = [e.clientX, e.clientY];
  });

  window.addEventListener('mousemove', e=>{
    if (!drag) return;

    const [lx, ly] = last;
    const dx = e.clientX - lx;
    const dy = e.clientY - ly;

    last = [e.clientX, e.clientY];

    const tr = g.getAttribute('transform');
    const m = /translate\(([^,]+),([^)]+)\)/.exec(tr);
    if (!m) return;

    const id = g.getAttribute('data-id');
    const v = state.V.get(id);

    let x = parseFloat(m[1]) + dx;
    let y = parseFloat(m[2]) + dy;

    g.setAttribute('transform', `translate(${x},${y})`);

    v.x = (x - SVG_MARGIN) / SVG_USABLE_W;
    v.y = (y - SVG_MARGIN) / SVG_USABLE_H;

    render();
  });

  window.addEventListener('mouseup', ()=> drag = false);
}

// ============================================================
// EVENTOS
// ============================================================
document.getElementById('btnCalcular').addEventListener('click', ()=>{
  const {path, cost} = dijkstra(origem.value, destino.value);
  state.path = path;
  state.cost = cost;
  showResult();
  render();
  startAnimation();
});

document.getElementById('btnLimpar').addEventListener('click', ()=>{
  state.path = [];
  state.cost = null;
  stopAnimation();
  showResult();
  render();
});

// EXPORTAR JSON
document.getElementById('btnExportar').addEventListener('click', ()=>{
  if (!state.path.length) return alert("Nenhuma rota para exportar.");

  const payload = {
    origem: origem.value,
    destino: destino.value,
    caminho: state.path,
    custo: state.cost
  };

  const blob = new Blob([JSON.stringify(payload, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `rota_${payload.origem}_${payload.destino}.json`;
  a.click();
});

// AUTO-LAYOUT EM CÍRCULO
document.getElementById('btnAutoLayout').addEventListener('click', ()=>{
  const r = 0.35;
  const arr = [...state.V.values()];
  const n = arr.length;
  arr.forEach((v,i)=>{
    v.x = 0.5 + r*Math.cos(2*Math.PI*i/n);
    v.y = 0.5 + r*Math.sin(2*Math.PI*i/n);
  });
  render();
});

// GERAR NOVOS PESOS
document.getElementById('btnGerarPesos').addEventListener('click', ()=>{
  for (const e of state.E) {
    const j = Math.random()*1.2 - 0.6;
    e.peso = Math.max(1, +(e.peso + j).toFixed(2));
  }

  render();

  if (state.path.length >= 2){
    const {path,cost} = dijkstra(state.path[0], state.path.at(-1));
    state.path = path;
    state.cost = cost;
    showResult();
    render();
    startAnimation();
  }
});

// ZOOM
document.getElementById('zoomIn').addEventListener('click', ()=> zoom(1.1));
document.getElementById('zoomOut').addEventListener('click', ()=> zoom(0.9));
document.getElementById('zoomReset').addEventListener('click', ()=>{
  svg.setAttribute('viewBox', `0 0 ${SVG_W} ${SVG_H}`);
});

function zoom(f){
  const vb = svg.getAttribute('viewBox').split(' ').map(Number);
  vb[2] /= f;
  vb[3] /= f;
  svg.setAttribute('viewBox', vb.join(' '));
}

// ============================================================
// BOOT
// ============================================================
carregarDoArquivoPadrao();
