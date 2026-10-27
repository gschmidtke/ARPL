# Masterplan from a neutral rebuild package: floors, DirectShape envelopes and domain-based grids

**Intent:** Rebuild a 13-building masterplan in an empty Revit project from a compact, tool-neutral rebuild package (8 levels, 22 floor-profile prototypes placed as 48 floors, 13 exact mass envelopes as triangle face loops), then create reference grids per building, without re-reading the original source model and without inventing walls, rooms or structure.

Builds on ARPL-GEO-0004 (staging, idempotent tags, visual gate), adapted for a masterplan: stages are levels, floors, envelopes, grids. The upstream reading of the source belongs to USG, not ARPL.

Measured (Revit 2024, laptop): 8 levels 0.3 s; 48 floors 2.1 s; 12 envelopes 0.05 s; one 5,907-triangle envelope 0.37 s; 361 grids including the delete of the old set 1.3 s.
