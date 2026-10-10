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
- Log: 14 required tests passed; 13 NovaDyne test functions were registered at audit.
- Wiki check passed during audit: 27 items, 19 crafts/furnaces, 9 processes.
- Local worktree 2026-10-09: 16 functions registered (3 added); each has a
  data/novadyne/test_instance/*.json entry; JSON validated. No local build or
  client reproduction performed (machine has no Gradle cache; builds need approval).
- Independent static review by novadyne-review on the local diff: filter/recipe matrix
  exact, shift-click no loss/duplication, existing tests compatible. Runtime pending CI.
- Real test result: none. Gradle was not run and GitHub CI was not reached, so no
  passing runtime evidence exists for commit b619098.

## Prioritized work (code inspection findings)
1. Filter each machine input slot and route Processor shift-click by ingredient. (done, local)
2. Bind progress to recipe identity; decide pause behavior for insufficient FE.
3. Add sided item capability to Fuel Generator, including remainder extraction.
4. Permit safe empty-bucket extraction from Lithography auxiliary slot.
5. Test reload persistence, all horizontal orientations and multi-consumer distribution.
6. Profile repeated per-tick network discovery before optimizing networks.

## Current task
Input filters per slot (BlockEntity isItemValidForSlot overrides) and Processor
shift-click routing by ingredient.
Branch feat/input-slot-validation, commit b619098 (local only; NOT pushed).
Changed: Macerator/WaferPress/Processor/Litografia BlockEntities, ProcessorMenu,
LitografiaMenu (bucket routing), CoreSmokeTests (+3 functions slot_input_filters,
sided_input_filters, processor_shift_click) + 3 test_instance datapack entries.
Output slots stay permissive at inventory level (insertResult + existing tests
depend on it); external output protection remains at SidedMachineItemHandler/menu
layer. Litografia bucket slot accepts WATER_BUCKET and empty BUCKET (processCleaning
returns it via insertResult). Main unchanged, worktree clean.

## Blocked
Push, PR to main and GitHub Actions check: no `gh` CLI on this PC, no Git Credential
Manager entry and no GH_TOKEN/GITHUB_TOKEN; push fails with "could not read Username
for 'https://github.com'". Once credentials/gh are available, run:
git push -u origin feat/input-slot-validation
gh pr create --base main --head feat/input-slot-validation

## Next suggested task
Progress bound to recipe identity (task 2). Task 1 runtime confirmation depends on
the next approved push/PR run; migration note below still applies.
- Migration note: saves from before the filters may hold an invalid item in an input
  slot; deserialization does not re-filter, and shift-click merges same-item stacks
  past mayPlace. Item is never lost and canProcess still blocks; clear manually.
