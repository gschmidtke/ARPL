// ARPL add-in learning, step 2: ribbon inventory. READ-ONLY.
// Lists every control on one ribbon tab: panel | label | command id | control type | tooltip | expanded tooltip,
// plus loaded assemblies whose name contains the tab name (name and version only).
// Run with RevitBridge run_csharp, transaction "none". Show this script to the user before running it.
// It reads Revit's own ribbon (AdWindows) through reflection; it does not open, inspect or decompile the add-in.
// Tested: Revit 2024.3, 2026-11-03. The expanded tooltip (the second paragraph shown when the pointer
// rests on a button) often carries usage rules, e.g. "Close the CSV in Excel before running."
// INPUT: TAB = the tab title as shown on the ribbon.
string TAB = "ZEN";
var adw = AppDomain.CurrentDomain.GetAssemblies().First(a => a.GetName().Name == "AdWindows");
var ribbon = adw.GetType("Autodesk.Windows.ComponentManager").GetProperty("Ribbon").GetValue(null);
object P(object o, string n) => o?.GetType().GetProperty(n)?.GetValue(o);
var tabs = ((System.Collections.IEnumerable)P(ribbon, "Tabs")).Cast<object>().ToList();
var tab = tabs.FirstOrDefault(t => (string)P(t, "Title") == TAB || (string)P(t, "Id") == TAB);
if (tab == null) return new { error = "tab not found", tabs = tabs.Select(t => (string)P(t, "Title")).ToList() };
var rows = new List<string>();
void Walk(object item, string panel, int depth) {
  var text = ((string)P(item, "Text") ?? "").Replace("\r\n", " ").Replace("\n", " ");
  var id = (string)P(item, "Id") ?? "";
  var tip = P(item, "ToolTip"); var tipText = tip as string ?? P(tip, "Content") as string ?? "";
  var exp = P(tip, "ExpandedContent"); var expText = exp as string ?? P(exp, "Content") as string ?? "";
  if (text != "" || id != "") rows.Add($"{panel} | {new string('>', depth)}{text} | {id} | {item.GetType().Name} | {tipText.Replace("\n", " ").Trim()} | {expText.Replace("\r", " ").Replace("\n", " ").Trim()}");
  if (P(item, "Items") is System.Collections.IEnumerable kids) foreach (var k in kids) Walk(k, panel, depth + 1);
}
foreach (var panel in ((System.Collections.IEnumerable)P(tab, "Panels")).Cast<object>()) {
  var src = P(panel, "Source"); var pname = (string)P(src, "Title") ?? "";
  foreach (var it in ((System.Collections.IEnumerable)P(src, "Items")).Cast<object>()) Walk(it, pname, 0);
}
var asm = AppDomain.CurrentDomain.GetAssemblies()
  .Where(a => !a.IsDynamic && a.GetName().Name.IndexOf(TAB, StringComparison.OrdinalIgnoreCase) >= 0)
  .Select(a => a.GetName().Name + " " + a.GetName().Version).ToList();
return new { tab = TAB, revit = uiapp.Application.VersionBuild, count = rows.Count, assemblies = asm, rows };
