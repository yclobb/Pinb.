"""Fit a geometric flipper outline (pivot circle + tip circle + bottom corner, convex hull) to the art's body mask by IoU."""
from PIL import Image, ImageDraw
import math, itertools, json
m=Image.open("art/parts/flipper_body_mask.png").convert("L"); W,H=m.size
SC=4; ms=m.resize((W//SC,H//SC)); mp=ms.load(); w,h=ms.size
target=[(x,y) for y in range(h) for x in range(w) if mp[x,y]>127]; tset=set(target)
def hull(pts):
    pts=sorted(set(pts))
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def outline(p):
    c1,r1,c2,r2,k=(p["c1"],p["r1"],p["c2"],p["r2"],p["k"])
    pts=[(c1[0]+r1*math.cos(a/36*math.pi),c1[1]+r1*math.sin(a/36*math.pi)) for a in range(72)]
    pts+=[(c2[0]+r2*math.cos(a/36*math.pi),c2[1]+r2*math.sin(a/36*math.pi)) for a in range(72)]
    return hull(pts+[k])
def iou(p):
    im=Image.new("L",(w,h),0); ImageDraw.Draw(im).polygon([(x/SC,y/SC) for x,y in outline(p)],fill=255); ip=im.load()
    inter=sum(1 for q in target if ip[q]>127); area=sum(1 for y in range(h) for x in range(w) if ip[x,y]>127)
    return inter/(len(target)+area-inter)
import os
p={"c1":(245,345),"r1":150,"c2":(1590,460),"r2":88,"k":(480,708)}
if os.path.exists("tools/flipper_geo_params.json"):
    p={k:(tuple(v) if isinstance(v,list) else v) for k,v in json.load(open("tools/flipper_geo_params.json")).items()}
best=iou(p); print("start IoU",round(best,4))
steps={"c1":8,"r1":6,"c2":8,"r2":6,"k":10}
for rnd in range(14):
    improved=False
    for key in p:
        for d in ([(-1,0),(1,0),(0,-1),(0,1)] if isinstance(p[key],tuple) else [-1,1]):
            q=dict(p)
            q[key]=(p[key][0]+d[0]*steps[key],p[key][1]+d[1]*steps[key]) if isinstance(p[key],tuple) else p[key]+d*steps[key]
            v=iou(q)
            if v>best: best,p,improved=v,q,True
    if not improved: steps={k:max(1,v//2) for k,v in steps.items()}
    print("round",rnd,"IoU",round(best,4))
json.dump({k:list(v) if isinstance(v,tuple) else v for k,v in p.items()},open("tools/flipper_geo_params.json","w"))
print("params",p)
