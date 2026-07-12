# PRD: Bei Xujiaqiao GeoJSON Layer Viewer

## 1. Overview

A single-page HTML application that renders all GeoJSON vector files from the Bei Xujiaqiao archaeological excavation project on an interactive map. The viewer provides **two tabs** representing two ways to organize the same data:

1. **By Period** — layers grouped by chronological period across all trenches and compounds. **Default tab on load.**
2. **By Compound / Trench** — layers grouped by compound (or by T-number when no compound applies), listed chronologically within each group.

In both views, layers are colored by **feature type** (e.g., all muzang share one color, all F-number foundations share another), and each layer can be toggled on/off via checkboxes.

## 2. Goals

- **G1**: Display all `.geojson` files from every `T*` directory on an interactive map.
- **G2**: Provide per-layer checkboxes so users can show/hide individual GeoJSON layers independently.
- **G3**: Offer two organizational views (tabs) of the same dataset with shared map state.
- **G4**: Color-code features by **type** consistently across both tabs.
- **G5**: Require zero build step — the page must work locally and when hosted as a static site on **GitHub Pages**.
- **G6**: Handle the full dataset (~140 GeoJSON layers across 21 trench groups) without performance issues.
- **G7**: Support bulk toggling at layer, group, and global levels.

## 3. Data Inventory

There are 21 trench directories. Some cover a single trench, others span multiple trenches and/or include a compound designation:

| Directory | Compound | Trench(es) |
|---|---|---|
| `T2/` | — | T2 |
| `T3/` | — | T3 |
| `T4 Compound II/` | Compound II | T4 |
| `T5/` | — | T5 |
| `T5 Compound VIII/` | Compound VIII | T5 |
| `T5 Compound IX/` | Compound IX | T5 |
| `T7/` | — | T7 |
| `T8/` | — | T8 |
| `T9 Compound IV/` | Compound IV | T9 |
| `T10/` | — | T10 |
| `T11 T12 Compound VI/` | Compound VI | T11, T12 |
| `T13 Compound I/` | Compound I | T13 |
| `T14 T15 Compound VII/` | Compound VII | T14, T15 |
| `T16/` | — | T16 |
| `T17 Compound III/` | Compound III | T17 |
| `T18/` | — | T18 |
| `T19/` | — | T19 |
| `T20 Compound V/` | Compound V | T20 |
| `T21T22/` | — | T21, T22 |
| `T23/` | — | T23 |
| `T24/` | — | T24 |

### 3.2 File Types

| Extension | Role |
|---|---|
| `.geojson` | Vector data (FeatureCollections). **Primary display data.** |
| `.qmd` | QGIS layer style metadata. Ignored by the viewer for now. |

### 3.3 File Naming Convention

Each directory contains:

1. **Base file** — `{ID}.geojson` (e.g., `T2.geojson`, `CompoundVI.geojson`). Contains all features for the trench/compound as a single FeatureCollection.
2. **Layer files** — `{ID}_{Period}_{FeatureType}.geojson` (e.g., `T19_PeriodIVEarly_F11.geojson`). Subsets filtered by period and feature type.
3. **Interpretation files** (some directories) — `*Interpretation*.geojson`. Analytical overlays.

### 3.4 GeoJSON Structure

All files share a consistent schema:

```json
{
  "type": "FeatureCollection",
  "name": "<layer name>",
  "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3857" } },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "FeatName": "F19",
        "Type": "F",
        "Note": null,
        "RelaFeat": "F19",
        "Period": "IVEarly"
      },
      "geometry": { "type": "Polygon", "coordinates": [...] }
    }
  ]
}
```

- **CRS**: EPSG:3857 (Web Mercator). Coordinates are in meters.
- **Geometry types**: Primarily `Polygon`.
- **Properties**: `FeatName`, `Type`, `Note`, `RelaFeat`, `Period`.

### 3.5 Chronological Period Order

Periods are sorted from earliest to latest. This order governs both the layer listing within Tab 1 groups and the group ordering in Tab 2.

