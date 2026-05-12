"""Generate Ремсити36 case-card cover (electronics & appliance repair theme) as compressed WebP."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

W, H = 900, 540
out = Image.new("RGB", (W, H), (8, 14, 28))
draw = ImageDraw.Draw(out, "RGBA")


# ── Background: dark navy → electric blue diagonal gradient ──
def vgrad(img, top, bottom):
    for y in range(img.height):
        t = y / max(1, img.height - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        ImageDraw.Draw(img).line([(0, y), (img.width, y)], fill=(r, g, b))


vgrad(out, (10, 18, 38), (15, 60, 110))

# ── Diagonal radial wash (electric blue) ──
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, alpha in [(420, 60), (320, 90), (220, 110), (140, 130), (80, 150)]:
    gd.ellipse([W * 0.78 - r, H * 0.45 - r, W * 0.78 + r, H * 0.45 + r],
               fill=(14, 165, 233, alpha))
glow = glow.filter(ImageFilter.GaussianBlur(40))
out = Image.alpha_composite(out.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(out, "RGBA")

# Orange accent glow (repair-tool warm)
warm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(warm)
for r, alpha in [(280, 55), (180, 80), (110, 110)]:
    wd.ellipse([W * 0.18 - r, H * 0.85 - r, W * 0.18 + r, H * 0.85 + r],
               fill=(245, 158, 11, alpha))
warm = warm.filter(ImageFilter.GaussianBlur(35))
out = Image.alpha_composite(out.convert("RGBA"), warm).convert("RGB")
draw = ImageDraw.Draw(out, "RGBA")

# ── Subtle circuit grid ──
for x in range(0, W, 60):
    draw.line([(x, 80), (x, H)], fill=(255, 255, 255, 8), width=1)
for y in range(80, H, 60):
    draw.line([(0, y), (W, y)], fill=(255, 255, 255, 8), width=1)

# Circuit accents (small + nodes)
for (x, y) in [(120, 200), (300, 380), (540, 160), (720, 320), (640, 460), (180, 460)]:
    draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(34, 211, 238, 180))
    draw.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(34, 211, 238, 90), width=1)

# Connecting circuit traces
draw.line([(120, 200), (300, 200), (300, 380)], fill=(34, 211, 238, 70), width=2)
draw.line([(540, 160), (720, 160), (720, 320)], fill=(34, 211, 238, 70), width=2)
draw.line([(640, 460), (180, 460)], fill=(34, 211, 238, 50), width=2)

# ── Top "browser bar" ──
bar_h = 56
draw.rectangle([0, 0, W, bar_h], fill=(0, 0, 0, 130))
draw.line([(0, bar_h), (W, bar_h)], fill=(255, 255, 255, 25), width=1)

# Traffic lights
for i, color in enumerate([(255, 95, 87), (255, 189, 46), (40, 201, 63)]):
    cx = 26 + i * 26
    draw.ellipse([cx - 8, bar_h // 2 - 8, cx + 8, bar_h // 2 + 8], fill=color)

# URL pill
url_x1, url_x2 = 130, 410
draw.rounded_rectangle([url_x1, 14, url_x2, 42], radius=8, fill=(255, 255, 255, 35))


# ── Fonts ──
def load_font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


font_url = load_font(["consola.ttf", "consolab.ttf", "cour.ttf"], 16)
font_brand = load_font(["seguibl.ttf", "segoeuib.ttf", "ariblk.ttf", "arialbd.ttf"], 78)
font_sub = load_font(["segoeuib.ttf", "arialbd.ttf"], 26)
font_logo = load_font(["seguibl.ttf", "ariblk.ttf", "arialbd.ttf"], 44)
font_chip = load_font(["segoeuib.ttf", "arialbd.ttf"], 18)
font_lock = load_font(["seguisym.ttf", "seguiemj.ttf", "arial.ttf"], 14)

# URL text
draw.text((url_x1 + 14, 17), "🔒  ремсити36.рф", font=font_url, fill=(255, 255, 255, 230))

# Status chip on right
chip = "● ONLINE"
chip_bbox = draw.textbbox((0, 0), chip, font=font_chip)
chip_w = chip_bbox[2] - chip_bbox[0]
draw.rounded_rectangle([W - 36 - chip_w - 18, 14, W - 36, 42], radius=8,
                       fill=(40, 201, 63, 60), outline=(40, 201, 63, 180), width=1)
draw.text((W - 36 - chip_w - 4, 17), chip, font=font_chip, fill=(140, 240, 160, 255))

# ── LOGO TILE (left) ──
logo_x, logo_y, logo_s = 70, 230, 140
# Outer glow
glow_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gld = ImageDraw.Draw(glow_l)
gld.rounded_rectangle([logo_x - 16, logo_y - 16, logo_x + logo_s + 16, logo_y + logo_s + 16],
                      radius=32, fill=(245, 158, 11, 130))
glow_l = glow_l.filter(ImageFilter.GaussianBlur(22))
out = Image.alpha_composite(out.convert("RGBA"), glow_l).convert("RGB")
draw = ImageDraw.Draw(out, "RGBA")

# Logo body — gradient orange
for i in range(logo_s):
    t = i / logo_s
    r = int(255 + (217 - 255) * t)
    g = int(140 + (90 - 140) * t)
    b = int(0 + (10 - 0) * t)
    draw.line([(logo_x, logo_y + i), (logo_x + logo_s, logo_y + i)], fill=(r, g, b, 255))

# Mask logo to rounded rectangle by drawing a rounded mask, then re-paste
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([logo_x, logo_y, logo_x + logo_s, logo_y + logo_s], radius=22, fill=255)
# Background snapshot under logo, then use mask to paint
base = out.copy()
overlay = Image.new("RGB", (W, H), 0)
od = ImageDraw.Draw(overlay)
for i in range(logo_s):
    t = i / logo_s
    r = int(255 + (200 - 255) * t)
    g = int(140 + (70 - 140) * t)
    b = int(20 + (10 - 20) * t)
    od.line([(0, logo_y + i), (W, logo_y + i)], fill=(r, g, b))
out.paste(overlay, mask=mask)
draw = ImageDraw.Draw(out, "RGBA")

# Inner highlight on logo (glossy)
draw.rounded_rectangle([logo_x + 6, logo_y + 6, logo_x + logo_s - 6, logo_y + logo_s // 2],
                       radius=18, fill=(255, 255, 255, 38))

# Logo letters "RC36"
text_rc = "RC"
text_36 = "36"
b1 = draw.textbbox((0, 0), text_rc, font=font_logo)
b2 = draw.textbbox((0, 0), text_36, font=font_logo)
w1 = b1[2] - b1[0]; h1 = b1[3] - b1[1]
w2 = b2[2] - b2[0]; h2 = b2[3] - b2[1]
draw.text((logo_x + (logo_s - w1) // 2, logo_y + 22), text_rc, font=font_logo, fill=(255, 255, 255, 255))
draw.text((logo_x + (logo_s - w2) // 2, logo_y + logo_s // 2 + 8), text_36, font=font_logo, fill=(255, 255, 255, 255))

# ── BRAND TEXT ──
text_x = logo_x + logo_s + 40
draw.text((text_x, 200), "Ремсити", font=font_brand, fill=(255, 255, 255, 255))
# Stylize "36" with cyan
brand_w = draw.textbbox((0, 0), "Ремсити", font=font_brand)[2]
draw.text((text_x + brand_w + 8, 200), "36", font=font_brand, fill=(34, 211, 238, 255))

# Subtitle
draw.text((text_x, 308), "Ремонт бытовой техники", font=font_sub, fill=(220, 235, 255, 240))
draw.text((text_x, 342), "и электроники", font=font_sub, fill=(220, 235, 255, 240))

# Service chips
chips = [("Холодильники", (14, 165, 233)), ("Стиралки", (245, 158, 11)),
         ("ТВ / Микро", (139, 92, 246)), ("Электроника", (34, 211, 238))]
cx = text_x
cy = 400
for label, color in chips:
    bb = draw.textbbox((0, 0), label, font=font_chip)
    pw = bb[2] - bb[0] + 24
    ph = 32
    draw.rounded_rectangle([cx, cy, cx + pw, cy + ph], radius=16,
                           fill=(color[0], color[1], color[2], 50),
                           outline=(color[0], color[1], color[2], 180), width=1)
    draw.text((cx + 12, cy + 5), label, font=font_chip,
              fill=(255, 255, 255, 235))
    cx += pw + 10

# Decorative "tools" lightning bolt in corner
import math as _m
def bolt(d, x, y, scale=1.0, color=(34, 211, 238, 200)):
    pts = [(0, -28), (-10, -2), (-2, -2), (-12, 22), (8, -2), (0, -2), (10, -28)]
    pts = [(x + p[0] * scale, y + p[1] * scale) for p in pts]
    d.polygon(pts, fill=color)

bolt(draw, W - 110, 220, scale=2.0, color=(34, 211, 238, 220))
bolt(draw, W - 110, 220, scale=2.0, color=(255, 255, 255, 60))

# Soft vignette
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], fill=(0, 0, 0, 0))
vd.rectangle([0, 0, W, 80], fill=(0, 0, 0, 90))
vd.rectangle([0, H - 60, W, H], fill=(0, 0, 0, 70))
out = Image.alpha_composite(out.convert("RGBA"), vig).convert("RGB")

out_path = os.path.join(os.path.dirname(__file__), "remcity36_cover.webp")
out.save(out_path, "WEBP", quality=82, method=6)
print(f"Saved: {out_path}")
print(f"Size: {os.path.getsize(out_path)} bytes  ({os.path.getsize(out_path)/1024:.1f} KB)")
