#!/usr/bin/env python3
"""Build index.html with embedded FILE_MANIFEST."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT, "manifest.json")
OUT_PATH = os.path.join(ROOT, "index.html")

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bei Xujiaqiao GeoJSON Viewer</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css" crossorigin="">
<style>
:root {
  --sidebar-w: 360px;
  --bg: #f5f5f0;
  --panel: #fff;
  --border: #d8d4c8;
  --text: #2c2c2c;
  --accent: #5c4a32;
  --muted: #6b6560;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; font-family: "Segoe UI", system-ui, sans-serif; color: var(--text); background: var(--bg); }
#app { display: flex; height: 100vh; overflow: hidden; }
#sidebar {
  width: var(--sidebar-w); min-width: 280px; max-width: 90vw;
  background: var(--panel); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; z-index: 1000;
}
#sidebar.collapsed { display: none; }
#sidebar-header { padding: 12px 14px; border-bottom: 1px solid var(--border); background: #faf8f4; }
#sidebar-header h1 { margin: 0 0 8px; font-size: 1.05rem; font-weight: 600; color: var(--accent); }
.global-actions { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
.abandonment-row {
  display: flex; align-items: flex-start; gap: 6px; margin-bottom: 8px;
  font-size: 0.75rem; line-height: 1.35; color: var(--muted);
}
.abandonment-row input { margin-top: 2px; flex-shrink: 0; }
button {
  border: 1px solid var(--border); background: #fff; color: var(--text);
  padding: 5px 10px; border-radius: 4px; font-size: 0.78rem; cursor: pointer;
}
button:hover { background: #f0ebe3; }
.tabs { display: flex; gap: 4px; margin-bottom: 8px; }
.tab-btn { flex: 1; padding: 8px 6px; font-size: 0.75rem; }
.tab-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
#layer-panels { flex: 1; overflow-y: auto; padding: 8px 10px 16px; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.group { margin-bottom: 6px; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }
.group-header {
  display: flex; align-items: center; gap: 6px; padding: 7px 8px;
  background: #f7f4ee; cursor: pointer; user-select: none;
}
.group-header input[type=checkbox] { flex-shrink: 0; }
.group-title { flex: 1; font-size: 0.82rem; font-weight: 600; }
.group-title:hover { color: var(--accent); text-decoration: underline; }
.group-toggle { color: var(--muted); font-size: 0.75rem; width: 14px; }
.group-body { display: none; padding: 4px 8px 8px 22px; }
.group.open .group-body { display: block; }
.layer-row {
  display: flex; align-items: center; gap: 6px; padding: 3px 0;
  font-size: 0.78rem; line-height: 1.3;
}
.swatch { width: 12px; height: 12px; border-radius: 2px; border: 1px solid rgba(0,0,0,.15); flex-shrink: 0; }
.swatch.dashed { background: transparent !important; border-style: dashed; }
.swatch.dotted { background: transparent !important; border-style: dotted; }
#map-wrap { flex: 1; position: relative; }
#map { width: 100%; height: 100%; }
#map-toolbar {
  position: absolute; top: 10px; right: 10px; z-index: 1000;
  display: flex; gap: 6px;
}
#sidebar-toggle {
  position: absolute; top: 10px; left: 10px; z-index: 1000; display: none;
}
#legend {
  position: absolute; bottom: 24px; right: 10px; z-index: 1000;
  background: rgba(255,255,255,.95); border: 1px solid var(--border);
  border-radius: 6px; max-height: 45vh; overflow: hidden; min-width: 180px;
  box-shadow: 0 2px 8px rgba(0,0,0,.12);
}
#legend-header {
  padding: 8px 10px; font-size: 0.8rem; font-weight: 600; cursor: pointer;
  display: flex; justify-content: space-between; border-bottom: 1px solid var(--border);
}
#legend-body { padding: 8px 10px; overflow-y: auto; max-height: 38vh; }
#legend.collapsed #legend-body { display: none; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.72rem; margin-bottom: 4px; }
#status { padding: 6px 14px; font-size: 0.72rem; color: var(--muted); border-top: 1px solid var(--border); }
@media (max-width: 900px) {
  #sidebar-toggle { display: block; }
  #sidebar { position: absolute; left: 0; top: 0; bottom: 0; box-shadow: 2px 0 12px rgba(0,0,0,.15); }
}
</style>
</head>
<body>
<div id="app">
  <aside id="sidebar">
    <div id="sidebar-header">
      <h1>Bei Xujiaqiao Viewer</h1>
      <div class="global-actions">
        <button id="show-all-global" type="button">Show All Layers</button>
        <button id="hide-all-global" type="button">Hide All Layers</button>
        <button id="collapse-all" type="button">Collapse All</button>
        <button id="expand-all" type="button">Expand All</button>
      </div>
      <label class="abandonment-row">
        <input id="abandonment-mode" type="checkbox">
        <span>Grey out pre–Early WZ layers when Early WZ+ layers are visible (abandonment)</span>
      </label>
      <div class="tabs">
        <button class="tab-btn active" data-tab="compound" type="button">By Compound/Trench</button>
        <button class="tab-btn" data-tab="period" type="button">By Period</button>
      </div>
    </div>
    <div id="layer-panels">
      <div id="panel-compound" class="tab-panel active"></div>
      <div id="panel-period" class="tab-panel"></div>
    </div>
    <div id="status">Loading…</div>
  </aside>
  <div id="map-wrap">
    <button id="sidebar-toggle" type="button">☰ Layers</button>
    <div id="map-toolbar">
      <button id="fit-all" type="button">Fit All</button>
      <button id="toggle-basemap" type="button">Blank Background</button>
      <button id="clear-sketches" type="button">Clear Sketches</button>
    </div>
    <div id="map"></div>
    <div id="legend">
      <div id="legend-header"><span>Legend (Feature Type)</span><span id="legend-chevron">▼</span></div>
      <div id="legend-body"></div>
    </div>
  </div>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js" crossorigin=""></script>
<script src="https://cdn.jsdelivr.net/npm/proj4@2.11.0/dist/proj4.js"></script>
<script>
const FILE_MANIFEST = __MANIFEST__;

const PERIOD_ORDER = [
  "PeriodII","PeriodII-III","PeriodIII","PeriodIII-IVEarly","PeriodIII-IVLate",
  "PeriodIV","PeriodIVEarly","PeriodIVEarly-IVLate","PeriodIVLate",
  "PeriodIVEarly-EarlyWZ","PeriodEarlyWZ","PeriodShang","PeriodShang-ZhouTransition",
  "PeriodShangZhou","PeriodSuiTang","PeriodSongYuan","Unperiodized","recent"
];
const PERIOD_LABELS = {
  PeriodII:"Period II", "PeriodII-III":"Period II–III", PeriodIII:"Period III",
  "PeriodIII-IVEarly":"Period III → IV Early", "PeriodIII-IVLate":"Period III → IV Late",
  PeriodIV:"Period IV", PeriodIVEarly:"Period IV Early", "PeriodIVEarly-IVLate":"Period IV Early → Late",
  PeriodIVLate:"Period IV Late", "PeriodIVEarly-EarlyWZ":"Period IV Early → Early WZ",
  PeriodEarlyWZ:"Early Western Zhou", PeriodShang:"Shang", "PeriodShang-ZhouTransition":"Shang–Zhou Transition",
  PeriodShangZhou:"Shang–Zhou", PeriodSuiTang:"Sui–Tang", PeriodSongYuan:"Song–Yuan",
  Unperiodized:"Unperiodized", recent:"Recent"
};
const TYPE_COLORS = {
  foundation:"#626262", muzang:"#4f953b", huikeng:"#e5b636", daogou:"#becf50", gou:"#becf50",
  keng:"#e5b636", jing:"#4f86c6", lu:"#5f5f5f", jiao:"#e5b636", jisi:"#4f953b", sanshui:"#5f5f5f",
  hangtuqiang:"#626262", hangtugoucao:"#626262", hongshaotu:"#626262", huozao:"#e7969c",
  wengguanzang:"#4f953b", zhuchu:"#626262", zhuji:"#626262", zhudong:"#626262",
  dongwutaiji:"#626262", nanwutaiji:"#626262", xiwutaiji:"#626262", lumian:"#5f5f5f",
  shaotumian:"#e7969c", zao:"#e7969c", dianjimu:"#626262", huangtuaogou:"#becf50", huigou:"#becf50",
  base:"#999999"
};
const OMIT_TYPES = new Set(["mutan","chezhe","jar","interpretation","other","daodong","stairs"]);
const ABANDONMENT_PERIOD_IDX = PERIOD_ORDER.indexOf("PeriodEarlyWZ");
const TYPE_LABELS = {
  foundation:"Foundation (F)", muzang:"Burial (muzang)", huikeng:"Ash pit", daogou:"Ditch",
  gou:"Channel", keng:"Pit", jing:"Well", lu:"Road", jiao:"Cellar", jisi:"Sacrifice",
  sanshui:"Water drainage", hangtuqiang:"Rammed earth wall", hangtugoucao:"Rammed earth trench",
  hongshaotu:"Burnt earth", huozao:"Hearth", wengguanzang:"Urn burial", mutan:"Altar",
  zhuchu:"Post base", zhuji:"Post trace", zhudong:"Post hole", chezhe:"Cart ruts",
  dongwutaiji:"East platform", nanwutaiji:"South platform", lumian:"Road surface",
  shaotumian:"Burnt earth surface", zao:"Stove", xiwutaiji:"West platform",
  dianjimu:"Foundation timber", huangtuaogou:"Yellow earth ditch", huigou:"Ash ditch", base:"Base outline"
};

function isOmittedFile(file) {
  return file.isInterpretation || OMIT_TYPES.has(file.featureType);
}

function colorLuminance(hex) {
  const h = (hex || "#000000").replace("#", "");
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return r * 0.299 + g * 0.587 + b * 0.114;
}

const ROMAN = {I:1,II:2,III:3,IV:4,V:5,VI:6,VII:7,VIII:8,IX:9,X:10};

function romanToInt(s) {
  const m = s.match(/Compound ([IVXLC]+)/);
  return m ? (ROMAN[m[1]] || 99) : 999;
}

function trenchSortKey(t) {
  const n = parseInt(t.replace(/\D/g, ""), 10);
  return isNaN(n) ? 999 : n;
}

function groupLabel(entry) {
  if (entry.compound) return entry.compound;
  if (entry.trenches.length > 1) return entry.trenches.join("–");
  return entry.trenches[0];
}

function layerId(entry, file) {
  return entry.dir + "/" + file.name;
}

function encodePath(path) {
  return path.split("/").map(encodeURIComponent).join("/");
}

function featureSuffix(name) {
  const base = name.replace(/\.geojson$/i, "");
  for (const p of [...PERIOD_ORDER].sort((a,b)=>b.length-a.length)) {
    const marker = "_" + p + "_";
    if (base.includes(marker)) return base.split(marker)[1];
    if (base.endsWith("_" + p)) return "";
  }
  return base;
}

function layerLabelTab1(file) {
  if (file.isBase) return "(Base outline)";
  const pl = file.period ? (PERIOD_LABELS[file.period] || file.period) : "—";
  const suffix = featureSuffix(file.name);
  const tl = TYPE_LABELS[file.featureType] || suffix || file.featureType;
  if (file.featureType === "foundation" && /F\d+/.test(suffix)) return pl + " — " + suffix;
  return pl + " — " + (suffix || tl);
}

function layerLabelTab2(entry, file) {
  const src = groupLabel(entry);
  if (file.isBase) return src + " — Base outline";
  if (file.isInterpretation) return src + " — Interpretation";
  const suffix = featureSuffix(file.name);
  if (file.featureType === "foundation" && /F\d+/.test(suffix)) return src + " — " + suffix;
  return src + " — " + (suffix || TYPE_LABELS[file.featureType] || file.featureType);
}

function buildLayers() {
  const layers = [];
  for (const entry of FILE_MANIFEST) {
    for (const file of entry.files) {
      if (isOmittedFile(file)) continue;
      layers.push({
        id: layerId(entry, file),
        dir: entry.dir,
        name: file.name,
        entry,
        file,
        groupKeyTab1: groupLabel(entry),
        period: file.period,
        featureType: file.featureType,
        isBase: file.isBase,
        isInterpretation: file.isInterpretation,
        labelTab1: layerLabelTab1(file),
        labelTab2: layerLabelTab2(entry, file)
      });
    }
  }
  return layers;
}

function sortGroupsTab1(entries) {
  const compounds = entries.filter(e => e.compound).sort((a,b) => romanToInt(a.compound) - romanToInt(b.compound));
  const trenches = entries.filter(e => !e.compound).sort((a,b) => trenchSortKey(a.trenches[0]) - trenchSortKey(b.trenches[0]));
  return [...compounds, ...trenches];
}

function periodIndex(p) {
  const i = PERIOD_ORDER.indexOf(p);
  return i >= 0 ? i : 999;
}

function sortLayersInGroup(layers) {
  return [...layers].sort((a,b) => {
    if (a.isBase !== b.isBase) return a.isBase ? -1 : 1;
    const pi = periodIndex(a.period) - periodIndex(b.period);
    if (pi !== 0) return pi;
    return (a.featureType || "").localeCompare(b.featureType || "");
  });
}

function sortLayersTab2(layers, groupOrder) {
  const orderMap = new Map(groupOrder.map((g,i) => [g,i]));
  return [...layers].sort((a,b) => {
    const gi = (orderMap.get(a.groupKeyTab1) ?? 999) - (orderMap.get(b.groupKeyTab1) ?? 999);
    if (gi !== 0) return gi;
    return (a.featureType || "").localeCompare(b.featureType || "");
  });
}

function transformCoords(coords) {
  if (typeof coords[0] === "number") {
    const [lng, lat] = proj4("EPSG:3857", "EPSG:4326", coords);
    return [lng, lat];
  }
  return coords.map(c => transformCoords(c));
}

function reprojectGeoJSON(geojson) {
  const clone = JSON.parse(JSON.stringify(geojson));
  for (const f of clone.features || []) {
    if (f.geometry && f.geometry.coordinates) {
      f.geometry.coordinates = transformCoords(f.geometry.coordinates);
    }
  }
  delete clone.crs;
  return clone;
}

function styleForType(featureType, abandoned) {
  if (abandoned) {
    return { color: "#999999", weight: 1, dashArray: "4 4", fillColor: "#bbbbbb", fillOpacity: 0.2 };
  }
  const color = TYPE_COLORS[featureType] || "#7f7f7f";
  if (featureType === "base") return { color: "#999999", weight: 2, dashArray: "6 4", fillOpacity: 0 };
  return { color, weight: 2, fillColor: color, fillOpacity: 0.4 };
}

function isAbandonmentPeriod(period) {
  return period && periodIndex(period) >= ABANDONMENT_PERIOD_IDX;
}

function shouldAbandonLayer(meta) {
  if (!abandonmentMode || meta.isBase || !meta.period) return false;
  const hasEwzPlus = Object.keys(layerState).some(id => layerState[id] && isAbandonmentPeriod(LAYER_BY_ID[id].period));
  return hasEwzPlus && periodIndex(meta.period) < ABANDONMENT_PERIOD_IDX;
}

function refreshAbandonmentStyles() {
  for (const id of Object.keys(leafletLayers)) {
    if (!layerState[id]) continue;
    const meta = LAYER_BY_ID[id];
    const lg = leafletLayers[id];
    const abandoned = shouldAbandonLayer(meta);
    lg.eachLayer(featureLayer => featureLayer.setStyle(styleForType(meta.featureType, abandoned)));
  }
}

const ALL_LAYERS = buildLayers();
const LAYER_BY_ID = Object.fromEntries(ALL_LAYERS.map(l => [l.id, l]));
const layerState = Object.fromEntries(ALL_LAYERS.map(l => [l.id, l.isBase]));
const geoCache = {};
const leafletLayers = {};
const loading = new Set();
let map, osmLayer, blankLayer, activeBasemap = "osm";
let loadedBounds = null;
let abandonmentMode = false;
let drawnItems, drawControl;

const mapEl = document.getElementById("map");
const statusEl = document.getElementById("status");
const panelCompound = document.getElementById("panel-compound");
const panelPeriod = document.getElementById("panel-period");
let activeTab = "compound";

function setStatus(msg) { statusEl.textContent = msg; }

function swatchClass(ft) {
  if (ft === "base") return "swatch dashed";
  return "swatch";
}

function setGroupExpanded(group, expanded) {
  group.classList.toggle("open", expanded);
  const toggle = group.querySelector(".group-toggle");
  if (toggle) toggle.textContent = expanded ? "▼" : "▶";
}

function setAllGroupsExpanded(expanded) {
  document.querySelectorAll("#layer-panels .group").forEach(g => setGroupExpanded(g, expanded));
}

function renderGroup(container, groupId, title, layers, tabName) {
  const group = document.createElement("div");
  group.className = "group open";
  group.dataset.groupId = groupId;
  group.dataset.tab = tabName;

  const header = document.createElement("div");
  header.className = "group-header";

  const toggle = document.createElement("span");
  toggle.className = "group-toggle";
  toggle.textContent = "▼";

  const cb = document.createElement("input");
  cb.type = "checkbox";
  cb.dataset.groupCheckbox = groupId;
  cb.dataset.tab = tabName;
  cb.addEventListener("click", e => e.stopPropagation());
  cb.addEventListener("change", () => {
    const ids = layers.map(l => l.id);
    const turnOn = cb.checked;
    setLayersVisible(ids, turnOn);
  });

  const titleEl = document.createElement("span");
  titleEl.className = "group-title";
  titleEl.textContent = title;
  titleEl.addEventListener("click", e => {
    e.stopPropagation();
    zoomToLayers(layers.map(l => l.id));
  });

  header.appendChild(toggle);
  header.appendChild(cb);
  header.appendChild(titleEl);
  header.addEventListener("click", e => {
    if (e.target.closest("input")) return;
    setGroupExpanded(group, !group.classList.contains("open"));
  });

  const body = document.createElement("div");
  body.className = "group-body";

  for (const layer of layers) {
    const row = document.createElement("label");
    row.className = "layer-row";

    const sw = document.createElement("span");
    sw.className = swatchClass(layer.featureType);
    sw.style.background = TYPE_COLORS[layer.featureType] || "#7f7f7f";

    const lcb = document.createElement("input");
    lcb.type = "checkbox";
    lcb.dataset.layerId = layer.id;
    lcb.dataset.tab = tabName;
    lcb.checked = !!layerState[layer.id];
    lcb.addEventListener("change", () => setLayerVisible(layer.id, lcb.checked));

    const lbl = document.createElement("span");
    lbl.textContent = tabName === "compound" ? layer.labelTab1 : layer.labelTab2;

    row.appendChild(lcb);
    row.appendChild(sw);
    row.appendChild(lbl);
    body.appendChild(row);
  }

  group.appendChild(header);
  group.appendChild(body);
  container.appendChild(group);
}

function buildSidebar() {
  panelCompound.innerHTML = "";
  panelPeriod.innerHTML = "";

  const sortedEntries = sortGroupsTab1(FILE_MANIFEST);
  const groupOrder = sortedEntries.map(groupLabel);

  for (const entry of sortedEntries) {
    const layers = sortLayersInGroup(ALL_LAYERS.filter(l => l.entry === entry));
    renderGroup(panelCompound, "c:" + groupLabel(entry), groupLabel(entry), layers, "compound");
  }

  for (const period of PERIOD_ORDER) {
    const layers = sortLayersTab2(ALL_LAYERS.filter(l => l.period === period && !l.isBase && !l.isInterpretation), groupOrder);
    if (layers.length) renderGroup(panelPeriod, "p:" + period, PERIOD_LABELS[period] || period, layers, "period");
  }

  const special = sortLayersTab2(ALL_LAYERS.filter(l => l.isBase), groupOrder);
  if (special.length) renderGroup(panelPeriod, "p:special", "Base Outlines", special, "period");

  syncAllCheckboxUI();
}

function getGroupState(ids) {
  const on = ids.filter(id => layerState[id]).length;
  if (on === 0) return "unchecked";
  if (on === ids.length) return "checked";
  return "indeterminate";
}

function syncAllCheckboxUI() {
  document.querySelectorAll("input[data-layer-id]").forEach(cb => {
    cb.checked = !!layerState[cb.dataset.layerId];
  });

  document.querySelectorAll(".group").forEach(group => {
    const ids = [...group.querySelectorAll("input[data-layer-id]")].map(cb => cb.dataset.layerId);
    const gcb = group.querySelector("input[data-group-checkbox]");
    if (!gcb || !ids.length) return;
    const st = getGroupState(ids);
    gcb.checked = st === "checked";
    gcb.indeterminate = st === "indeterminate";
  });
}

async function fetchLayer(id) {
  if (geoCache[id]) return geoCache[id];
  if (loading.has(id)) {
    while (loading.has(id)) await new Promise(r => setTimeout(r, 50));
    return geoCache[id];
  }
  loading.add(id);
  const layer = LAYER_BY_ID[id];
  try {
    const res = await fetch(encodePath(layer.id));
    if (!res.ok) throw new Error(res.statusText);
    const raw = await res.json();
    geoCache[id] = reprojectGeoJSON(raw);
    return geoCache[id];
  } finally {
    loading.delete(id);
  }
}

function popupHtml(props, layer) {
  const rows = [
    ["FeatName", props.FeatName], ["Type", props.Type], ["Period", props.Period],
    ["Note", props.Note], ["RelaFeat", props.RelaFeat], ["Source", layer.labelTab2]
  ];
  return "<div style='font-size:12px;min-width:140px'>" +
    rows.filter(([,v]) => v != null && v !== "").map(([k,v]) => "<div><b>" + k + ":</b> " + v + "</div>").join("") +
    "</div>";
}

function addToMap(id) {
  const layerMeta = LAYER_BY_ID[id];
  const gj = geoCache[id];
  if (!gj || leafletLayers[id]) return;

  const lg = L.geoJSON(gj, {
    style: () => styleForType(layerMeta.featureType, shouldAbandonLayer(layerMeta)),
    onEachFeature(feature, featureLayer) {
      featureLayer.bindPopup(popupHtml(feature.properties || {}, layerMeta));
      featureLayer.on("mouseover", function() {
        if (shouldAbandonLayer(layerMeta)) {
          this.setStyle({ weight: 2, fillOpacity: 0.3 });
        } else {
          this.setStyle({ weight: 4, fillOpacity: 0.55 });
        }
      });
      featureLayer.on("mouseout", function() {
        this.setStyle(styleForType(layerMeta.featureType, shouldAbandonLayer(layerMeta)));
      });
    }
  });
  lg.addTo(map);
  leafletLayers[id] = lg;

  const b = lg.getBounds();
  if (b.isValid()) {
    loadedBounds = loadedBounds ? loadedBounds.extend(b) : b;
  }
}

function removeFromMap(id) {
  if (leafletLayers[id]) {
    map.removeLayer(leafletLayers[id]);
    delete leafletLayers[id];
  }
}

async function setLayerVisible(id, visible) {
  layerState[id] = visible;
  if (visible) {
    setStatus("Loading " + id + "…");
    try {
      await fetchLayer(id);
      addToMap(id);
    } catch (e) {
      console.error(e);
      layerState[id] = false;
      setStatus("Failed to load: " + id);
      syncAllCheckboxUI();
      return;
    }
  } else {
    removeFromMap(id);
  }
  syncAllCheckboxUI();
  refreshAbandonmentStyles();
  const on = Object.values(layerState).filter(Boolean).length;
  setStatus(on + " layer(s) visible");
}

async function setLayersVisible(ids, visible) {
  setStatus(visible ? "Showing layers…" : "Hiding layers…");
  for (const id of ids) layerState[id] = visible;
  if (visible) {
    await Promise.all(ids.map(id => fetchLayer(id).catch(e => { console.error(id, e); layerState[id] = false; })));
    ids.forEach(id => { if (layerState[id] && geoCache[id]) addToMap(id); });
  } else {
    ids.forEach(removeFromMap);
  }
  syncAllCheckboxUI();
  refreshAbandonmentStyles();
  const on = Object.values(layerState).filter(Boolean).length;
  setStatus(on + " layer(s) visible");
}

function layersInActiveTab() {
  const panel = activeTab === "compound" ? panelCompound : panelPeriod;
  return [...panel.querySelectorAll("input[data-layer-id]")].map(cb => cb.dataset.layerId);
}

async function zoomToLayers(ids) {
  const visibleIds = ids.filter(id => layerState[id]);
  const toLoad = ids.filter(id => !geoCache[id]);
  if (toLoad.length) {
    setStatus("Loading for zoom…");
    await Promise.all(toLoad.map(id => fetchLayer(id).catch(() => null)));
    toLoad.forEach(id => { if (layerState[id]) addToMap(id); });
  }
  const bounds = L.latLngBounds([]);
  const target = visibleIds.length ? visibleIds : ids;
  for (const id of target) {
    if (!geoCache[id]) continue;
    if (!leafletLayers[id] && layerState[id]) addToMap(id);
    const lg = leafletLayers[id];
    if (lg) {
      const b = lg.getBounds();
      if (b.isValid()) bounds.extend(b);
    } else {
      const tmp = L.geoJSON(geoCache[id]);
      const b = tmp.getBounds();
      if (b.isValid()) bounds.extend(b);
    }
  }
  if (bounds.isValid()) map.fitBounds(bounds.pad(0.1));
}

function buildLegend() {
  const body = document.getElementById("legend-body");
  const usedTypes = [...new Set(ALL_LAYERS.map(l => l.featureType))];
  const entries = usedTypes.map(ft => ({
    ft,
    color: TYPE_COLORS[ft] || "#7f7f7f",
    label: TYPE_LABELS[ft] || ft
  }));
  entries.sort((a, b) => colorLuminance(a.color) - colorLuminance(b.color) || a.label.localeCompare(b.label));
  body.innerHTML = "";
  for (const { ft, color, label } of entries) {
    const item = document.createElement("div");
    item.className = "legend-item";
    const sw = document.createElement("span");
    sw.className = swatchClass(ft);
    sw.style.background = color;
    const lbl = document.createElement("span");
    lbl.textContent = label;
    item.appendChild(sw);
    item.appendChild(lbl);
    body.appendChild(item);
  }
}

function initDrawing() {
  drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);
  drawControl = new L.Control.Draw({
    position: "topleft",
    edit: { featureGroup: drawnItems },
    draw: {
      polygon: true,
      polyline: { shapeOptions: { color: "#c0392b", weight: 3 } },
      rectangle: true,
      marker: true,
      circle: false,
      circlemarker: false
    }
  });
  map.addControl(drawControl);
  map.on(L.Draw.Event.CREATED, e => drawnItems.addLayer(e.layer));
}

function initMap() {
  map = L.map("map", { preferCanvas: true }).setView([34.8, 114.3], 16);
  osmLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 22, attribution: "&copy; OpenStreetMap"
  }).addTo(map);
  blankLayer = L.tileLayer("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==", {
    tileSize: 256, opacity: 1
  });
  document.getElementById("map-wrap").style.background = "#fff";
}

async function init() {
  initMap();
  initDrawing();
  buildSidebar();
  buildLegend();

  const baseIds = ALL_LAYERS.filter(l => l.isBase).map(l => l.id);
  await setLayersVisible(baseIds, true);
  if (loadedBounds && loadedBounds.isValid()) map.fitBounds(loadedBounds.pad(0.05));

  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      activeTab = btn.dataset.tab;
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.toggle("active", b === btn));
      panelCompound.classList.toggle("active", activeTab === "compound");
      panelPeriod.classList.toggle("active", activeTab === "period");
      syncAllCheckboxUI();
    });
  });

  document.getElementById("show-all-global").addEventListener("click", () => setLayersVisible(ALL_LAYERS.map(l => l.id), true));
  document.getElementById("hide-all-global").addEventListener("click", () => setLayersVisible(ALL_LAYERS.map(l => l.id), false));
  document.getElementById("collapse-all").addEventListener("click", () => setAllGroupsExpanded(false));
  document.getElementById("expand-all").addEventListener("click", () => setAllGroupsExpanded(true));
  document.getElementById("abandonment-mode").addEventListener("change", e => {
    abandonmentMode = e.target.checked;
    refreshAbandonmentStyles();
  });
  document.getElementById("clear-sketches").addEventListener("click", () => drawnItems.clearLayers());
  document.getElementById("fit-all").addEventListener("click", () => {
    if (loadedBounds && loadedBounds.isValid()) map.fitBounds(loadedBounds.pad(0.05));
  });
  document.getElementById("toggle-basemap").addEventListener("click", function() {
    if (activeBasemap === "osm") {
      map.removeLayer(osmLayer);
      blankLayer.addTo(map);
      activeBasemap = "blank";
      this.textContent = "OSM Basemap";
    } else {
      map.removeLayer(blankLayer);
      osmLayer.addTo(map);
      activeBasemap = "osm";
      this.textContent = "Blank Background";
    }
  });
  document.getElementById("legend-header").addEventListener("click", () => {
    document.getElementById("legend").classList.toggle("collapsed");
    document.getElementById("legend-chevron").textContent =
      document.getElementById("legend").classList.contains("collapsed") ? "▶" : "▼";
  });
  document.getElementById("sidebar-toggle").addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("collapsed");
  });
}

init().catch(e => { console.error(e); setStatus("Init failed: " + e.message); });
</script>
</body>
</html>
'''


def main():
    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        manifest = json.load(fh)
    manifest_js = json.dumps(manifest, ensure_ascii=False)
    html = HTML_TEMPLATE.replace("__MANIFEST__", manifest_js)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {OUT_PATH} ({len(html)} bytes, {len(manifest)} dirs)")


if __name__ == "__main__":
    main()
