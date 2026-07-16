## Type of change

- [ ] New funding record
- [ ] New funding opportunity
- [ ] Update to existing entry
- [ ] Other (docs/site/CI)

## Checklist

- [ ] Filename follows `YYYY-funder-slug-lead-topic.md` (or lives under `rolling/` for opportunities without a fixed deadline)
- [ ] `slug` frontmatter field matches the filename
- [ ] All required frontmatter fields are filled in (see `schemas/`)
- [ ] Dates are ISO 8601 (`YYYY-MM-DD`)
- [ ] `end_date` (if applicable) is on/after `start_date`
- [ ] Amount is a plain number; currency is a 3-letter ISO code
- [ ] For funding records: `consent_confirmed: true`, and I have confirmed every named individual agreed to be listed
- [ ] I ran `quarto preview` (or at least `python scripts/validate_frontmatter.py <file>`) locally