| Sort Order | Period Key | Display Label |
|---|---|---|
| 1 | `PeriodII` | Period II |
| 2 | `PeriodII-III` | Period II–III |
| 3 | `PeriodIII` | Period III |
| 4 | `PeriodIII-IVEarly` | Period III → IV Early |
| 5 | `PeriodIII-IVLate` | Period III → IV Late |
| 6 | `PeriodIV` | Period IV |
| 7 | `PeriodIVEarly` | Period IV Early |
| 8 | `PeriodIVEarly-IVLate` | Period IV Early → Late |
| 9 | `PeriodIVLate` | Period IV Late |
| 10 | `PeriodIVEarly-EarlyWZ` | Period IV Early → Early WZ |
| 11 | `PeriodEarlyWZ` | Early Western Zhou |
| 12 | `PeriodShang` | Shang |
| 13 | `PeriodShang-ZhouTransition` | Shang–Zhou Transition |
| 14 | `PeriodShangZhou` | Shang–Zhou |
| 15 | `PeriodSuiTang` | Sui–Tang |
| 16 | `PeriodSongYuan` | Song–Yuan |
| 17 | `recent` | Recent |
| 18 | `Unperiodized` | Unperiodized |

> **Tab 2 ordering note:** In the By Period tab, **Base Outlines** appear first (top), chronological period groups follow, and **Unperiodized** appears last. The sort order above still governs layer ordering within Tab 1 groups and general chronology.

### 3.6 Feature Types & Color Coding

Colors are assigned by **feature type**, not by period. All feature names that map to the same type share one hex color. Types marked **Omit = yes** are excluded from the sidebar, map, and legend.

**Rules:**

1. Any `F` + number name (`F2`, `F20F21`, `F23F24F25F26`, etc.) maps to **`foundation`**.
2. Compound suffixes (`underF11_muzang`, etc.) map to the embedded type (`muzang`), not `foundation`.
3. The viewer reads colors from this table. Legend entries are sorted by hex color (see §4.6).

| Feature Type | Display Label | Hex Color | Omit |
|---|---|---|---|
| `foundation` | Foundation (F + number) | `#626262` | |
| `muzang` | Burial (muzang) | `#4f953b` | |
| `huikeng` | Ash pit (huikeng) | `#e5b636` | |
| `daogou` | Ditch (daogou) | `#becf50` | |
| `gou` | Channel (gou) | `#becf50` | |
| `keng` | Pit (keng) | `#e5b636` | |
| `jing` | Well (jing) | `#4f86c6` | |
| `lu` | Road (lu) | `#5f5f5f` | |
| `jiao` | Cellar (jiao) | `#e5b636` | |
| `jisi` | Sacrifice (jisi) | `#4f953b` | |
| `sanshui` | Water drainage (sanshui) | `#5f5f5f` | |
| `hangtuqiang` | Rammed earth wall | `#626262` | |
| `hangtugoucao` | Rammed earth trench | `#626262` | |
| `hongshaotu` | Burnt earth | `#626262` | |
| `huozao` | Hearth (huozao) | `#e7969c` | |
| `wengguanzang` | Urn burial | `#4f953b` | |
| `zhuchu` | Post base (zhuchu) | `#626262` | |
| `zhuji` | Post trace (zhuji) | `#626262` | |
| `zhudong` | Post hole (zhudong) | `#626262` | |
| `dongwutaiji` | East platform | `#626262` | |
| `nanwutaiji` | South platform | `#626262` | |
| `xiwutaiji` | West platform | `#626262` | |
| `lumian` | Road surface | `#5f5f5f` | |
| `shaotumian` | Burnt earth surface | `#e7969c` | |
| `zao` | Stove (zao) | `#e7969c` | |
| `dianjimu` | Foundation timber (dianjimu) | `#626262` | |
| `huangtuaogou` | Yellow earth ditch | `#becf50` | |
| `huigou` | Ash ditch | `#becf50` | |
| `base` | Base outline | `#999999` | |
| `mutan` | Altar (mutan) | — | yes |
| `chezhe` | Cart ruts (chezhe) | — | yes |
| `jar` | Jar | — | yes |
| `interpretation` | Interpretation overlay | — | yes |
| `other` | Other / unclassified | — | yes |

## 4. Functional Requirements

### 4.1 Map Display

