# Restore a cloud link to the state its link matrix defines

**Intent:** a repair run brings every link of a host back to its link matrix row, the way linking created it: the right cloud model, exactly once, at the shared position, associated with the shared site, pinned, on its workset. Nothing is left for a person to clean up, and no dialog stops an unattended batch (owner rule, 2026-11-10).

Tested 2026-11-10 in Revit 2024.3 on the Snowdon Towers sample federation (ACC). Cases: link moved 11-28 m and rotated, link type removed, link unloaded, link on another workset, duplicate instance, Overlay/Attachment change, a wrong model GUID in the matrix, several deviations at once. Each case ran twice; the second run had to change nothing.
