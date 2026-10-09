# NovaDyne - checkpoint

Updated: 2026-10-09. Audit reference: main 12114a11c69b4d86cf91a36b43a527a9b08461e3.
Setup publication to main authorized by the user on 2026-10-09. Verify current HEAD.
Verify current HEAD and source before acting; this file does not update itself.

## Implemented at audit reference
- Four machines, FE input with no external machine drain, inventory/menu persistence.
- Fuel (80 FE/t), basic solar (40/0), advanced solar (100/25); 40,000 FE generator buffers.
- Directional energy cables, transaction-safe external insertion, bounded traversal.
- Infinite Water Sink, passive water pipes, 4,000 mB Lithography tank; 1,000 mB/cleaning.
- Six relative item-side modes, optional auto output. Modes do not configure FE/fluid sides.
- PRs #15 and #16 merged; side-config branch has same file tree as audited main.

## Evidence
- Historical PR #16 Build run 36029499769 passed build and server tests.
- Log: 14 required tests passed; 13 NovaDyne test functions are registered.
- Wiki check passed during audit: 27 items, 19 crafts/furnaces, 9 processes.
- No fresh local Java build or client reproduction performed in audit.

## Prioritized work (code inspection findings)
1. Filter each machine input slot and route Processor shift-click by ingredient.
2. Bind progress to recipe identity; decide pause behavior for insufficient FE.
3. Add sided item capability to Fuel Generator, including remainder extraction.
4. Permit safe empty-bucket extraction from Lithography auxiliary slot.
5. Test reload persistence, all horizontal orientations and multi-consumer distribution.
6. Profile repeated per-tick network discovery before optimizing networks.

## Current task
None. Setup only; no gameplay files modified.

## Next suggested task
Only input filters and shift-click. Preserve internal output insertion.
Regression: wrong ingredient rejected by sided capability; shift-click each Processor
ingredient into correct slot regardless of insertion order; output cannot accept
external input; valve slot preserved; no item loss or duplication.

## Last task result
OpenCode configuration, Windows launcher and tutorial prepared for this approved main
submission. No gameplay changes. Config schema and prompt paths validated; Windows
launcher not executed on a Windows host. Fresh runtime tests not run.
