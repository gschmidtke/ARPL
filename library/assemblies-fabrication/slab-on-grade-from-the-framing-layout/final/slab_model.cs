// ARPL: slab on grade 4in with thickened edge, shower recess, anchor bolts, plumbing stub-ups; terrace -50
double X0 = -3983, X1 = 8040.8, Y0 = -1172.7, Y1 = 2494.8, EW = 305, ED = 406, T = 101.6, REC = 51;
double RX0 = 6229, RX1 = 7901.1, RY0 = 1462, RY1 = 2355.1;   // shower recess (to framing faces)
string AN = "AB-N01,-3720,2425;AB-N02,-2560,2425;AB-N03,-1342,2425;AB-N04,-528,2425;AB-N05,690,2425;AB-N06,1504,2425;AB-N07,2722,2425;AB-N08,3536,2425;AB-N09,4754,2425;AB-N10,5568,2425;AB-N11,6786,2425;AB-N12,7862,2425;AB-S13,-3804,-1103;AB-S14,-3172,-1103;AB-S15,-1134,-1103;AB-S16,-810,-1103;AB-S17,1025,-1103;AB-S18,1350,-1103;AB-S19,3388,-1103;AB-S20,4586,-1103;AB-S21,5806,-1103;AB-S22,6718,-1103;AB-S23,7777,-1103;AB-E24,7971,-955;AB-E25,7971,120;AB-E26,7971,1339;AB-E27,7971,2142;AB-W28,-3913,-820;AB-W29,-3913,390;AB-W30,-3913,1608;AB-W31,-3913,2277", PL = "WC,7583,504,102;SH,7065,1902,76;LAV,7625,-560,51;KS,352,2080,64;WS,7470,-200,64";
var res = new Dictionary<string, object>(); var fc = Bridge.Failures(); string step = "";
var lvl = new FilteredElementCollector(doc).OfClass(typeof(Level)).Cast<Level>().First(l => l.Name == "L1");
XYZ Pt(double x, double y, double z = 0) => new XYZ(Bridge.Mm(x), Bridge.Mm(y), Bridge.Mm(z));
CurveLoop Rect(double x0, double y0, double x1, double y1, double z = 0) { var p = new[] { Pt(x0, y0, z), Pt(x1, y0, z), Pt(x1, y1, z), Pt(x0, y1, z) }; var l = new CurveLoop(); for (int i = 0; i < 4; i++) l.Append(Line.CreateBound(p[i], p[(i + 1) % 4])); return l; }
CurveLoop Circ(double x, double y, double z, double dia) { var c = Pt(x, y, z); var l = new CurveLoop(); l.Append(Arc.Create(c, Bridge.Mm(dia / 2), 0, Math.PI, XYZ.BasisX, XYZ.BasisY)); l.Append(Arc.Create(c, Bridge.Mm(dia / 2), Math.PI, 2 * Math.PI, XYZ.BasisX, XYZ.BasisY)); return l; }
var made = new List<ElementId>();
void Tag(Element e, string kind, string mark) { e.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set(kind); if (mark != null) e.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.Set(mark); made.Add(e.Id); }
ElementId DS(BuiltInCategory cat, string kind, string mark, Solid s, ElementId mat) { var ds = DirectShape.CreateElement(doc, new ElementId(cat)); ds.SetShape(new GeometryObject[] { s }); ds.Name = kind; Tag(ds, kind, mark); return ds.Id; }
try {
using (var tx = new Transaction(doc, "ARPL: slab on grade")) { var o = tx.GetFailureHandlingOptions(); o.SetFailuresPreprocessor(fc); o.SetForcedModalHandling(false); o.SetClearAfterRollback(true); tx.SetFailureHandlingOptions(o); tx.Start();
  step = "materials";
  var conc = new FilteredElementCollector(doc).OfClass(typeof(Material)).Cast<Material>().First(m => m.Name == "Concrete - Cast-in-Place Concrete");
  var steel = new FilteredElementCollector(doc).OfClass(typeof(Material)).Cast<Material>().FirstOrDefault(m => m.Name.ToLower().Contains("steel") || m.Name.ToLower().Contains("metal"));
  var pvc = new FilteredElementCollector(doc).OfClass(typeof(Material)).Cast<Material>().FirstOrDefault(m => m.Name == "RB PVC");
  if (pvc == null) { pvc = doc.GetElement(Material.Create(doc, "RB PVC")) as Material; pvc.Color = new Color(235, 235, 235); }
  step = "floor type";
  var ft = new FilteredElementCollector(doc).OfClass(typeof(FloorType)).Cast<FloorType>().FirstOrDefault(t => t.Name == "ARPL Slab on Grade 4in");
  if (ft == null) { ft = (new FilteredElementCollector(doc).OfClass(typeof(FloorType)).Cast<FloorType>().First(t => t.Name == "Concrete 4\"")).Duplicate("ARPL Slab on Grade 4in") as FloorType;
    var cs = CompoundStructure.CreateSingleLayerCompoundStructure(MaterialFunctionAssignment.Structure, Bridge.Mm(T), conc.Id); cs.EndCap = EndCapCondition.NoEndCap; ft.SetCompoundStructure(cs); }
  step = "slab";
  var slab = Floor.Create(doc, new List<CurveLoop> { Rect(X0, Y0, X1, Y1), Rect(RX0, RY0, RX1, RY1) }, ft.Id, lvl.Id);
  Tag(slab, "Slab on grade 4in", "SL-1");
  var rec = Floor.Create(doc, new List<CurveLoop> { Rect(RX0, RY0, RX1, RY1) }, ft.Id, lvl.Id);
  rec.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(Bridge.Mm(-REC)); Tag(rec, "Slab recess (curbless shower) -51", "SL-2");
  step = "thickened edge";
  var ring = GeometryCreationUtilities.CreateExtrusionGeometry(new List<CurveLoop> { Rect(X0, Y0, X1, Y1, -ED), Rect(X0 + EW, Y0 + EW, X1 - EW, Y1 - EW, -ED) }, XYZ.BasisZ, Bridge.Mm(ED - T), new SolidOptions(conc.Id, ElementId.InvalidElementId));
  var recBox = GeometryCreationUtilities.CreateExtrusionGeometry(new List<CurveLoop> { Rect(RX0, RY0, RX1, RY1, -REC - T) }, XYZ.BasisZ, Bridge.Mm(T + REC), new SolidOptions(conc.Id, ElementId.InvalidElementId));
  var ring2 = BooleanOperationsUtils.ExecuteBooleanOperation(ring, recBox, BooleanOperationsType.Difference);
  DS(BuiltInCategory.OST_StructuralFoundation, "Thickened edge 12x16in, 2 #5 cont.", "SL-E", ring2, conc.Id);
  step = "anchors";
  int na = 0; foreach (var a in AN.Split(';')) { var f = a.Split(','); double x = double.Parse(f[1]), y = double.Parse(f[2]);
    var s = GeometryCreationUtilities.CreateExtrusionGeometry(new List<CurveLoop> { Circ(x, y, -178, 12.7) }, XYZ.BasisZ, Bridge.Mm(178 + 64), new SolidOptions(steel?.Id ?? ElementId.InvalidElementId, ElementId.InvalidElementId));
    DS(BuiltInCategory.OST_GenericModel, "Anchor bolt 1/2x10in J (7in embed)", f[0], s, steel?.Id ?? ElementId.InvalidElementId); na++; }
  step = "stub-ups";
  var pl = new List<string>(); foreach (var p in PL.Split(';')) { var f = p.Split(','); double x = double.Parse(f[1]), y = double.Parse(f[2]), dd = double.Parse(f[3]);
    bool inRec = x > RX0 && x < RX1 && y > RY0 && y < RY1; double top = (inRec ? -REC : 0) + 75;
    var s = GeometryCreationUtilities.CreateExtrusionGeometry(new List<CurveLoop> { Circ(x, y, -ED, dd + 8) }, XYZ.BasisZ, Bridge.Mm(top + ED), new SolidOptions(pvc.Id, ElementId.InvalidElementId));
    DS(BuiltInCategory.OST_GenericModel, "Plumbing stub-up " + f[0], "PS-" + f[0], s, pvc.Id); pl.Add(f[0] + (inRec ? " (in recess)" : "")); }
  step = "terrace";
  var ter = doc.GetElement(new ElementId(1263461L)) as Floor; ter.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).Set(Bridge.Mm(-50));
  step = "delete placeholder";
  var del = doc.Delete(new ElementId(1232239L)); res["placeholder deleted (with dependents)"] = del.Count;
  doc.Regenerate();
  step = "assembly";
  var ai = AssemblyInstance.Create(doc, made, new ElementId(BuiltInCategory.OST_StructuralFoundation));
  res["assembly id"] = ai.Id.Value;
  res["anchors"] = na; res["stub-ups"] = pl; res["made"] = made.Count;
  tx.Commit(); }
