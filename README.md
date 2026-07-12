# Bei Xujiaqiao GeoJSON Viewer

**Live site:** https://ywzhou997.github.io/BeiXujiaqiao/

Interactive map viewer for Bei Xujiaqiao excavation GeoJSON layers.

This repository is **private**. GeoJSON data is only available to collaborators with repo access.

## For collaborators

### 1. Get access

Ask the repo owner to add your GitHub account under **Settings → Collaborators**.

### 2. Clone the repository

```bash
git clone https://github.com/ywzhou997/BeiXujiaqiao.git
cd BeiXujiaqiao
```

### 3. Run the viewer locally

```bash
./serve.sh
```

Or manually:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000/](http://localhost:8000/) in your browser.

> **Important:** Do not open `index.html` directly from the file system (`file://`). The browser must load GeoJSON over HTTP, so a local server is required.

## For the repo owner

### Make the repository private (one-time)

1. Open [github.com/ywzhou997/BeiXujiaqiao](https://github.com/ywzhou997/BeiXujiaqiao)
2. Go to **Settings** → **General**
3. Scroll to **Danger Zone** → **Change repository visibility**
4. Select **Make private** and confirm

### Add collaborators

1. **Settings** → **Collaborators** (or **Manage access**)
2. Click **Add people**
3. Enter their GitHub username or email and choose a role (usually **Read** is enough for viewing)

### Optional: private GitHub Pages (paid plan required)

If you have **GitHub Pro** (or Team/Enterprise), you can host the viewer at a URL visible only to collaborators:

1. **Settings** → **Pages**
2. Source: **Deploy from branch** → `main` → `/ (root)`
3. Under **Pages visibility**, choose **Private** (only available on paid plans)

URL: `https://ywzhou997.github.io/BeiXujiaqiao/`

Without a paid plan, collaborators should use the local server workflow above.

## Project layout

```
BeiXujiaqiao/
├── index.html       # Map viewer (entry point)
├── manifest.json    # Layer manifest source
├── T2/              # Trench GeoJSON files
├── T13 Compound I/
└── ...
```

## Documentation

See [docs/PRD.md](docs/PRD.md) for full product requirements and technical details.
