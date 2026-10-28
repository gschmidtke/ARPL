// ARPL-CRD-0001 reference script (RevitBridge run_csharp, Revit 2024). Read before running; adapt model titles, keys and categories.
// Assumes every model is already open in the session (link worksets closed) and all share one internal origin and shared position.
// Read-only on the models; writes one CSV per pair and a run log to the report folder.
var docs = uiapp.Application.Documents.Cast<Document>().ToList();
Document D(string k) => docs.First(d => d.Title.Contains(k));
var M = new Dictionary<string,(string doc,string key,BuiltInCategory[] cats)>{
 {"HVAC",("HVAC","Snowdon Towers-HVAC",new[]{BuiltInCategory.OST_DuctCurves,BuiltInCategory.OST_DuctFitting})},
 {"PLU",("Plumbing","Snowdon Towers- PLUMBING",new[]{BuiltInCategory.OST_PipeCurves,BuiltInCategory.OST_PipeFitting})},
 {"ELE",("Electrical","Snowdon Towers-ELECTRICAL",new[]{BuiltInCategory.OST_CableTray,BuiltInCategory.OST_CableTrayFitting,BuiltInCategory.OST_Conduit,BuiltInCategory.OST_ConduitFitting})},
 {"STR",("Structural","Snowdon Towers-STRUCTURAL",new[]{BuiltInCategory.OST_StructuralFraming,BuiltInCategory.OST_StructuralColumns})},
 {"CEIL",("Architectural","Snowdon Towers-ARCHITECTURE",new[]{BuiltInCategory.OST_Ceilings})}};
// Clash matrix: (moving side, fixed side). Week 1 used all nine pairs below in two calls (60 s bridge limit).
var PAIRS = new[]{ ("HVAC","STR"),("PLU","STR"),("ELE","STR"),("HVAC","PLU"),("HVAC","ELE"),("PLU","ELE"),("HVAC","CEIL"),("PLU","CEIL"),("ELE","CEIL") };
var opt = new Options { DetailLevel = ViewDetailLevel.Fine };
var cache = new Dictionary<string, List<Solid>>();
List<Solid> solids(Document d, Element e) {
  string k = d.Title + "|" + e.Id; if (cache.TryGetValue(k, out var r)) return r; r = new List<Solid>();
  var g = e.get_Geometry(opt);
  void walk(GeometryElement ge) { foreach (var o in ge) { if (o is Solid so && so.Volume > 1e-6) r.Add(so); else if (o is GeometryInstance gi) walk(gi.GetInstanceGeometry()); } }
  if (g != null) walk(g); cache[k] = r; return r; }
string lvl(Document d, Element e) {
  var l = d.GetElement(e.LevelId) as Level; if (l != null) return l.Name;
  foreach (var bp in new[]{BuiltInParameter.RBS_START_LEVEL_PARAM, BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM, BuiltInParameter.FAMILY_LEVEL_PARAM, BuiltInParameter.SCHEDULE_LEVEL_PARAM}) { var p = e.get_Parameter(bp); if (p != null && p.StorageType == StorageType.ElementId && d.GetElement(p.AsElementId()) is Level lv) return lv.Name; }
  return ""; }
string q(string s) => "\"" + (s ?? "").Replace("\"","'") + "\"";
var dir = System.IO.Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), @"<PROJECT>\REPORTS\<date>\Clashes");
System.IO.Directory.CreateDirectory(dir);
var summary = new List<string>();
foreach (var (a, b) in PAIRS) {
  var sw = System.Diagnostics.Stopwatch.StartNew();
  var A = M[a]; var B = M[b]; var da = D(A.doc); var db = D(B.doc);
  var fb = new ElementMulticategoryFilter(B.cats.ToList());
  var rows = new List<string>{"pair,model_a,category_a,family_type_a,uid_a,id_a,level_a,model_b,category_b,family_type_b,uid_b,id_b,level_b,volume_cf,x,y,z"};
  foreach (var ea in new FilteredElementCollector(da).WherePasses(new ElementMulticategoryFilter(A.cats.ToList())).WhereElementIsNotElementType().ToElements()) {
    var bb = ea.get_BoundingBox(null); if (bb == null) continue;
    var sa = solids(da, ea); if (sa.Count == 0) continue;
    foreach (var eb in new FilteredElementCollector(db).WherePasses(fb).WhereElementIsNotElementType().WherePasses(new BoundingBoxIntersectsFilter(new Outline(bb.Min, bb.Max)))) {
      double vol = 0; XYZ c = null;
      foreach (var x1 in sa) foreach (var x2 in solids(db, eb)) { try { var x = BooleanOperationsUtils.ExecuteBooleanOperation(x1, x2, BooleanOperationsType.Intersect); if (x != null && x.Volume > 1e-4) { vol += x.Volume; c ??= x.ComputeCentroid(); } } catch { } }
      if (vol > 0) rows.Add(string.Join(",", a + "x" + b, A.key, q(ea.Category.Name), q(ea.Name), ea.UniqueId, ea.Id, q(lvl(da, ea)), B.key, q(eb.Category.Name), q(eb.Name), eb.UniqueId, eb.Id, q(lvl(db, eb)), vol.ToString("0.00000"), c.X.ToString("0.00"), c.Y.ToString("0.00"), c.Z.ToString("0.00")));
    }
  }
  System.IO.File.WriteAllLines(System.IO.Path.Combine(dir, $"CLASH_{a}_x_{b}.csv"), rows);
  summary.Add($"{a}x{b}: {rows.Count - 1} in {sw.Elapsed.TotalSeconds:0.0}s");
  System.IO.File.AppendAllLines(System.IO.Path.Combine(dir, "clash_run_log.txt"), new[]{DateTime.Now.ToString("s") + " " + summary.Last()});
}
return string.Join("\n", summary);
