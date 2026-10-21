import json, math
# ---- inputs from ADU-01 (mm) ----
X0, X1, Y0, Y1 = -3983, 8040.8, -1172.7, 2494.8          # framing outer faces = slab edge
EDGE_W, EDGE_D, SLAB_T = 305, 406, 102                    # thickened edge 12in wide x 16in below top, slab 4in
MAX_S, END_MAX, END_MIN, BOLT_CLR = 1219, 305, 60, 35    # anchor spacing <= 4 ft (assumed, engineer to confirm), ends <= 12 in
walls = {  # plate segments along the wall axis, the fixed coordinate, stud axes
 "North": dict(fixed=("y",2425), segs=[(-3983,8041)], studs=[-3964,-3862,-3577,-3170,-2764,-2357,-1951,-1545,-1138,-732,-325,81,487,894,1300,1707,2113,2519,2926,3332,3739,4145,4551,4958,5364,5771,6177,6583,6990,7396,7803,7920,8022]),
 "South": dict(fixed=("y",-1103), segs=[(-3983,-2950),(-1426,-663),(861,1624),(3148,8041)], studs=[-3964,-3862,-3745,-3338,-3007,-2969,-1407,-1369,-900,-720,-682,880,918,1132,1567,1605,3167,3205,3570,3977,4383,4790,5196,5602,6009,6415,6577,6615,6822,7275,7313,7634,7920,8022]),
 "East":  dict(fixed=("x",7971), segs=[(-1033,2355)], studs=[-1014,-896,-490,-83,323,729,1136,1542,1949,2336]),
 "West":  dict(fixed=("x",-3913), segs=[(-1033,2355)], studs=[-1014,-627,-220,186,593,999,1405,1812,2218,2336]),
}
def anchors(seg, studs):
    a,b = seg; st=sorted(s for s in studs if a-20 <= s <= b+20)
    bays=[(p+q)/2 for p,q in zip(st,st[1:]) if q-p-38 >= 2*BOLT_CLR]
    bays=sorted(c for c in bays if a+END_MIN <= c <= b-END_MIN)
    first=[c for c in bays if c-a <= END_MAX]; out=[max(first) if first else bays[0]]
    while b-out[-1] > END_MAX:
        nxt=[c for c in bays if out[-1] < c <= out[-1]+MAX_S]
        if not nxt: break
        out.append(max(nxt))
    if b-out[-1] > END_MAX or len(out) < 2: out.append(bays[-1])
    return sorted(set(round(x) for x in out))
A=[]; report=[]
for name,w in walls.items():
    ax,val=w["fixed"]
    for seg in w["segs"]:
        pts=anchors(seg,w["studs"])
        gaps=[q-p for p,q in zip(pts,pts[1:])]; ends=(pts[0]-seg[0], seg[1]-pts[-1])
        mind=min(min(abs(p-s) for s in w["studs"]) for p in pts)
        report.append(dict(wall=name,segment=seg,count=len(pts),max_gap=max(gaps) if gaps else 0,ends=ends,min_dist_to_stud=round(mind)))
        for i,p in enumerate(pts): A.append(dict(id=f"AB-{name[0]}{len(A)+1:02d}",x=p if ax=="y" else val,y=val if ax=="y" else p,wall=name))
# ---- plumbing stub-ups (DWV + supply) ----
P=[dict(id="WC",what='WC flange 3" (12" from finished wall)',x=7888-305,y=504,d=102),
   dict(id="SH",what='Shower drain 2"',x=7065,y=1902,d=76),
   dict(id="LAV",what='Lavatory drain 1-1/2"',x=7625,y=-560,d=51),
   dict(id="KS",what='Kitchen sink drain 2"',x=352,y=2080,d=64),
   dict(id="WS",what="Water service + PEX manifold (cold in, hot out to kitchen), under vanity",x=7470,y=-200,d=64)]
# ---- quantities ----
L,Wd=(X1-X0)/1000,(Y1-Y0)/1000; area=L*Wd; perim=2*(L+Wd)
v_slab=area*SLAB_T/1000; v_edge=(EDGE_W/1000)*((EDGE_D-SLAB_T)/1000)*(perim-4*EDGE_W/1000); v=v_slab+v_edge
cy=v*1.30795; order=math.ceil((cy*1.08)*2)/2
bars5=2*(perim+4*0.76+6*0.76)/6.096
q=dict(area_m2=round(area,2),area_sf=round(area*10.764),perimeter_m=round(perim,2),concrete_m3=round(v,2),concrete_cy=round(cy,2),order_cy=order,rebar_5_20ft_bars=math.ceil(bars5),wwf_sheets_8x20=math.ceil(area*10.764*1.1/160),anchors=len(A))
inner=(X0+EDGE_W+50,X1-EDGE_W-50,Y0+EDGE_W+50,Y1-EDGE_W-50)
for p in P: p['clear_of_edge']=inner[0]<=p['x']<=inner[1] and inner[2]<=p['y']<=inner[3]
print([ (p['id'],p['clear_of_edge']) for p in P])
json.dump(dict(slab=dict(x0=X0,x1=X1,y0=Y0,y1=Y1,edge_w=EDGE_W,edge_d=EDGE_D,t=SLAB_T),anchors=A,plumbing=P,quantities=q,anchor_report=report),open("slab_layout.json","w"),indent=1)
for r in report: print(r)
print(q)