| ID | Requirement |
|---|---|
| F-MAP-1 | Use **Leaflet.js** (loaded from CDN) as the mapping library. |
| F-MAP-2 | Transform EPSG:3857 coordinates to EPSG:4326 (lat/lng) for Leaflet display using `proj4js` (CDN). |
| F-MAP-3 | On load, set the map view to a **fixed default bounding box** in WGS84: `(36.1075510, 114.3083653)` and `(36.1060077, 114.3114498)`. **Fit All** still zooms to all currently selected (visible) layers. |
| F-MAP-4 | Provide a tile basemap (OpenStreetMap) with an option to toggle to a blank/white background for print-friendly views. |
| F-MAP-5 | The map state (zoom, pan, visible layers) is **shared** between the two tabs. Switching tabs does not reset the map or remove visible layers. |
| F-MAP-6 | Scroll-wheel and toolbar zoom use **fractional zoom levels** (`zoomSnap: 0`, `zoomDelta: 0.25`). |

### 4.2 Tab System

| ID | Requirement |
|---|---|
| F-TAB-1 | The sidebar has **two tabs** at the top: **"By Period"** (default on load) and **"By Compound/Trench"**. |
| F-TAB-2 | Switching tabs changes only the sidebar organization. The map and all visible layers remain unchanged. |
| F-TAB-3 | Checkbox states are synchronized: if a layer is toggled on in Tab 1, its checkbox also appears checked in Tab 2, and vice versa. |

### 4.3 Tab 1: By Compound / Trench

| ID | Requirement |
|---|---|
| F-T1-1 | Layers are grouped into collapsible sections. Directories that have a compound name are grouped under **the compound name** (e.g., "Compound I", "Compound VI"). Directories with no compound are grouped under **the T-number** (e.g., "T2", "T16", "T21–T22"). |
| F-T1-2 | The groups are sorted: compounds by Roman numeral (I, II, … IX), then standalone trenches by T-number (T2, T3, T5, T7, …). |
| F-T1-3 | Within each group, layers are listed in **chronological order** by period (following the sort order in §3.5). Layers with the same period are sub-sorted alphabetically by feature type. |
| F-T1-4 | Each layer has a checkbox and a human-readable label, e.g., "Period IV Early — F11", with a small color swatch next to it matching the feature-type color. |
| F-T1-5 | The base file (e.g., `T2.geojson`) appears first in the group with label "(Base outline)". |
| F-T1-6 | Each group header has a **group checkbox** that toggles all layers in that group on/off. |
| F-T1-7 | Clicking the group header name **zooms** the map to that compound/trench's extent. |

### 4.4 Tab 2: By Period

| ID | Requirement |
|---|---|
| F-T2-1 | Layers are grouped into collapsible sections by **period key**, sorted chronologically (following the sort order in §3.5). |
| F-T2-2 | Each period section lists **all layer files from all trenches and compounds** that belong to that period. |
| F-T2-3 | Within each period group, layers are sorted by compound/trench (same order as Tab 1), then by feature type alphabetically. |
| F-T2-4 | Each layer label includes the source trench/compound prefix, e.g., "Compound VI — F10", "T19 — muzang". The color swatch reflects the feature type. |
| F-T2-5 | Base files are placed in a special group at the **top** labeled **"Base Outlines"** (interpretation layers are omitted per §3.6). Base outline layers are **deselected by default** on page load. |
| F-T2-7 | The **Unperiodized** period group appears **last** among period groups (after `recent`). |
| F-T2-6 | Each period group header has a **group checkbox** that toggles all layers in that group on/off. |

### 4.5 Bulk Toggle Controls

Users must be able to show/hide layers at three levels. All toggles update the map immediately and stay synchronized across both tabs.

| ID | Requirement |
|---|---|
| F-TOGGLE-1 | **Layer level** — each layer has its own checkbox. |
| F-TOGGLE-2 | **Group level** — each collapsible group header has a checkbox that turns all layers in that group on or off. |
| F-TOGGLE-3 | **Global level** — the sidebar has **"Show All Layers"**, **"Hide All Layers"**, and **"Collapse All"** buttons. Show/Hide affect every layer in the dataset, regardless of tab. Collapse All collapses every group in the active sidebar tab. |
| F-TOGGLE-8 | **Default state on page load** — all sidebar groups start **collapsed**. All layers start **selected (visible)** except **Base outline** layers, which start **deselected**. |
| F-TOGGLE-4 | Group checkboxes use a **tri-state** model: checked (all children on), unchecked (all children off), indeterminate (some children on). |
| F-TOGGLE-5 | Toggling a group on checks all child layer checkboxes in that group. Toggling it off unchecks all child layer checkboxes. |
| F-TOGGLE-6 | Manually changing individual layer checkboxes updates the parent group checkbox state (checked / unchecked / indeterminate). |
| F-TOGGLE-7 | Bulk actions apply at group or global scope, but the resulting visibility state is shared globally on the map. |

