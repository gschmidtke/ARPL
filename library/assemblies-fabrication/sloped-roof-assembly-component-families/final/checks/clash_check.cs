// ARPL-ASM-0006 validation check: clash check across assemblies. READ-ONLY (no transaction, no writes).
// Run with RevitBridge run_csharp, transaction "none". Show this script to the user before running it.
// Edit ASSEMBLY_PREFIXES and ALLOW for your model. ALLOW lists intended contacts as "Comments A x Comments B" (order-free).
// Members are identified by their Comments value (the piece kind), as written by the ARPL build scripts.
string[] ASSEMBLY_PREFIXES = { "ROOF", "EXT WALL" };
var ALLOW = new HashSet<string> { "End rafter x Outlooker", "Batt R-19 x Outlooker" };
string K(Element e) => e?.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.AsString() ?? "";
string Pair(string a, string b) => string.CompareOrdinal(a, b) <= 0 ? a + " x " + b : b + " x " + a;
var allow = new HashSet<string>(ALLOW.Select(p => { var s = p.Split(new[] { " x " }, StringSplitOptions.None); return Pair(s[0], s[1]); }));
var asms = new FilteredElementCollector(doc).OfClass(typeof(AssemblyInstance)).Cast<AssemblyInstance>().Where(a => ASSEMBLY_PREFIXES.Any(p => a.Name.StartsWith(p))).ToList();
var pool = asms.SelectMany(a => a.GetMemberIds()).ToList();
var unexpected = new Dictionary<string, int>(); var allowed = new Dictionary<string, int>(); 
var tol = 1 / 304.8; var sw = System.Diagnostics.Stopwatch.StartNew();
var boxes = pool.Select(i => (id: i, bb: doc.GetElement(i)?.get_BoundingBox(null))).Where(x => x.bb != null).ToList();
bool Over(BoundingBoxXYZ a, BoundingBoxXYZ b) => a.Min.X < b.Max.X - tol && b.Min.X < a.Max.X - tol && a.Min.Y < b.Max.Y - tol && b.Min.Y < a.Max.Y - tol && a.Min.Z < b.Max.Z - tol && b.Min.Z < a.Max.Z - tol;
for (int i = 0; i < boxes.Count; i++) {
  var cand = new List<ElementId>(); for (int j = i + 1; j < boxes.Count; j++) if (Over(boxes[i].bb, boxes[j].bb)) cand.Add(boxes[j].id);
  if (cand.Count == 0) continue; var e = doc.GetElement(boxes[i].id);
  foreach (var h in new FilteredElementCollector(doc, cand).WherePasses(new ElementIntersectsElementFilter(e)).ToElementIds()) {
    var p = Pair(K(e), K(doc.GetElement(h))); var bucket = allow.Contains(p) ? allowed : unexpected; bucket[p] = (bucket.TryGetValue(p, out var v) ? v : 0) + 1; } }
return new { check = "ARPL-ASM-0006/clash_check", pass = unexpected.Count == 0, assemblies = asms.Select(a => a.Name + ":" + a.GetMemberIds().Count).ToList(), unexpected, allowed, seconds = Math.Round(sw.Elapsed.TotalSeconds, 1) };
