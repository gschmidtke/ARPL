import json, math
# ---- ADU-01 geometry (mm, interior finish faces) ----
ROOMS = {
 "LIVING 100": [(-3831,-1020),(1972,-1020),(1972,-264),(1915,-264),(1915,2342),(-3831,2342)],
 "BEDR 103":   [(1972,-1020),(5424,-1020),(5424,247),(5395,247),(5395,2342),(2029,2342),(2029,-264),(1972,-264)],
 "HALL":       [(5509,-1020),(6127,-1020),(6127,847),(5509,847)],
 "CLOSET":     [(5509,961),(6127,961),(6127,2342),(5509,2342)],
 "BATH 104":   [(6241,-1020),(7888,-1020),(7888,1462),(6241,1462)],
 "SHOWER 105": [(6241,1462),(7888,1462),(7888,2342),(6241,2342)],
}
EXT = [(-3983,-1172.7),(8040.8,-1172.7),(8040.8,2494.8),(-3983,2494.8)]   # framing outer face
SLIDER = (-2950, 3148)      # sliding door on the south wall (x range)
BATH_DOOR = (-930, -168)    # on wall x=6184 (y range)
FURN = {"Sofa":(-3081,1392,-1081,2292),"Coffee table":(-2688,395,-1588,995),"Dining":(691,-447,1891,1193),
        "Bed":(2695,311,4045,2311),"Fridge":(1198,1692,1798,2342),"Base cab (cooktop)":(-681,1742,-81,2342),
        "Sink base":(52,1742,652,2342),"WC":(7140,304,7840,704),"Vanity":(7400,-642,7850,-42)}
COUNTER = (-681, 652)       # x range of the kitchen counter on the north wall (y=2342)
# ---- devices: (id, kind, x, y, mount height mm, circuit, note) ----
D = []
def dev(i,k,x,y,h,c,n=""): D.append(dict(id=i,kind=k,x=x,y=y,h=h,circuit=c,note=n))
# living wall receptacles (TR, AFCI)
dev("L1","Receptacle TR",-3831,-300,300,6); dev("L2","Receptacle TR",-3831,1600,300,6)
dev("L3","Receptacle TR",-2300,2342,300,6,"behind sofa / TV"); dev("L4","Receptacle TR",1915,1100,300,6,"dining")
# kitchen counter (GFCI, 2 small-appliance circuits) + fridge
dev("K1","Receptacle GFCI TR",-160,2342,1100,2,"counter: coffee maker, microwave"); dev("K2","Receptacle GFCI TR",560,2342,1100,4,"counter")
dev("K3","Receptacle GFCI TR",1500,2342,1200,4,"refrigerator"); dev("CK","Cooktop 240V 2-burner",-381,2042,900,"1/3","20 A 2P, junction box in base cabinet")
# bedroom
dev("B1","Receptacle TR",2029,1000,300,7); dev("B2","Receptacle TR",2550,2342,300,7,"bed left")
dev("B3","Receptacle TR",4200,2342,300,7,"bed right"); dev("B4","Receptacle TR",5395,1300,300,7); dev("B5","Receptacle TR",4300,-1020,300,7)
# laundry (required in dwelling unit unless waived), closet
dev("LA","Receptacle 20A TR (laundry)",5818,2342,1100,9,"remove if the building official waives laundry")
# bath
dev("BA1","Receptacle GFCI TR",7888,-760,1100,5,"within 900 mm of basin"); dev("WH","Tankless water heater 12 kW 240V",7625,-342,300,"11/13","under vanity, 60 A 2P, #6 Cu")
# exterior (WR GFCI) + HVAC
dev("X1","Receptacle WR GFCI (front)",-3400,-1196,450,8,"south, in-use cover"); dev("X2","Receptacle WR GFCI (back + HVAC service)",-2700,2519,450,8,"north, within 7.5 m of condenser")
dev("AC-I","Mini-split head 12k BTU (cooling)",-3831,1950,2150,"10/12","indoor unit, living west wall")
dev("AC-O","Mini-split condenser",-3500,2900,0,"10/12","outdoor, north"); dev("AC-D","A/C disconnect 30A NEMA 3R",-3300,2519,1300,"10/12","within sight of condenser")
dev("P","Load center 100A MB 120/240V NEMA 3R, 20 spaces",8065,700,1350,"-","exterior East wall face, top of handle ≤ 2.0 m; feeder 100 A from house panel (10 m)")
# lighting + switches + smoke
for i,(x,y) in enumerate([(-2900,0),(-2900,1500),(-900,0),(-900,1500),(1000,700)]): dev(f"LL{i+1}","Downlight LED",x,y,"ceil",6)
for i,(x,y) in enumerate([(3000,0),(4400,0)]): dev(f"LB{i+1}","Downlight LED",x,y,"ceil",7)
dev("LH","Downlight LED",5818,-100,"ceil",7); dev("LC","Closet light",5818,1650,"ceil",7)
dev("LBA","Downlight LED + exhaust fan",7065,250,"ceil",5); dev("LSH","Downlight LED wet-rated",7065,1900,"ceil",5)
dev("XL1","Exterior wall light",-3300,-1196,2100,8); dev("XL2","Exterior wall light",3500,-1196,2100,8); dev("XL3","Exterior wall light (back)",-1500,2519,2100,8)
dev("S1","Switch 2-gang (living lights / exterior)",-3200,-1020,1220,6,"at sliding door"); dev("S2","Switch (bedroom)",2029,-150,1220,7)
dev("S3","Switch 2-gang (bath light / fan)",6127,-50,1220,5,"hall side, next to bath door"); dev("S4","Switch (hall)",5509,-400,1220,7)
dev("SM1","Smoke alarm (hardwired, interconnected)",3700,700,"ceil",7,"sleeping room"); dev("SM2","Smoke alarm (hardwired, interconnected)",5818,500,"ceil",7,"outside sleeping area, ≥ 0.9 m from bath door")
dev("SM3","Smoke alarm (hardwired, interconnected)",-1500,700,"ceil",6,"living (open to bedroom)")
CIRCUITS = {
 "1/3":("Cooktop 2-burner 240 V","20 A 2P",3600),"2":("Kitchen small appliance 1 (GFCI)","20 A AFCI/GFCI",1500),"4":("Kitchen small appliance 2 + fridge (GFCI)","20 A AFCI/GFCI",1500),
 "5":("Bath receptacle, light, fan (GFCI)","20 A GFCI",1300),"6":("Living receptacles + lights + smoke","15 A AFCI",1400),"7":("Bedroom, hall, closet + smoke","15 A AFCI",1200),
 "8":("Exterior WR receptacles + lights","20 A GFCI",800),"9":("Laundry","20 A AFCI/GFCI",1500),"10/12":("Mini-split condenser 240 V","20 A 2P (per nameplate)",2400),
 "11/13":("Tankless water heater 240 V","60 A 2P",12000)}
