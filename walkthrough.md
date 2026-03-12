# Maintenance Walkthrough - 2026-03-12

- Merged PRs `#277`, `#272`, `#275`, `#278`, and `#271` via GitHub squash merge after bringing contributor branches into a mergeable state and refreshing PR bodies against the quality checklist in `.github/MAINTENANCE.md`.
- Verified PR `#271` locally with `npm run validate:references` and `npm run test` before merge; confirmed `#269` auto-closed from the merged PR body.
- Added a user-facing Windows truncation recovery guide at `docs/users/windows-truncation-recovery.md`, linked it from `README.md`, `docs/users/faq.md`, `docs/users/getting-started.md`, and `docs/integrations/jetski-cortex.md`, and credited the workflow to issue `#274`.
- Updated `skills/metasploit-framework/SKILL.md` to remove the remote installer flow, require an existing Metasploit installation, and add the required offensive-skill warning.
- Ran the required maintenance validations after the direct fixes:
  - `npm run validate`
  - `npm run validate:references`
  - `npm run chain`
  - `npm run catalog`
- Final release prep, issue closure comments, and verification were completed on `main`.
