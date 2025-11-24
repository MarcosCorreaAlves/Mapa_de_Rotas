'use strict';

// Dimensões e margens do SVG
const SVG_W = 1000;
const SVG_H = 700;
const SVG_MARGIN = 80; // controla o “tamanho” do mapa dentro da área
const SVG_USABLE_W = SVG_W - 2 * SVG_MARGIN;
const SVG_USABLE_H = SVG_H - 2 * SVG_MARGIN;

// ===== Modelo e helpers =====
const state = {
  V: new Map(), // id -> {id,nome,x,y} (x,y normalizados em [0,1])
  E: [],        // {u,v,peso}
  path: [],
  cost: null
};

const svg        = document.getElementById('svg');
const origem     = document.getElementById('origem');
const destino    = document.getElementById('destino');
const rotaBox    = document.getElementById('rota');
const custoBox   = document.getElementById('custo');
const metaChips  = document.getElementById('metaChips');

function chip(label){
  const s = document.createElement('span');
  s.className = 'chip';
  s.textContent = label;
  return s;
}

// Dijkstra simples (grafo não direcionado)
function dijkstra(start, goal){
  const adj = {};
  for (const v of state.V.keys()) {
    adj[v] = [];
  }

  for (const {u, v, peso} of state.E) {
    const w = +peso;
    if (!Number.isFinite(w)) continue;
    adj[u].push([v, w]);
    adj[v].push([u, w]);
  }

  const dist = Object.fromEntries([...state.V.keys()].map(v => [v, Infinity]));
  const prev = Object.fromEntries([...state.V.keys()].map(v => [v, null]));

  dist[start] = 0;
  const pq = [[0, start]];

  const popMin = () => {
    let k = 0;
    for (let i = 1; i < pq.length; i++) {
      if (pq[i][0] < pq[k][0]) k = i;
    }
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

  if (!isFinite(dist[goal])) {
    return { path: [], cost: Infinity };
  }

  const path = [];
  for (let cur = goal; cur !== null; cur = prev[cur]) {
    path.push(cur);
  }
  path.reverse();
  return { path, cost: dist[goal] };
}

// ===== Carregar grafo da pasta dados/ =====
async function carregarDoArquivoPadrao(){
  try {
    const resp = await fetch('../dados/grafo_front.json');
    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}`);
    }
    const data = await resp.json();
    loadGraph(data);
  } catch (e) {
    console.error('Erro ao carregar ../dados/grafo_front.json', e);
    alert('Não foi possível carregar ../dados/grafo_front.json.\n' +
          'Verifique se você está servindo a pasta "mapa_rotas_cidades" em um servidor HTTP.');
  }
}

function loadGraph(data){
  state.V.clear();
  state.E.length = 0;
  state.path = [];
  state.cost = null;

  if (!data || !Array.isArray(data.vertices) || !Array.isArray(data.arestas)) {
    alert('JSON não segue o formato esperado.');
    return;
  }

  // Normaliza as coordenadas (x,y) para a faixa [0..1]
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

  for (const v of data.vertices) {
    const x = Number(v.x);
    const y = Number(v.y);
    if (Number.isFinite(x) && Number.isFinite(y)) {
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }
  }

  if (!Number.isFinite(minX)) {
    minX = 0; maxX = 1; minY = 0; maxY = 1;
  }

  const dx = (maxX - minX) || 1;
  const dy = (maxY - minY) || 1;

  for (const v of data.vertices) {
    const id = String(v.id);
    const rawX = Number(v.x) || 0;
    const rawY = Number(v.y) || 0;
    const nx = (rawX - minX) / dx;
    const ny = (rawY - minY) / dy;

    state.V.set(id, {
      id,
      nome: v.nome || id,
      x: nx,
      y: ny
    });
  }

  for (const e of data.arestas) {
    const u = String(e.u);
    const v = String(e.v);
    const peso = Number(e.peso);
    if (!state.V.has(u) || !state.V.has(v) || !Number.isFinite(peso)) continue;
    state.E.push({ u, v, peso });
  }

  fillCombos();
  render();
  showMeta();
  showResult();
}

function fillCombos(){
  const keys = [...state.V.keys()].sort();
  origem.innerHTML  = keys.map(k => `<option value="${k}">${k}</option>`).join('');
  destino.innerHTML = keys.map(k => `<option value="${k}">${k}</option>`).join('');

  if (keys.length) {
    origem.value  = keys[0];
    destino.value = keys[keys.length - 1];
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

  if (!state.path.length || !Number.isFinite(state.cost)) {
    custoBox.textContent = 'Custo: —';
    return;
  }

  state.path.forEach((v, i) => {
    const c = chip(v);
    rotaBox.append(c);
    if (i < state.path.length - 1) {
      rotaBox.append(chip('→'));
    }
  });

  custoBox.textContent = `Custo: ${Number(state.cost).toFixed(2)}`;
}

function render(){
  svg.innerHTML = '';
  svg.setAttribute('viewBox', `0 0 ${SVG_W} ${SVG_H}`);

  // Arestas
  for (const e of state.E) {
    const a = state.V.get(e.u);
    const b = state.V.get(e.v);
    if (!a || !b) continue;

    const x1 = SVG_MARGIN + a.x * SVG_USABLE_W;
    const y1 = SVG_MARGIN + a.y * SVG_USABLE_H;
    const x2 = SVG_MARGIN + b.x * SVG_USABLE_W;
    const y2 = SVG_MARGIN + b.y * SVG_USABLE_H;

    const active = isEdgeActive(e.u, e.v);
    const g = line(x1, y1, x2, y2, active);

    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;
    const wt = weightLabel(mx, my, e.peso);

    svg.appendChild(g);
    svg.appendChild(wt);
  }

  // Nós
  for (const [id, v] of state.V) {
    const x = SVG_MARGIN + v.x * SVG_USABLE_W;
    const y = SVG_MARGIN + v.y * SVG_USABLE_H;
    const isActive = state.path.includes(id);
    svg.appendChild(node(id, x, y, isActive));
  }
}

// Marca arestas que pertencem ao menor caminho
function isEdgeActive(u, v){
  const p = state.path;
  for (let i = 0; i < p.length - 1; i++) {
    const a = p[i];
    const b = p[i + 1];
    if ((a === u && b === v) || (a === v && b === u)) {
      return true;
    }
  }
  return false;
}

function line(x1, y1, x2, y2, active = false){
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class', `edge${active ? ' active' : ''}`);

  const l = document.createElementNS('http://www.w3.org/2000/svg','line');
  l.setAttribute('x1', x1);
  l.setAttribute('y1', y1);
  l.setAttribute('x2', x2);
  l.setAttribute('y2', y2);

  g.appendChild(l);
  return g;
}

function weightLabel(x, y, w){
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class','edge weight');

  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x', x);
  t.setAttribute('y', y - 6);
  t.setAttribute('text-anchor','middle');
  t.textContent = String(w);

  g.appendChild(t);
  return g;
}

function node(id, x, y, active = false){
  const g = document.createElementNS('http://www.w3.org/2000/svg','g');
  g.setAttribute('class', `node${active ? ' active' : ''}`);
  g.setAttribute('data-id', id);
  g.setAttribute('transform', `translate(${x},${y})`);

  const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
  c.setAttribute('r', 16);

  const t = document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x', 0);
  t.setAttribute('y', 5);
  t.setAttribute('text-anchor','middle');
  t.textContent = id;

  g.appendChild(c);
  g.appendChild(t);

  enableDrag(g);
  g.addEventListener('dblclick', () => {
    // reservado pra futuras ações
  });

  return g;
}

function enableDrag(g){
  let dragging = false;
  let last = null;

  g.addEventListener('mousedown', (e) => {
    dragging = true;
    last = [e.clientX, e.clientY];
    e.preventDefault();
  });

  window.addEventListener('mousemove', (e) => {
    if (!dragging || !last) return;

    const [lx, ly] = last;
    const dx = e.clientX - lx;
    const dy = e.clientY - ly;
    last = [e.clientX, e.clientY];

    const id = g.getAttribute('data-id');
    const v  = state.V.get(id);
    if (!v) return;

    const tr = g.getAttribute('transform');
    const m = /translate\(([^,]+),([^\)]+)\)/.exec(tr);
    if (!m) return;

    let x = parseFloat(m[1]) + dx;
    let y = parseFloat(m[2]) + dy;

    g.setAttribute('transform', `translate(${x},${y})`);

    // salva em [0..1] de novo (usando mesma lógica de margem)
    v.x = (x - SVG_MARGIN) / SVG_USABLE_W;
    v.y = (y - SVG_MARGIN) / SVG_USABLE_H;

    render();
  });

  window.addEventListener('mouseup', () => {
    dragging = false;
    last = null;
  });
}

// ===== Eventos UI =====
document.getElementById('btnCalcular').addEventListener('click', () => {
  const s = origem.value;
  const t = destino.value;

  if (!s || !t || s === t) {
    state.path = [];
    state.cost = null;
    showResult();
    render();
    return;
  }

  const {path, cost} = dijkstra(s, t);
  state.path = path;
  state.cost = cost;
  showResult();
  render();
});

document.getElementById('btnLimpar').addEventListener('click', () => {
  state.path = [];
  state.cost = null;
  showResult();
  render();
});

document.getElementById('btnExportar').addEventListener('click', () => {
  if (!state.path.length) {
    alert('Nenhuma rota calculada para exportar.');
    return;
  }

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
  URL.revokeObjectURL(a.href);
});

document.getElementById('btnAutoLayout').addEventListener('click', () => {
  const n = state.V.size;
  if (!n) return;

  const r = 0.35;
  let i = 0;
  for (const v of state.V.values()) {
    v.x = 0.5 + r * Math.cos(2 * Math.PI * i / n);
    v.y = 0.5 + r * Math.sin(2 * Math.PI * i / n);
    i++;
  }
  render();
});

document.getElementById('btnGerarPesos').addEventListener('click', () => {
  for (const e of state.E) {
    const jitter = (Math.random() * 1.2 - 0.6);
    e.peso = Math.max(1, +(e.peso + jitter).toFixed(2));
  }

  render();

  if (state.path.length >= 2) {
    const origemAtual  = state.path[0];
    const destinoAtual = state.path[state.path.length - 1];
    const {path, cost} = dijkstra(origemAtual, destinoAtual);
    state.path = path;
    state.cost = cost;
    showResult();
    render();
  }
});

// Zoom toolbar
document.getElementById('zoomIn').addEventListener('clickZ', () => zoom(1.1));
document.getElementById('zoomOut').addEventListener('click', () => zoom(0.9));
document.getElementById('zoomReset').addEventListener('click', () => {
  svg.setAttribute('viewBox', `0 0 ${SVG_W} ${SVG_H}`);
});

function zoom(f){
  const vb = svg.getAttribute('viewBox').split(' ').map(Number); // x y w h
  if (vb.length !== 4 || vb.some(Number.isNaN)) return;
  vb[2] /= f;
  vb[3] /= f;
  svg.setAttribute('viewBox', vb.join(' '));
}

// Inicializa carregando dados da pasta dados/
carregarDoArquivoPadrao();
