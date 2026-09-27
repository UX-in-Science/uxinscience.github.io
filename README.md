# UX in Science website

An accessible, responsive, multipage website built with [Eleventy](https://www.11ty.dev/) and Nunjucks. The visual and interaction rules live in [`docs/DESIGN.md`](docs/DESIGN.md).

## Get started

You need Node.js and npm. Use an active Node.js LTS release.

```sh
npm ci
npm start
```

Eleventy prints the local preview URL when it starts and rebuilds the site when source files change. Port `8080` is the default; if that port is occupied, Eleventy selects another one.

Create a production build with:

```sh
npm run build
```

The generated static site is written to `_site/`, including the root `CNAME` file for the custom domain. Deploy this directory. Do not edit generated files; builds overwrite them, but do not automatically remove stale output from deleted or renamed source files. Use a fresh output directory for production deployments.

## Project structure

```text
.
├── src/                         Site source
│   ├── _data/                   Global navigation and content data
│   ├── _includes/
│   │   ├── layouts/             Shared page shells
│   │   └── partials/            Header and footer
│   ├── assets/                  Published CSS and selected logo files
│   ├── ux-resources/            UX Resources overview and sub-pages
│   ├── communities/             Communities page
│   ├── education-training/      Education & Training page
│   ├── about/                   About and contact page
│   ├── research-design/         Legacy URL redirect
│   └── index.html               Homepage template
├── docs/
│   ├── DESIGN.md                Design-system and accessibility rules
│   └── brand-assets/            Brand guide and retained logo artifacts
├── tools/generation/            Brand and logo generation utilities
├── eleventy.config.js           Eleventy directories and asset copying
├── package.json                 Commands and dependencies
└── README.md                    Contributor guide
```

## Site map

- `/` — Home
- `/news/` — News feed (under Home)
- `/ux-resources/` — UX Resources overview
- `/ux-resources/research/` — UX Research
- `/ux-resources/design/` — UX Design
- `/ux-resources/engineering/` — UX Engineering
- `/communities/` — Communities
- `/education-training/` — Education & Training
- `/about/` — About and contact

`/research-design/` is retained as a redirect for older links.

## Contributing

### Before making a change

1. Install the locked dependencies with `npm ci`.
2. Start the preview server with `npm start`.
3. Read [`docs/DESIGN.md`](docs/DESIGN.md) before changing layout, color, typography, interaction, or accessibility behavior.
4. Keep unrelated changes out of the same contribution.

### Edit content

Page content lives in `src/` as Nunjucks templates. Front matter at the top of each page controls its shared layout metadata:

```yaml
---
layout: layouts/interior.njk
title: Page title
summary: A concise page introduction.
description: A search-friendly page description.
compactHero: true
showBreadcrumbs: true
---
```

UX Resources sub-pages also define their parent breadcrumb and active navigation section:

```yaml
section: ux-resources
parentTitle: UX Resources
parentUrl: /ux-resources/
```

Use one unique `h1` per page. Start content sections at `h2`, keep link text descriptive, and write summaries that still make sense outside their surrounding page.

### Change navigation

Edit `src/_data/site.json` for the primary navigation. The `children` array under UX Resources powers the header dropdown. Keep URLs trailing-slash consistent.

If you add or rename a UX Resources page, also update `src/_data/uxResources.json` when that data is used by page content or future components.

### Add a page

1. Create a directory under `src/` that matches the desired URL.
2. Add an `index.njk` file with front matter and `layout: layouts/interior.njk`.
3. Add the route to `src/_data/site.json` when it belongs in primary navigation.
4. Add breadcrumbs using `showBreadcrumbs`, or `parentTitle` and `parentUrl` for a nested page.
5. Run a production build and inspect the page at narrow and wide viewport sizes.

### Add a news or blog post

The news feed at `/news/` automatically lists posts tagged `news`, newest publication date first. Copy `src/news/a-space-for-scientific-ux/index.njk` into a new directory under `src/news/`, keeping `tags: [news]` and `section: home`. Update its content and quoted `published` date. The feed uses the title, author, date, and lede from the post; no manual feed entry is needed.

Copy `src/posts/example/index.njk` to `src/posts/your-post/index.njk` to start a post at `/posts/your-post/`. Preview the complete example at `/posts/example/`.

Use `layout: layouts/post.njk` and supply `title`, `description`, `lede`, `published` (a quoted `"YYYY-MM-DD"` date), and an `author` object with `name`, `bio`, and `email`. Set `postType` to a label such as `News` or `Blog`; it defaults to `Article`. Replace the example text and author details before publishing.

Write paragraphs and headings below the front matter, starting body sections at `h2`. The layout adds the title, lede, byline, formatted publication date, and author bio automatically. The bio accepts a few sentences of plain text. Optional `author.image` and `author.imageAlt` fields replace the bundled decorative placeholder with a portrait and appropriate alternative text.

For optional sidebar boxes, use a `sidebar` list; each item has a `title` and a `paragraphs` list, plus optional `url` and `linkText`. Omit `sidebar` entirely for a single-column article. Sidebars stack after the narrative on small screens.

For an inline callout, place this markup between paragraphs. Use a unique heading ID for each box and choose the heading level that fits its surrounding section:

```html
<aside class="post-callout" aria-labelledby="post-note">
  <h3 id="post-note">Key takeaway</h3>
  <p>A short supporting explanation.</p>
</aside>
```

### Homepage carousel

The homepage carousel displays the three newest posts tagged `news`, followed by entries in `src/_data/homeHighlights.json`. Edit that file to highlight another page or a section using a URL such as `/communities/#section-id` (the destination must have that ID). Each entry needs `label`, `title`, `summary`, `url`, and `linkText`. Use an empty list to show news only.

The compact carousel shows one entry at a time and loops every six seconds, with Previous, Next, and Pause/Play controls. Hovering pauses rotation temporarily; keyboard focus or manual navigation stops it until Play is selected. Rotation also pauses in background tabs. Reduced-motion users start with autoplay off and receive no transition animation. Automatic changes are not announced to screen readers; manual changes announce the position. Without JavaScript, all entries remain visible as stacked cards; controls are hidden. With fewer than two entries, controls stay hidden.

### Change shared presentation

- Shared document structure: `src/_includes/layouts/`
- Header and footer: `src/_includes/partials/`
- Design tokens and component styles: `src/assets/css/styles.css`
- Selected site logos: `src/assets/logos/`

Prefer existing CSS tokens and components. Keep core content and navigation functional without JavaScript. Do not copy experimental files from `docs/brand-assets/` directly into templates; publish intentionally selected assets through `src/assets/`.

## Quality checklist

Before opening a pull request or handing off a change:

- Run `npm run build` and resolve all Eleventy errors.
- Confirm the changed page has one `h1` and ordered heading levels.
- Test all new or changed links.
- Check keyboard focus, navigation dropdowns, and visible focus styles.
- Check the layout at `320px` and at a desktop width; there should be no horizontal page scrolling.
- Check light and dark color schemes when changing color or imagery.
- Provide meaningful alternative text for informative images and empty alternative text for decorative images.
- Avoid unnecessary client-side JavaScript, tracking, or third-party requests.

## Commit and pull-request guidance

Use a short, action-oriented commit message, such as `Add engineering resource page` or `Refine mobile navigation`. In the pull request, describe:

- what changed;
- why it changed;
- how it was tested;
- any accessibility or content considerations;
- screenshots for visible design changes.

## Brand and generation files

The files under `docs/brand-assets/` document the retained brand explorations and final guide. Scripts and intermediate generation artifacts are kept under `tools/generation/` so they do not mix with deployable website source. The website build only publishes files under `src/assets/`.