**UI placement (sidebar top, above the tabs):**

```
[ Show All Layers ]  [ Hide All Layers ]  [ Collapse All ]

Tab: By Period | By Compound/Trench

▼ [✓] Compound I
    [✓] Period II — muzang
    [ ] Period III — muzang
```

### 4.6 Layer Styling

| ID | Requirement |
|---|---|
| F-STYLE-1 | Assign a distinct color to each **feature type** using the palette defined in §3.6. The same colors apply in both tabs. |
| F-STYLE-2 | Base trench/compound outlines use gray (`#999`) with dashed stroke and no fill. |
| F-STYLE-3 | Interpretation layers use dark gray (`#333`) with dotted stroke and semi-transparent fill. |
| F-STYLE-4 | Display a **map legend** on the map mapping feature-type colors (collapsible, sorted by hex color; types with the same hex color appear as one entry). This legend is independent of the **export legend** (see §4.12). |
| F-STYLE-5 | Each feature type polygon is rendered with a semi-transparent fill (opacity ~0.4) and a solid stroke (opacity 1.0, weight 2). |
| F-STYLE-6 | Omitted feature types (§3.6) do not appear in the legend or sidebar. |

### 4.7 Abandonment Mode

When the user turns on any layer from **Early Western Zhou (`PeriodEarlyWZ`) or later** (per §3.5 sort order), the viewer offers an option to visually signal abandonment of earlier remains.

| ID | Requirement |
|---|---|
| F-ABANDON-1 | A sidebar checkbox: **"Grey out pre–Early WZ layers"** (abandonment mode). |
| F-ABANDON-2 | When abandonment mode is enabled and at least one visible layer is from `PeriodEarlyWZ` or a later period, all **earlier** visible vector layers (period sort order &lt; `PeriodEarlyWZ`) are rendered in grey (`#bbbbbb` fill, `#999999` stroke, reduced opacity). **Stroke style remains solid** — outlines are not dashed. |
| F-ABANDON-3 | Base outline layers are never greyed out. |
| F-ABANDON-4 | When abandonment mode is disabled, or no Early WZ+ layers are visible, all layers revert to their normal feature-type colors. |
| F-ABANDON-5 | Turning on an Early WZ+ layer while abandonment mode is enabled immediately applies grey styling to earlier visible layers. |

### 4.8 Drawing Tool

The map includes a sketching toolbar for annotating the excavation plan.

| ID | Requirement |
|---|---|
| F-DRAW-1 | Use **Leaflet.draw** (CDN) for on-map sketching. |
| F-DRAW-2 | Support drawing **polyline** and **polygon** sketches via the map toolbar (see §4.12). |
| F-DRAW-3 | Drawn features are editable and deletable via **Edit** and **Delete** tools on the map toolbar. |
| F-DRAW-4 | Sketches persist in the browser session only (no server save in V1). |
| F-DRAW-5 | A **"Clear sketches"** button removes all drawn features. |
| F-DRAW-6 | Drawing mode does not interfere with layer checkbox toggling or feature popups when draw mode is off. |

### 4.9 Feature Interaction

| ID | Requirement |
|---|---|
| F-INTERACT-1 | Clicking a feature shows a **popup** with: `FeatName`, `Type`, `Period`, `Note`, `RelaFeat`, and the source file/trench. |
| F-INTERACT-2 | Hovering over a feature highlights it (increased stroke weight or opacity). |

### 4.10 Navigation

| ID | Requirement |
|---|---|
| F-NAV-1 | A **"Fit All"** button (upper-right map toolbar) zooms the map to fit all **currently selected (visible)** layers. |
| F-NAV-2 | Clicking a group header name in either tab zooms to that group's spatial extent. |

### 4.11 Map Toolbar (Upper Right)

Three buttons appear in the upper-right corner of the map:

