# MIGRATION PLAN

## Applied logic
- Detect heavy project copies inside the current repository shape.
- Generate one light representation per project in `projects/<slug>/`.
- Keep only derived documentation, manifests, trees, and references.
- Exclude full copies, installed dependencies, and build output from the final structure.

## Classification rules
- `summarize`: create README, summary, and stack notes for projects.
- `index`: generate catalogs, inventories, and manifests.
- `catalog`: register metadata and source paths.
- `reference`: point to original locations without copying content.
- `ignore`: keep heavy, binary, and generated artifacts out of the light repo.
- `review`: register ambiguous items for manual follow-up.
