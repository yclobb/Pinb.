"""Lucas's flipper art -> art/parts/flipper.png: text removed, big ring decal, dark halo replaced by cyan glow.
Usage: python tools/flipper_art.py "<flipper.png>" """
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
im=Image.open(sys.argv[1]).convert("RGBA"); W,H=im.size; A=im.getchannel("A")
body=A.point(lambda v:255 if v>=235 else 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
# text + its glow = pixels clearly brighter than the dark panel, inside the text area (below the top border, left of the swoosh)
X0,X1,Y0,Y1=440,1046,312,536
px=im.load(); lum=lambda p:0.3*p[0]+0.59*p[1]+0.11*p[2]
mask=Image.new("L",(W,H),0); mp=mask.load()
top=lambda x: 318 if x<930 else 318+(x-930)*0.25        # stay below the panel's sloping top border
for y in range(Y0,Y1):
    for x in range(X0,X1):
        if y>=top(x) and lum(px[x,y])>48: mp[x,y]=255
mask=mask.filter(ImageFilter.MaxFilter(7)); mp=mask.load()
# fill each masked run from the clean pixels on both sides of it (row interpolation)
for y in range(Y0,Y1):
    x=X0
    while x<X1:
        if mp[x,y]:
            s=x
            while x<X1 and mp[x,y]: x+=1
            L=px[s-1,y]; R=px[min(x,W-1),y]; n=x-s+1
            for i in range(s,x):
                t=(i-s+1)/n; px[i,y]=tuple(int(L[c]*(1-t)+R[c]*t) for c in range(4))
        x+=1
# soften the filled rows a little so no streaks remain
filled=im.filter(ImageFilter.GaussianBlur(14)); im=Image.composite(filled,im,mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
# big ring decal (the "." from the logo): glow, dark outline, mint ring, white inner line
cx,cy,R=735,418,92
rg=Image.new("L",(W,H),0); ImageDraw.Draw(rg).ellipse((cx-R-14,cy-R-14,cx+R+14,cy+R+14),outline=255,width=34)
im=Image.composite(Image.new("RGBA",(W,H),(110,230,200,255)),im,rg.filter(ImageFilter.GaussianBlur(14)).point(lambda v:int(v*0.45)))
d=ImageDraw.Draw(im)
d.ellipse((cx-R-6,cy-R-6,cx+R+6,cy+R+6),outline=(16,34,34,255),width=34)
d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=(123,237,190,255),width=22)
d.ellipse((cx-R+5,cy-R+5,cx+R-5,cy+R-5),outline=(235,255,250,255),width=4)
# consistent subtle cyan glow from the body outline (replaces the dark halo)
glow=body.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(22)).point(lambda v:int(v*0.55))
out=Image.new("RGBA",(W,H),(0,0,0,0)); out.paste((90,235,255,255),mask=glow)
b=im.copy(); b.putalpha(ImageChops.multiply(body,A)); out=Image.alpha_composite(out,b)
out.save("art/parts/flipper.png"); body.save("art/parts/flipper_body_mask.png"); print("ok", out.size)
