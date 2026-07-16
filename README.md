# Bioconductor Funding Hub

A community-maintained record of funding relevant to the [Bioconductor](https://bioconductor.org)
project: past/existing funding that community members can learn from, and upcoming funding
opportunities worth applying to together.

**Site:** https://bioconductor.github.io/funding-hub/ (once published — see Setup below)

## Repository layout

- `funding-records/` — past and ongoing funding, one Markdown file per award, organized by year.
- `funding-opportunities/` — open/upcoming calls, one Markdown file per opportunity.
- `_templates/` — copy these to add a new entry.
- `schemas/` — JSON Schemas that define and validate the frontmatter fields for each collection.
- `scripts/validate_frontmatter.py` — the same validation logic CI runs, runnable locally.
- `.github/workflows/` — CI (`validate-content.yml`) and site publishing (`publish.yml`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide to adding or updating an entry.

## Local development

```sh
quarto preview
```

requires [Quarto](https://quarto.org/docs/get-started/) installed locally.

## Setup (one-time, for whoever stands this repo up on GitHub)

1. Push this repository to GitHub (e.g. under the `Bioconductor` org, or a personal account to
   start).
2. In **Settings → Pages**, set **Source** to "GitHub Actions" (the `publish.yml` workflow handles
   the rest on every push to `main`).
3. Update `site-url` and `repo-url` in [`_quarto.yml`](_quarto.yml) to match the final repo
   location if it differs from `Bioconductor/funding-hub`.

## License

Content is published under [CC BY 4.0](LICENSE).