using (var t2 = new Transaction(doc, "ARPL: slab assembly name")) { t2.Start(); var ai = doc.GetElement(new ElementId((long)res["assembly id"])) as AssemblyInstance; ai.AssemblyTypeName = "SLAB - On Grade 4in"; res["assembly"] = ai.AssemblyTypeName + " members " + ai.GetMemberIds().Count; t2.Commit(); }
step = "clash";
var asmEl = new FilteredElementCollector(doc).OfClass(typeof(AssemblyInstance)).Cast<AssemblyInstance>().Where(a => !a.Name.StartsWith("SLAB")).SelectMany(a => a.GetMemberIds()).ToList();
var cl = new Dictionary<string, int>();
foreach (var id in made) { var e = doc.GetElement(id); if (e == null) continue; foreach (var h in new FilteredElementCollector(doc, asmEl).WherePasses(new ElementIntersectsElementFilter(e)).ToElements()) { var k = (e.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString() ?? "").Split('(')[0].Trim() + " x " + (h.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.AsString() ?? h.Name); cl[k] = (cl.TryGetValue(k, out var v) ? v : 0) + 1; } }
res["clash vs walls/roof"] = cl; res["errors"] = fc.Errors; return res;
} catch (Exception ex) { res["error"] = step + ": " + ex.GetType().Name + ": " + ex.Message; return res; }