| ID | Requirement |
|---|---|
| F-TOOL-UR-1 | **Fit All** — zoom the map to fit all currently selected (visible) layers in one view. |
| F-TOOL-UR-2 | **Blank Background** — toggle the basemap to a white/blank background for print-friendly views. Toggles back to OpenStreetMap when clicked again. |
| F-TOOL-UR-3 | **Clear Sketches** — remove all user-drawn sketch features from the map. |

### 4.12 Map Sidebar (Left)

A vertical toolbar on the left side of the map is organized into **three function groups**:

**Group 1 — Zoom**

| ID | Requirement |
|---|---|
| F-TOOL-L-1 | **Zoom In** — increase map zoom by one level. |
| F-TOOL-L-2 | **Zoom Out** — decrease map zoom by one level. |

**Group 2 — Sketch**

| ID | Requirement |
|---|---|
| F-TOOL-L-3 | **Draw Line** — activate polyline drawing mode for sketch annotations. |
| F-TOOL-L-4 | **Draw Polygon** — activate polygon drawing mode for sketch annotations. |
| F-TOOL-L-5 | **Edit Layer** — edit existing sketch features (vertices, shape). |
| F-TOOL-L-6 | **Delete Layer** — delete selected sketch features. |

Sketches persist in the browser session only (no server save in V1). Drawing mode does not interfere with layer checkbox toggling or feature popups when draw mode is off.

**Group 3 — Export / Screenshot**

| ID | Requirement |
|---|---|
| F-TOOL-L-7 | **Draw Screenshot Area** — user draws a rectangle on the map defining the export region. The rectangle has a **transparent fill** (outline only). |
| F-TOOL-L-8 | **Place Scale Bar** — place a draggable, **resizable** scale bar anchored to the **screenshot area** (position stored as a fraction of the screenshot rectangle). The bar maintains its relative position when the map is zoomed or panned. Transparent background. The user adjusts bar width with the corner handle; **ground distance labels snap to whole meters** and are computed from the current map scale (meters per pixel at map center), updating on zoom, pan, or resize. |
| F-TOOL-L-9 | **Legend** — open a panel to select export legend items (deselected by default). The **export legend** is minimalist, distinct from the map legend, draggable and resizable, anchored to the **screenshot area** like the scale bar, with a transparent background. |
| F-TOOL-L-10 | **Download** — temporarily zoom the map to the **maximum extent** of the drawn screenshot area, capture at high resolution, then restore the previous view. The dashed screenshot boundary is **not** included in the exported image. Resize handles are **not** included. Output is at least **1000 × 1000 px**. |

## 5. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NF-1 | **Single HTML entry point** — all CSS and JS inline (except CDN libraries). No build tools. |
| NF-2 | **Static hosting** — must work on **GitHub Pages** with no backend. GeoJSON files are loaded via relative `fetch()` calls. |
| NF-3 | **Local development compatible** — must also work when served via `python3 -m http.server` or similar. |
| NF-4 | **Lazy loading** — GeoJSON files are fetched when their checkbox is toggled on. On startup, all selected (non–base-outline) layers are loaded. |
| NF-5 | **Caching** — once fetched, GeoJSON data is cached in memory so toggling off/on doesn't re-fetch. |
| NF-6 | **Responsive** — the sidebar should be collapsible on small screens. |
| NF-7 | **Synchronized state** — checking/unchecking a layer in one tab is immediately reflected in the other tab, including group and global toggle states. |
| NF-8 | **Path-safe URLs** — directory names with spaces (e.g., `T13 Compound I/`) must be URL-encoded in `fetch()` paths so the app works on GitHub Pages (Linux-hosted, case-sensitive). |
| NF-9 | **No secrets** — the page must not depend on API keys or private services. Basemap tiles must use a free/public tile provider. |

## 6. Technical Approach

### 6.1 Libraries (CDN)

| Library | Version | Purpose |
|---|---|---|
| Leaflet | 1.9.x | Map rendering |
| Leaflet.draw | 1.0.x | On-map sketching (polyline, polygon, rectangle, marker) |
| proj4js | latest | EPSG:3857 → EPSG:4326 coordinate reprojection |

### 6.2 Data Manifest

The file manifest is embedded in the HTML as a JavaScript object. Each entry carries enough metadata to power both tab views:

