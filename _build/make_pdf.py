"""Builds a simple placeholder catalogue PDF (replace downloads/inkwell-catalogue.pdf with your real one)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from build import CATS, CONFIG as C, ROOT
W, H = 1240, 1754
INK, PAPER, HL = (15, 27, 61), (251, 247, 239), (255, 216, 74)
F = "C:/Windows/Fonts/"
def font(n, s): return ImageFont.truetype(F + n, s)
head, headb, body, bodyb = "georgiab.ttf", "georgiab.ttf", "segoeui.ttf", "segoeuib.ttf"
def wrap(d, text, f, w):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if d.textlength(t, font=f) <= w: line = t
        else: out.append(line); line = word
    return out + [line]
pages = []
# cover
im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
d.rectangle([80, 80, W-80, H-80], outline=PAPER, width=3)
d.rectangle([120, 1180, 420, 1200], fill=HL)
d.text((120, 300), "Catalogue", font=font(head, 120), fill=HL)
d.text((120, 440), "2026", font=font(head, 120), fill=PAPER)
d.text((120, 1230), C["brand"], font=font(head, 72), fill=PAPER)
d.text((120, 1330), "Office & school stationery", font=font(body, 38), fill=PAPER)
d.text((120, 1560), C["email"] + "   |   " + C["phone"], font=font(body, 30), fill=(200, 205, 220))
pages.append(im)
for c in CATS:
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=INK)
    d.text((80, 90), c["name"], font=font(head, 86), fill=PAPER)
    d.rectangle([80, 230, 380, 246], fill=HL)
    photo = Image.open(os.path.join(ROOT, "assets/img/%s.jpg" % c["img"])).convert("RGB")
    ph = photo.copy(); ph.thumbnail((1080, 1080)); pw, phh = ph.size
    ph = ph.crop((0, 0, pw, min(phh, 520)))
    im.paste(ph, (80, 350)); d.rectangle([80, 350, 80+ph.size[0], 350+ph.size[1]], outline=INK, width=4)
    y = 350 + ph.size[1] + 50
    for ln in wrap(d, c["intro"], font(body, 30), 1080):
        d.text((80, y), ln, font=font(body, 30), fill=INK); y += 44
    y += 30
    for s in c["subs"]:
        d.ellipse([84, y+12, 104, y+32], fill=HL, outline=INK, width=3)
        d.text((124, y), s["name"], font=font(bodyb, 32), fill=INK)
        lines = wrap(d, s["desc"], font(body, 26), 1000)
        y += 44
        for ln in lines:
            d.text((124, y), ln, font=font(body, 26), fill=(85, 96, 125)); y += 36
        y += 18
    d.text((80, H-70), C["brand"] + "  |  " + C["email"] + "  |  " + C["phone"], font=font(body, 24), fill=(85, 96, 125))
    pages.append(im)
os.makedirs(os.path.join(ROOT, "downloads"), exist_ok=True)
out = os.path.join(ROOT, "downloads", "inkwell-catalogue.pdf")
pages[0].save(out, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print(out, round(os.path.getsize(out)/1024), "KB", len(pages), "pages")
