# CLEANUP PLAN

## Sanitization strategy
1. Treat `projects/` and `archive/versions/` as contaminated areas.
2. Preserve only the light representation in `capymind/projects/`.
3. Do not promote full copies as official repository structure.
4. Remove heavy copies in a later manual cleanup step after validation.

## Correct final structure
- Top level with README, reports, manifests, and light directories only.
- `projects/<slug>/` with exactly six derived files per project.
- `archive/` reserved for notes, never raw project dumps.
