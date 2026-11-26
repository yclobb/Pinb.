"""Lucas's Canva sketch -> art/sketch/walls.png (black/purple lines) + pieces.png (orange/red shapes).
Notes are skipped: marker red (231,25,31), filled arrows, text, the drawn balls, anything outside the table area.
Usage: python tools/sketch_extract.py "<sketch.png>" """
import sys
from PIL import Image, ImageFilter, ImageChops
from collections import deque
im=Image.open(sys.argv[1]).convert("RGB"); W,H=im.size; px=im.load()
RX0,RX1,RY0,RY1=215,615,50,650
def mask(test):
    m=Image.new("L",(W,H),0); mp=m.load()
    for y in range(RY0,RY1):
        for x in range(RX0,RX1):
            if test(px[x,y]): mp[x,y]=255
    return m
ink=mask(lambda p: (max(p)<100 and max(p)-min(p)<45) or (p[2]>140 and p[0]>70 and p[1]<100 and p[0]<180))
ink=ImageChops.subtract(ink,ink.filter(ImageFilter.MinFilter(11)).filter(ImageFilter.MaxFilter(19)))   # strip filled arrows
warm=mask(lambda p: p[0]>190 and p[2]<14 and p[0]-p[2]>150)   # pieces; marker red has blue=31
def comps(m):
    mp=m.load(); seen=set(); out=[]
    for y in range(RY0,RY1):
        for x in range(RX0,RX1):
            if mp[x,y]<128 or (x,y) in seen: continue
            q=deque([(x,y)]); seen.add((x,y)); pts=[]
            while q:
                a,b=q.popleft(); pts.append((a,b))
                for c in ((a+1,b),(a-1,b),(a,b+1),(a,b-1),(a+1,b+1),(a-1,b-1),(a+1,b-1),(a-1,b+1)):
                    if RX0<=c[0]<RX1 and RY0<=c[1]<RY1 and c not in seen and mp[c]>=128: seen.add(c); q.append(c)
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            out.append(dict(pts=pts,bbox=(min(xs),min(ys),max(xs)-min(xs)+1,max(ys)-min(ys)+1),n=len(pts)))
    return out
walls=[c for c in comps(ink) if max(c["bbox"][2:])>=28]
pieces=[c for c in comps(warm) if c["n"]>120 and min(c["bbox"][2:])>6 and not (abs(c["bbox"][2]-c["bbox"][3])<9 and 26<c["bbox"][2]<48)]
print("walls",len(walls),"pieces",len(pieces))
for name,cs,g in (("walls",walls,5),("pieces",pieces,3)):
    m=Image.new("L",(W,H),0); mp=m.load()
    for c in cs:
        for p in c["pts"]: mp[p]=255
    m=m.filter(ImageFilter.MaxFilter(g))
    if name=="pieces": m=m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    out=Image.new("RGBA",(W,H),(255,255,255,0)); out.putalpha(m); out.save(f"art/sketch/{name}.png")
