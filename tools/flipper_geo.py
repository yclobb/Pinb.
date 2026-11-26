"""Geometric flipper (shapes only) fitted to Lucas's flipper art -> art/parts/flipper.png (active) + flipper_disabled.png.
Same canvas + pin (245,331) as before so flipper.tscn keeps working."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, json
W,H=1774,887
P=json.load(open("tools/flipper_geo_params.json"))
def hull(pts):
    pts=sorted(set(pts)); cr=lambda o,a,b:(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]); lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
circ=lambda c,r,n=180:[(c[0]+r*math.cos(2*math.pi*i/n),c[1]+r*math.sin(2*math.pi*i/n)) for i in range(n)]
SS=2   # supersample for smooth edges
def poly_mask(pts):
    m=Image.new("L",(W*SS,H*SS),0); ImageDraw.Draw(m).polygon([(x*SS,y*SS) for x,y in pts],fill=255); return m.resize((W,H),Image.LANCZOS)
def erode(m,r):
    for _ in range(max(1,r//4)): m=m.filter(ImageFilter.MinFilter(9))
    return m
S=poly_mask(hull(circ(P["c1"],P["r1"])+circ(P["c2"],P["r2"])+[tuple(P["k"])]))            # whole body (top + side)
D=52                                                                                      # side band thickness
T=ImageChops.multiply(S,ImageChops.offset(S,0,-D))                                         # top surface
panel=erode(T,22); inner_line=ImageChops.subtract(erode(T,17),erode(T,21))
edge=ImageChops.subtract(T,erode(T,4))
def ring(c,r,w):
    m=Image.new("L",(W*SS,H*SS),0); ImageDraw.Draw(m).ellipse(((c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS),outline=255,width=int(w*SS)); return m.resize((W,H),Image.LANCZOS)
def disc(c,r):
    m=Image.new("L",(W*SS,H*SS),0); ImageDraw.Draw(m).ellipse(((c[0]-r)*SS,(c[1]-r)*SS,(c[0]+r)*SS,(c[1]+r)*SS),fill=255); return m.resize((W,H),Image.LANCZOS)
PIN=(245,331); DEC=(735,418)
# stripes near the pivot and the swoosh near the tip (clipped to the panel)
st=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(st)
for i in range(3): d.line([((390+i*34)*SS,250*SS),((330+i*34)*SS,470*SS)],fill=255,width=14*SS)
stripes=ImageChops.multiply(st.resize((W,H),Image.LANCZOS),panel)
q=lambda a,b,c,t:((1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*c[1])
curveA=[q((1000,600),(1290,410),(1660,390),t/40) for t in range(41)]
sw=poly_mask(curveA+[(1700,700),(1040,700)]); swoosh=ImageChops.multiply(sw,panel)
swl=Image.new("L",(W*SS,H*SS),0); ImageDraw.Draw(swl).line([(x*SS,(y-26)*SS) for x,y in [q((940,620),(1250,430),(1640,415),t/40) for t in range(41)]],fill=255,width=10*SS)
swoosh_line=ImageChops.multiply(swl.resize((W,H),Image.LANCZOS),panel)
def render(c,glow_rgb,glow_strength,glow_blur):
    out=Image.new("RGBA",(W,H),(0,0,0,0))
    g=S.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(glow_blur)).point(lambda v:int(v*glow_strength))
    out.paste(glow_rgb+(255,),mask=g)
    lay=Image.new("RGBA",(W,H),(0,0,0,0))
    for col,m in [(c["side"],S),(c["side_edge"],ImageChops.subtract(S,erode(S,4))),(c["rim"],T),(c["edge"],edge),(c["panel"],panel),
                  (c["stripe"],stripes),(c["swoosh"],swoosh),(c["line"],swoosh_line),(c["line"],inner_line),
                  (c["outline"],ring(DEC,98,34)),(c["rim"],ring(DEC,92,22)),(c["line"],ring(DEC,87,4)),
                  (c["outline"],disc(PIN,96)),(c["rim"],ring(PIN,80,20)),(c["line"],ring(PIN,88,4)),(c["cap"],disc(PIN,58)),(c["cap_hi"],ring(PIN,48,6))]:
        lay.paste(col+(255,),mask=m)
    return Image.alpha_composite(out,lay)
active=dict(side=(40,56,60),side_edge=(150,240,240),rim=(123,237,190),edge=(220,255,250),panel=(24,52,50),stripe=(44,72,70),swoosh=(120,226,198),
            line=(230,255,250),outline=(16,34,34),cap=(62,72,74),cap_hi=(110,124,126))
disabled=dict(side=(52,45,44),side_edge=(70,62,60),rim=(111,148,141),edge=(200,214,206),panel=(26,32,31),stripe=(40,48,47),swoosh=(96,118,120),
              line=(205,222,214),outline=(18,24,23),cap=(72,72,70),cap_hi=(120,120,116))
render(active,(90,235,255),0.55,22).save("art/parts/flipper.png")
render(disabled,(235,228,205),0.35,6).save("art/parts/flipper_disabled.png")
S.save("art/parts/flipper_geo_mask.png"); print("ok")