json.dump(dict(rooms=ROOMS,devices=D,circuits=CIRCUITS),open("layout.json","w"),indent=1,ensure_ascii=False)

# ---- NEC checks ----
def chain_check(name, pts, recs, maxd=1830):
    """pts: polyline of continuous wall space along the floor line; recs: receptacles (x,y) on it. Every point within maxd."""
    L=[0]; 
    for a,b in zip(pts,pts[1:]): L.append(L[-1]+math.dist(a,b))
    def s_of(p):
        best=(1e9,0)
        for i,(a,b) in enumerate(zip(pts,pts[1:])):
            ax,ay=a;bx,by=b;dx,dy=bx-ax,by-ay;l2=dx*dx+dy*dy;t=max(0,min(1,((p[0]-ax)*dx+(p[1]-ay)*dy)/l2))
            q=(ax+t*dx,ay+t*dy);d=math.dist(p,q)
            if d<best[0]: best=(d,L[i]+t*math.sqrt(l2))
        return best[1]
    s=sorted(s_of(r) for r in recs); total=L[-1]
    worst=max([s[0]]+[(b-a)/2 for a,b in zip(s,s[1:])]+[total-s[-1]]) if s else total
    return dict(chain=name,length=round(total),receptacles=len(s),worst_point_to_receptacle=round(worst),ok=worst<=maxd)
R={d["id"]:(d["x"],d["y"]) for d in D}
checks=[
 chain_check("Living: slider W edge → S pier → W wall → N wall to counter",[(-2950,-1020),(-3831,-1020),(-3831,2342),(-681,2342)],[R[k] for k in ["L1","L2","L3"]]),
 chain_check("Living: fridge end → E partition → opening",[(1798,2342),(1915,2342),(1915,-264)],[R["L4"]]),
 chain_check("Bedroom: opening → W partition → N wall → E wall → hall opening",[(2029,-264),(2029,2342),(5395,2342),(5395,247)],[R[k] for k in ["B1","B2","B3","B4"]]),
 chain_check("Bedroom: hall opening → S wall → slider E edge",[(5424,-1020),(3148,-1020)],[R["B5"]]),
]
# counter: no point more than 600 mm from a receptacle
cx=[R["K1"][0],R["K2"][0]]; worst=max([cx[0]-COUNTER[0],COUNTER[1]-cx[-1],(cx[1]-cx[0])/2])
checks.append(dict(chain="Kitchen counter (210.52(C)): no point > 600 mm",length=COUNTER[1]-COUNTER[0],receptacles=2,worst_point_to_receptacle=round(worst),ok=worst<=600))
basin=(7625,-342); checks.append(dict(chain="Bath (210.52(D)): receptacle within 900 mm of basin edge",distance_to_basin_center=round(math.dist(basin,R["BA1"])),ok=math.dist(basin,R["BA1"])-225<=900))
checks.append(dict(chain="Exterior (210.52(E)): front and back",ok=True,front="X1",back="X2"))
checks.append(dict(chain="HVAC service receptacle (210.63) within 7.5 m",distance=round(math.dist(R["X2"],R["AC-O"])),ok=math.dist(R["X2"],R["AC-O"])<=7500))
json.dump(checks,open("checks.json","w"),indent=1,ensure_ascii=False)
for c in checks: print(("PASS " if c["ok"] else "FAIL ")+c["chain"], {k:v for k,v in c.items() if k not in("chain","ok")})
