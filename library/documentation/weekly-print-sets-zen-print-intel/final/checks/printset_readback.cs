// ARPL-DOC-0003 validation check: print set content and read-back. READ-ONLY (no transaction, no writes).
// Run with RevitBridge run_csharp, transaction "none", on the active model. Show this script to the user before running it.
// Before the set exists it lists the content (expected, skipped); afterwards it compares the set with the rule.
// INPUTS: SET = print set name; SCHEDULES_COUNT = true when schedule-only and panel-schedule sheets belong in the set.
string SET = "Project-current";
bool SCHEDULES_COUNT = true;
var d = uiapp.ActiveUIDocument.Document;
var sheets = new FilteredElementCollector(d).OfClass(typeof(ViewSheet)).Cast<ViewSheet>().Where(s => !s.IsTemplate).OrderBy(s => s.SheetNumber).ToList();
var take = new HashSet<int>(); var expected = new List<string>(); var skipped = new List<string>(); var schedOnly = new List<string>();
foreach (var s in sheets) {
  if (s.IsPlaceholder) { skipped.Add(s.SheetNumber + " placeholder"); continue; }
  int vps = s.GetAllViewports().Count;
  int sch = new FilteredElementCollector(d, s.Id).OfClass(typeof(ScheduleSheetInstance)).Cast<ScheduleSheetInstance>().Count(x => !x.IsTitleblockRevisionSchedule);
  int pan = new FilteredElementCollector(d, s.Id).OfClass(typeof(Autodesk.Revit.DB.Electrical.PanelScheduleSheetInstance)).GetElementCount();
  if (vps > 0 || (SCHEDULES_COUNT && sch + pan > 0)) { take.Add(s.Id.IntegerValue); expected.Add(s.SheetNumber); if (vps == 0) schedOnly.Add(s.SheetNumber + (pan > 0 ? " panel" : " schedule")); }
  else skipped.Add(s.SheetNumber + " " + s.Name + (sch + pan > 0 ? ": schedule only" : ": no views"));
}
var set = new FilteredElementCollector(d).OfClass(typeof(ViewSheetSet)).Cast<ViewSheetSet>().FirstOrDefault(v => v.Name == SET);
if (set == null) return new { check = "ARPL-DOC-0003/printset_readback", model = d.Title, pass = false, set_existed = false, expected_count = expected.Count, expected, schedule_only = schedOnly, skipped };
var have = set.Views.Cast<View>().Select(v => v.Id.IntegerValue).ToHashSet();
var add = take.Except(have).Select(i => ((ViewSheet)d.GetElement(new ElementId(i))).SheetNumber).ToList();
var rem = have.Except(take).Select(i => d.GetElement(new ElementId(i))?.Name).ToList();
int nonSheet = set.Views.Cast<View>().Count(v => !(v is ViewSheet));
return new { check = "ARPL-DOC-0003/printset_readback", model = d.Title, pass = add.Count == 0 && rem.Count == 0 && nonSheet == 0, set_existed = true,
  count = have.Count, expected = expected.Count, would_add = add, would_remove = rem, non_sheet_views = nonSheet, schedule_only = schedOnly, skipped };
