# Turing Pi Docs

Source for **docs.turingpi.com**. Static site built with [Astro Starlight](https://starlight.astro.build); pages are plain Markdown.

## Editing

Every page has a **Suggest an edit** link to its file in this repository; outside contributors get a fork and pull request (see [CONTRIBUTING.md](CONTRIBUTING.md)). The repository must stay public for that to work.


- Pages live in `src/content/docs/docs/<slug>.md`. The file name is the URL: `turing-pi2-intro.md` → `/docs/turing-pi2-intro`.
- Images go in `src/assets/img/` and are referenced relatively: `![](../../../assets/img/board.png)`. They are converted to WebP at build time.
- The left menu is `src/sidebar.json`. A new page shows up there only after you add it.
- Callouts:

  ```md
  :::note[Optional title]
  Text
  :::
  ```

  Types: `note`, `tip`, `caution`, `danger`.

## Running locally

```sh
npm install
npm run dev          # http://localhost:4321
npm run build        # builds to dist/
npm run check-links  # after build: every internal link and #anchor must resolve
```

## Redirects

`public/_redirects` keeps every old ReadMe URL working (renamed pages, group pages, `/v1.1/…`, `/v2.0.0/…`).
When you rename or delete a page, add a line there: `/docs/old-slug  /docs/new-slug  301`.

## Hosting

Cloudflare Pages, connected to this repository: build command `npm run build`, output directory `dist`.
Every push to `main` deploys; branches of this repository get a preview URL. The build runs on Cloudflare, not GitHub Actions.

## Migration from ReadMe

`scripts/readme_export.py` and `scripts/readme_import.py` did the one-off import from ReadMe (Nov 2026).
They can be re-run to pick up edits made on ReadMe before the switch:

```sh
python3 -I scripts/readme_export.py /tmp/readme-export /tmp/readme-img
python3 -I scripts/readme_import.py /tmp/readme-export /tmp/readme-img .
```

The import overwrites `src/content/docs/{docs,page,changelog}`, `src/assets/img`, `src/sidebar.json` and `public/_redirects`. Once edits happen here, do not run it again.
