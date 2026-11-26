"""Draws Lucas's sketch with the measured resizes -> art/sketch/ideal_sketch.png (regenerate, never patch)."""
from PIL import Image, ImageDraw, ImageFilter
from collections import deque
walls=Image.open("art/sketch/walls.png").getchannel("A"); pieces=Image.open("art/sketch/pieces.png").getchannel("A"); W,H=walls.size
pm=pieces.load(); seen=set(); comps=[]
for y in range(H):
    for x in range(W):
        if pm[x,y]>127 and (x,y) not in seen:
            q=deque([(x,y)]); seen.add((x,y)); pts=[]
            while q:
                a,b=q.popleft(); pts.append((a,b))
                for c in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                    if 0<=c[0]<W and 0<=c[1]<H and c not in seen and pm[c]>127: seen.add(c); q.append(c)
            comps.append(pts)
roles={"KickerTL":(340,240),"FinL":(393,335),"FinR":(495,363),"Windmill":(430,378),"KickerL":(305,494),"KickerR":(540,563),"FlipperL":(408,622),"FlipperR":(474,622)}
out=Image.new("L",(W,H),0); om=out.load()
for pts in comps:
    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
    role=min(roles,key=lambda r:(roles[r][0]-cx)**2+(roles[r][1]-cy)**2)
    if role.startswith("Kicker"): f=lambda p:(cx+(p[0]-cx)*0.75, cy+(p[1]-cy)*0.75)
    elif role=="Windmill": f=lambda p:(p[0]-cx+345, p[1]-cy+565)
    elif role.startswith("Flipper"):
        piv=min(pts) if role=="FlipperL" else max(pts)
        f=lambda p,piv=piv:(piv[0]+(p[0]-piv[0])*0.8, piv[1]+(p[1]-piv[1])*0.8)
    else: f=lambda p:p
    for p in pts:
        xi,yi=(int(round(v)) for v in f(p))
        if 0<=xi<W and 0<=yi<H: om[xi,yi]=255
out=out.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
wl=walls.copy(); d=ImageDraw.Draw(wl)
P0,P1,P2=(492,124),(552,146),(556,196)   # curved fill in the tunnel-exit corner
d.line([((1-t)**2*P0[0]+2*(1-t)*t*P1[0]+t*t*P2[0],(1-t)**2*P0[1]+2*(1-t)*t*P1[1]+t*t*P2[1]) for t in [i/30 for i in range(31)]],fill=255,width=6,joint="curve")
crop=(200,40,640,660); s=2
img=Image.new("RGB",(W,H),"white"); img.paste((20,20,30),mask=wl); img.paste((240,100,20),mask=out)
img=img.crop(crop).resize(((crop[2]-crop[0])*s,(crop[3]-crop[1])*s),Image.LANCZOS)
d=ImageDraw.Draw(img); R=8.0*s    # ball = 16 sketch px across (17 game px)
bx,by=(610-200)*s,(455-40)*s; d.ellipse((bx-R,by-R,bx+R,by+R),fill=(170,170,180),outline=(60,60,70),width=2)
for (x,y),t in [((520,20),"curved exit: launch can't bounce back"),((10,560),"secret entry widened (1.4 balls)"),((10,1000),"windmill moved above the pit"),((560,1215),"drop 1.3+ balls"),((800,860),"ball\n(scale)")]:
    d.multiline_text((x,y),t,fill=(200,20,30))
img.save("art/sketch/ideal_sketch.png"); print(img.size)
