# Contributing to the Bioconductor Funding Hub

Thanks for helping build a shared record of Bioconductor-related funding. This guide covers both
kinds of entries: **funding records** (past/ongoing awards) and **funding opportunities** (open or
upcoming calls).

## Adding a past funding record

1. Copy [`_templates/funding-record-template.md`](_templates/funding-record-template.md).
2. Rename it to `YYYY-funder-slug-lead-surname-short-topic.md` (lowercase, hyphen-separated) and
   place it under `funding-records/<year>/`, where `<year>` is the award's start year. Create the
   year folder if it doesn't exist yet.
   - Example: `funding-records/2023/2023-czi-eoss-lun-scran-scaling.md`
3. Fill in every frontmatter field — see the field reference below, or the full schema at
   [`schemas/funding-record.schema.json`](schemas/funding-record.schema.json).
4. Fill in the `## Objectives`, `## Summary / outcomes`, and (optional but encouraged) `## Lessons
   learned` sections in prose.
5. Set `consent_confirmed: true` **only after** confirming every named individual (lead, co-leads,
   team members) has agreed to be listed publicly with these details. See **Consent**, below.
6. Open a pull request.

## Adding a funding opportunity

1. Copy [`_templates/funding-opportunity-template.md`](_templates/funding-opportunity-template.md).
2. Rename it to `YYYY-funder-slug-short-name.md` and place it under
   `funding-opportunities/<year>/`, where `<year>` is the deadline's year — or under
   `funding-opportunities/rolling/` if the call has no fixed deadline (`deadline_type: rolling`).
3. Fill in the frontmatter and the `## Description` / `## Notes for applicants` sections. See
   [`schemas/funding-opportunity.schema.json`](schemas/funding-opportunity.schema.json) for the
   full field reference.
4. Open a pull request.

## Field reference

### Funding record — required fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | Human-readable project title |
| `slug` | string | Must equal the filename without `.md` |
| `status` | `ongoing` \| `completed` | |
| `project_lead` | list of `{name, github?, orcid?}` | Always a list, even for one person |
| `lead_display` | string | Comma-separated names matching `project_lead` (+ `co_leads` if relevant) — used for the listing table, since Quarto can't render the structured list as a table column |
| `funder` | string | |
| `start_date` / `end_date` | `YYYY-MM-DD` | `end_date` is a best estimate while `status: ongoing` — edit later if extended |
| `amount` | number | No currency symbols/commas |
| `currency` | string | 3-letter ISO 4217 code, e.g. `USD` |
| `categories` | list of string | 2-4 tags; powers the site's filter chips |
| `consent_confirmed` | boolean | Must be `true` to merge — see **Consent** below |

Optional: `co_leads`, `team_members` (same shape as `project_lead`), `funder_program`, `grant_id`,
`amount_note`, `related_opportunity` (slug of the opportunity entry this was awarded under, if
tracked), `related_packages` (Bioconductor package names).

### Funding opportunity — required fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | |
| `slug` | string | Must equal the filename without `.md` |
| `funder` | string | |
| `deadline_type` | `fixed` \| `rolling` \| `estimated` | |
| `deadline` | `YYYY-MM-DD` | Required if `deadline_type: fixed` |
| `amount_min` / `amount_max` | number | At least one required |
| `currency` | string | 3-letter ISO 4217 code |
| `eligibility_notes` | string | Who can apply |
| `url` | string | Link to the call |
| `categories` | list of string | Filter chips: typically funder + status |
| `status` | `open` \| `closed` \| `archived` | |

Optional: `program`, `topics` (free-form keywords, not shown as filter chips), `submitted_records`
(slugs of any funding-record entries that resulted from this call).

## Consent

Funding amounts and awardee names are usually already public (funders publish them), but this
repository aggregates them into one much more visible, searchable place. Before setting
`consent_confirmed: true`, confirm with every named individual that they're comfortable being
listed here with these details. If someone previously listed later wants their name removed or
redacted, open an issue and a maintainer will handle it promptly.

## What happens after you open a PR

A GitHub Actions check validates your frontmatter automatically (required fields, valid dates,
`slug` matching the filename, consent attestation, etc.) — if it fails, the PR will show exactly
what to fix. A maintainer then reviews for accuracy and tone (not structural correctness, which CI
already covers) and merges. The site rebuilds and redeploys within a couple of minutes of merging.

## Previewing locally

```sh
quarto preview
```

To self-check your frontmatter before opening a PR:

```sh
pip install -r requirements.txt
python scripts/validate_frontmatter.py path/to/your-new-file.md
```

## Updating an existing entry

Same PR flow — edit the file in place. Common updates: marking a record `ongoing` → `completed`,
extending an `end_date`, or marking an opportunity `open` → `closed`.

## Style

Keep prose concise and factual. Avoid marketing language. Link to real artifacts where possible
(GitHub releases, package pages, publications, the funder's own award page).