```javascript
const FILE_MANIFEST = [
  {
    dir: "T2",
    compound: null,        // null = no compound, group by trench in Tab 1
    trenches: ["T2"],
    files: [
      { name: "T2.geojson",                        isBase: true },
      { name: "T2_PeriodIVEarly_F19.geojson",       period: "PeriodIVEarly", featureType: "foundation" },
      { name: "T2_PeriodIVEarly_muzang.geojson",    period: "PeriodIVEarly", featureType: "muzang" },
      { name: "T2_Unperiodized_hangtugoucao.geojson", period: "Unperiodized", featureType: "hangtugoucao" },
      { name: "T2_Unperiodized_daogou.geojson",     period: "Unperiodized", featureType: "daogou" },
    ]
  },
  {
    dir: "T13 Compound I",
    compound: "Compound I",
    trenches: ["T13"],
    files: [
      { name: "CompoundI.geojson",                          isBase: true },
      { name: "CompoundI_PeriodII_muzang.geojson",          period: "PeriodII", featureType: "muzang" },
      { name: "CompoundI_PeriodIII_muzang.geojson",         period: "PeriodIII", featureType: "muzang" },
      { name: "CompoundI_PeriodIVEarly_muzang.geojson",     period: "PeriodIVEarly", featureType: "muzang" },
      { name: "CompoundI_PeriodIVLate_F23F24F25F26.geojson", period: "PeriodIVLate", featureType: "foundation" },
      { name: "CompoundI_PeriodIVLate_muzang.geojson",      period: "PeriodIVLate", featureType: "muzang" },
      { name: "CompoundI_PeriodEarlyWZ_muzang.geojson",     period: "PeriodEarlyWZ", featureType: "muzang" },
      // ...
    ]
  },
  // ...
];
```

### 6.3 Feature Type Classification

Feature type is determined from the filename suffix (the last segment after the period key) using these rules, applied in order:

1. Matches `F\d+` (one or more F-numbers, e.g., `F19`, `F41F42`, `F23F24F25F26`) → `"foundation"`
2. Matches `foundation` → `"foundation"`
3. Matches known type keywords (`muzang`, `huikeng`, `daogou`, `gou`, `keng`, `jing`, `lu`, `jiao`, `jisi`, `sanshui`, `hangtuqiang`, `hangtugoucao`, `hongshaotu`, `huozao`, `wengguanzang`, `mutan`, `zhuchu`, `zhuji`, `zhudong`, `chezhe`, `lumian`, `shaotumian`, `jar`, `zao`, `dongwutaiji`, `nanwutaiji`, `xiwutaiji`) → that keyword
4. Base files (no period/type suffix) → `"base"`
5. Contains `Interpretation` → `"interpretation"`
6. Everything else → `"other"`

### 6.4 Coordinate Handling

GeoJSON files use EPSG:3857 (meters). Leaflet expects EPSG:4326 (degrees). On load, each feature's coordinates are reprojected using `proj4("EPSG:3857", "EPSG:4326", [x, y])`.

### 6.4.1 Default Map View

On page load (after layers are loaded), the map view is set to this fixed extent in WGS84 (lat, lng):

| Corner | Latitude | Longitude |
|---|---|---|
| North-west | 36.1075510 | 114.3083653 |
| South-east | 36.1060077 | 114.3114498 |

The **Fit All** control still zooms to the union of all selected layer extents.

### 6.5 Tab 1 Grouping Logic

```
For each manifest entry:
  if entry.compound is not null:
    group key = entry.compound  (e.g., "Compound I")
  else:
    group key = entry.trenches joined  (e.g., "T2", "T21–T22")

Sort groups:
  1. Compounds first, sorted by Roman numeral (I < II < III < ... < IX)
  2. Standalone trenches second, sorted by T-number numerically

Within each group, sort layers by:
  1. Base file first
  2. Then by period chronological order (§3.5)
  3. Within same period, alphabetically by feature type
```

### 6.6 Tab 2 Grouping Logic

```
For each layer file across all manifest entries:
  group key = layer.period  (e.g., "PeriodIVEarly")

Sort groups by chronological order (§3.5).

Within each group, sort layers by:
  1. Compound/trench order (same as Tab 1 group order)
  2. Then alphabetically by feature type

Special group at the top:
  "Base Outlines" — contains all base files (interpretation layers omitted), deselected by default

Period groups sorted chronologically, except Unperiodized appears last (after recent)
```

### 6.7 Bulk Toggle State Model

