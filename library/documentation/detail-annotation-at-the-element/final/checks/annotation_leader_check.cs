// Read-only check (run with transaction = none). Reports, for one drafting/detail view:
//  - leader crossings between text-note leaders            (Owner rule R3; proposed REQ-S7-SHEET-022)
//  - leaders whose first segment at the text is not horizontal (R4; proposed REQ-S7-SHEET-023)
//  - element-describing text without a leader                (R1; proposed REQ-S7-SHEET-020) -> listed for human review
//  - same-style duplicate lines and hidden lines buried under visible lines (R5; proposed REQ-S7-SHEET-024)
// A line counts as duplicate only if it is itself >= 90 % covered (compare against the candidate's OWN length,
// not the shorter of the pair - the shorter-of-pair test deleted long WRB lines in the source session).
// Body of: static object Run(UIApplication uiapp, UIDocument uidoc, Document doc, StringBuilder log)
long viewId = 0; // set the view id
var v = doc.GetElement(new ElementId(viewId)) as View;
bool Cross(XYZ p1, XYZ p2, XYZ p3, XYZ p4) { double d(XYZ a, XYZ b, XYZ c) => (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X); return d(p3, p4, p1) * d(p3, p4, p2) < 0 && d(p1, p2, p3) * d(p1, p2, p4) < 0; }
var notes = new FilteredElementCollector(doc, v.Id).OfClass(typeof(TextNote)).Cast<TextNote>().ToList();
var led = notes.Where(t => t.LeaderCount > 0).SelectMany(t => t.GetLeaders().Cast<Leader>().Select(l => (t, l))).ToList();
var segs = led.Select(x => (x.t, s: new[] { (x.l.Anchor, x.l.Elbow), (x.l.Elbow, x.l.End) })).ToList();
var crossings = new List<string>();
for (int i = 0; i < segs.Count; i++) for (int j = i + 1; j < segs.Count; j++)
  if (segs[i].s.Any(a => segs[j].s.Any(b => Cross(a.Item1, a.Item2, b.Item1, b.Item2)))) crossings.Add(segs[i].t.Id + " x " + segs[j].t.Id);
var noShoulder = led.Where(x => Math.Abs(x.l.Anchor.Y - x.l.Elbow.Y) > 1e-6 || x.l.Anchor.DistanceTo(x.l.Elbow) < 1e-6).Select(x => x.t.Id.ToString()).ToList();
var noLeader = notes.Where(t => t.LeaderCount == 0).Select(t => t.Id + ": " + (t.Text.Length > 40 ? t.Text.Substring(0, 40) : t.Text)).ToList();
var cs = new FilteredElementCollector(doc, v.Id).OfClass(typeof(CurveElement)).Cast<CurveElement>().Where(c => c.GeometryCurve is Line).ToList();
var dimRefs = new HashSet<ElementId>(new FilteredElementCollector(doc, v.Id).OfClass(typeof(Dimension)).Cast<Dimension>().SelectMany(d => d.References.Cast<Reference>().Select(r => r.ElementId)));
cs = cs.Where(c => !dimRefs.Contains(c.Id)).ToList(); // dimension witness lines are reviewed with their dimension
var dup = new List<string>(); double tol = 1.0 / 304.8;
for (int i = 0; i < cs.Count; i++) for (int j = 0; j < cs.Count; j++) { if (i == j) continue;
  var a = (Line)cs[i].GeometryCurve; var b = (Line)cs[j].GeometryCurve;
  if (Math.Abs(Math.Abs(a.Direction.DotProduct(b.Direction)) - 1) > 1e-4) continue;
  if (b.Direction.CrossProduct(a.GetEndPoint(0) - b.GetEndPoint(0)).GetLength() > tol) continue;
  double t1 = (a.GetEndPoint(0) - b.GetEndPoint(0)).DotProduct(b.Direction), t2 = (a.GetEndPoint(1) - b.GetEndPoint(0)).DotProduct(b.Direction);
  double ov = Math.Min(b.Length, Math.Max(t1, t2)) - Math.Max(0, Math.Min(t1, t2));
  bool sameStyle = cs[i].LineStyle.Id == cs[j].LineStyle.Id, buried = cs[i].LineStyle.Name == "<Hidden Lines>" && cs[j].LineStyle.Name != "<Hidden Lines>";
  if (ov >= 0.9 * a.Length && (sameStyle && (a.Length < b.Length || (a.Length == b.Length && i > j)) || buried)) dup.Add(cs[i].Id + " covered by " + cs[j].Id); }
return new { pass = crossings.Count == 0 && noShoulder.Count == 0 && dup.Count == 0, crossings, noShoulder, dup, noLeader_review = noLeader };
