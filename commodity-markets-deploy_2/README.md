# Commodity Markets Dashboard

A free, open-source commodity markets dashboard displaying USDA, EIA, CFTC, and ECB data.

## Quick Start

1. Create a new GitHub repository
2. Push these files to the `main` branch
3. Go to **Settings → Pages → Source** and select **GitHub Actions**
4. The site will deploy automatically on push

Your dashboard will be live at `https://<username>.github.io/<repo-name>/`

## Alternative: Netlify

1. Create a Netlify account at netlify.com
2. Drag and drop the project folder onto the Netlify dashboard
3. Done — Netlify gives you a URL immediately

## Architecture

- **`index.html`** — Entry point, loads React 18 + Chart.js 4 + Babel from CDN
- **`app.jsx`** — Single-file React application (~5,000 lines) with all components and data
- **`.github/workflows/deploy.yml`** — GitHub Actions workflow for automatic deployment

## Current Status

**Prototype v4** — All data is representative/simulated. The dashboard structure, navigation, charts, and interactions are fully functional.

## Data Sources (for future live integration)

| Source | Data | Frequency | API |
|--------|------|-----------|-----|
| USDA NASS | Crop progress, slaughter, cold storage, hogs & pigs, oilseed crushing | Weekly/Monthly | quickstats.nass.usda.gov |
| USDA AMS | Boxed beef & pork cutout | Daily | marketnews.usda.gov |
| USDA FAS | Export sales, export inspections | Weekly | apps.fas.usda.gov |
| USDA PSD | World balance sheets | Monthly | apps.fas.usda.gov/PSDOnline |
| USDA OCE | WASDE | Monthly | usda.gov/oce/commodity/wasde |
| EIA | Ethanol, petroleum, natural gas | Weekly | api.eia.gov |
| CFTC | Commitment of Traders | Weekly | cftc.gov |
| ECB | FX rates | Daily | data.ecb.europa.eu |
| USDM | Drought monitor | Weekly | droughtmonitor.unl.edu |

All sources are free and most require no API key.

## Tech Stack

- React 18 (CDN, no build step)
- Chart.js 4.4
- Babel Standalone (JSX transpilation in browser)
- Pure CSS (no framework)
- GitHub Pages / Netlify (static hosting)