All layers share a single visibility state object keyed by a stable layer ID (e.g., `T2/T2_PeriodIVEarly_F19.geojson`). Both tabs read from and write to this shared state.

```javascript
const layerState = {
  "T2/T2_PeriodIVEarly_F19.geojson": true,
  "T2/T2_PeriodIVEarly_muzang.geojson": false,
  // ...
};

function setLayersVisible(layerIds, visible) {
  layerIds.forEach(id => {
    layerState[id] = visible;
    visible ? showOnMap(id) : hideOnMap(id);
  });
  syncAllCheckboxUI(); // updates layer, group, tab, and global controls in both tabs
}

function getGroupState(layerIds) {
  const onCount = layerIds.filter(id => layerState[id]).length;
  if (onCount === 0) return "unchecked";
  if (onCount === layerIds.length) return "checked";
  return "indeterminate";
}
```

Group headers bind their checkbox `checked` / `indeterminate` properties to `getGroupState(...)`. Global buttons call `setLayersVisible(...)` with the full layer ID list.

### 6.8 GitHub Pages Deployment

The viewer is designed to be published as a static site from a GitHub repository.

**Repository layout (recommended):**

```
Bei-Xujiaqiao/                 ← GitHub repo root
├── .nojekyll                  ← disables Jekyll processing (recommended)
├── index.html                 ← main viewer page (GitHub Pages entry point)
├── docs/
│   └── PRD.md
├── T2/
│   ├── T2.geojson
│   └── ...
├── T13 Compound I/
│   ├── CompoundI.geojson
│   └── ...
└── ... (other T* directories)
```

**Deployment options:**

| Option | URL pattern | Notes |
|---|---|---|
| Project site | `https://<user>.github.io/<repo>/` | Set Pages source to `main` branch, `/ (root)` |
| User/org site | `https://<user>.github.io/` | Repo must be named `<user>.github.io` |

**GitHub-specific constraints:**

1. **Relative asset paths** — all GeoJSON `fetch()` URLs must be relative to the page (e.g., `T2/T2.geojson`), not absolute file-system paths.
2. **Spaces in paths** — use `encodeURI()` or `encodeURIComponent()` on path segments when building fetch URLs (e.g., `T13%20Compound%20I/CompoundI.geojson`).
3. **Case sensitivity** — GitHub Pages runs on Linux; filenames and paths must match exactly.
4. **Repository size** — ~140 GeoJSON files may be large. If the repo exceeds GitHub's recommended size limits, consider Git LFS for GeoJSON assets.
5. **No server-side logic** — directory listing is not available; the embedded `FILE_MANIFEST` remains required.
6. **CDN dependencies** — Leaflet and proj4js load from public CDNs; no npm install step at deploy time.

**Publishing steps:**

```bash
# 1. Push the repo to GitHub (all T* directories + index.html included)
git add index.html docs/ T*/
git commit -m "Add GeoJSON viewer"
git push origin main

# 2. In GitHub repo Settings → Pages:
#    Source: Deploy from branch
#    Branch: main, folder: / (root)

# 3. After deployment, open:
#    https://<user>.github.io/<repo>/
```

## 7. File Layout

```
Bei Xujiaqiao/
├── .nojekyll
├── index.html               ← GitHub Pages entry point (same app as viewer.html)
├── docs/
│   └── PRD.md               ← this document
├── T2/
│   ├── T2.geojson
│   ├── T2_PeriodIVEarly_F19.geojson
│   └── ...
├── T13 Compound I/
│   ├── CompoundI.geojson
│   └── ...
└── ... (other T* directories)
```

`index.html` is the canonical deployable page. A local alias such as `viewer.html` is optional for development only.

## 8. Usage

### Local development

```bash
# From the project root, start a local server:
python3 -m http.server 8000

# Then open in browser:
open http://localhost:8000/index.html
```

## 9. Future Enhancements (Out of Scope for V1)

- Parse `.qmd` files to apply QGIS-native styling (colors, stroke widths, fill patterns).
- Timeline slider to animate layers appearing/disappearing by period.
- Export visible layers as a combined GeoJSON or image.
- Search/filter features by `FeatName`, `Type`, or `Period` across all trenches.
- Side-by-side comparison of two trenches or compounds.
- Save/load sketch annotations to local storage or file.
