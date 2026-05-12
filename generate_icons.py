"""Generate favicons + apple-touch-icon + og-image for LAB301."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BASE = os.path.dirname(__file__)

# Brand colors
INDIGO = (99, 102, 241)
PURPLE = (168, 85, 247)
CYAN = (6, 182, 212)
DARK = (8, 8, 8)


def load_font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon(size, out_path, *, text="L3", rounded=True):
    """Square icon with gradient + 'L3' wordmark."""
    # Render at 4x for crisp downscale
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Rounded-rect background with diagonal gradient
    radius = int(s * 0.22) if rounded else 0
    # Diagonal gradient: indigo -> purple -> cyan
    grad = Image.new("RGBA", (s, s))
    gd = ImageDraw.Draw(grad)
    for y in range(s):
        for x_band in range(1):
            t = y / max(1, s - 1)
            # blend indigo→purple in top half, purple→cyan in bottom half
            if t < 0.5:
                k = t / 0.5
                r = int(INDIGO[0] + (PURPLE[0] - INDIGO[0]) * k)
                g = int(INDIGO[1] + (PURPLE[1] - INDIGO[1]) * k)
                b = int(INDIGO[2] + (PURPLE[2] - INDIGO[2]) * k)
            else:
                k = (t - 0.5) / 0.5
                r = int(PURPLE[0] + (CYAN[0] - PURPLE[0]) * k)
                g = int(PURPLE[1] + (CYAN[1] - PURPLE[1]) * k)
                b = int(PURPLE[2] + (CYAN[2] - PURPLE[2]) * k)
            gd.line([(0, y), (s, y)], fill=(r, g, b, 255))

    # Apply rounded mask
    mask = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, s, s], radius=radius, fill=255)
    img.paste(grad, (0, 0), mask)

    # Inner glow / highlight on top
    hl = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([int(s * 0.06), int(s * 0.06),
                          int(s * 0.94), int(s * 0.45)],
                         radius=int(radius * 0.7),
                         fill=(255, 255, 255, 40))
    hl = hl.filter(ImageFilter.GaussianBlur(s * 0.02))
    img.alpha_composite(hl)

    # Diagonal sheen
    sheen = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sheen)
    sd.polygon([(0, 0), (int(s * 0.6), 0), (0, int(s * 0.6))],
               fill=(255, 255, 255, 30))
    img.alpha_composite(sheen)

    # Text: bold sans
    font = load_font(["seguibl.ttf", "ariblk.ttf", "arialbd.ttf",
                      "segoeuib.ttf"], int(s * 0.55))
    d2 = ImageDraw.Draw(img)
    bbox = d2.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (s - tw) // 2 - bbox[0]
    ty = (s - th) // 2 - bbox[1] - int(s * 0.02)
    # subtle shadow
    d2.text((tx + int(s * 0.01), ty + int(s * 0.015)), text,
            font=font, fill=(0, 0, 0, 90))
    d2.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

    # Downsample
    final = img.resize((size, size), Image.LANCZOS)
    final.save(out_path, "PNG", optimize=True)
    print(f"  saved {out_path}  ({os.path.getsize(out_path)} bytes)")


def make_favicon_ico(out_path):
    """Multi-size ICO containing 16, 32, 48."""
    sizes = [16, 32, 48]
    imgs = []
    for sz in sizes:
        tmp = os.path.join(BASE, f"_tmp_{sz}.png")
        make_icon(sz, tmp)
        imgs.append(Image.open(tmp).convert("RGBA"))
    imgs[0].save(out_path, format="ICO",
                 sizes=[(s, s) for s in sizes],
                 append_images=imgs[1:])
    for sz in sizes:
        os.remove(os.path.join(BASE, f"_tmp_{sz}.png"))
    print(f"  saved {out_path}  ({os.path.getsize(out_path)} bytes)")


def make_og_image(out_path, w=1200, h=630):
    """Open Graph social share image — 1200×630."""
    img = Image.new("RGB", (w, h), DARK)
    d = ImageDraw.Draw(img, "RGBA")

    # Vertical gradient dark -> a touch lighter
    for y in range(h):
        t = y / (h - 1)
        r = int(8 + 12 * t)
        g = int(8 + 10 * t)
        b = int(14 + 30 * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))

    # Glow orbs (purple + cyan)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(420, 70), (320, 100), (220, 120), (140, 140)]:
        gd.ellipse([w * 0.78 - r, h * 0.30 - r, w * 0.78 + r, h * 0.30 + r],
                   fill=(168, 85, 247, a))
    for r, a in [(360, 70), (260, 95), (170, 120)]:
        gd.ellipse([w * 0.18 - r, h * 0.85 - r, w * 0.18 + r, h * 0.85 + r],
                   fill=(6, 182, 212, a))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # Subtle grid
    for x in range(0, w, 60):
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, h, 60):
        d.line([(0, y), (w, y)], fill=(255, 255, 255, 10), width=1)

    # Logo tile (left)
    tile_size = 140
    tx, ty = 90, 100
    tile = Image.new("RGBA", (tile_size * 4, tile_size * 4), (0, 0, 0, 0))
    # reuse make_icon-style render inline by calling helper
    tmp_logo = os.path.join(BASE, "_tmp_oglogo.png")
    make_icon(tile_size, tmp_logo, text="L3")
    logo_img = Image.open(tmp_logo).convert("RGBA")
    # outer soft glow behind logo
    g2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g2d = ImageDraw.Draw(g2)
    g2d.rounded_rectangle([tx - 20, ty - 20, tx + tile_size + 20,
                           ty + tile_size + 20], radius=42,
                          fill=(168, 85, 247, 110))
    g2 = g2.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img.convert("RGBA"), g2).convert("RGB")
    img.paste(logo_img, (tx, ty), logo_img)
    os.remove(tmp_logo)
    d = ImageDraw.Draw(img, "RGBA")

    # Brand text "LAB301"
    f_brand = load_font(["seguibl.ttf", "ariblk.ttf", "arialbd.ttf"], 120)
    f_title = load_font(["seguibl.ttf", "ariblk.ttf", "arialbd.ttf"], 76)
    f_sub = load_font(["segoeuib.ttf", "arialbd.ttf"], 32)
    f_chip = load_font(["segoeuib.ttf", "arialbd.ttf"], 22)

    text_x = tx + tile_size + 36
    d.text((text_x, ty + 14), "LAB301", font=f_brand, fill=(255, 255, 255, 255))

    # Big headline (two lines)
    d.text((90, 310), "Технологии роста", font=f_title, fill=(255, 255, 255, 255))
    # gradient-ish second line: split letters between purple and cyan
    line2 = "для бизнеса"
    d.text((90, 400), line2, font=f_title, fill=(192, 132, 252, 255))

    # Subtitle
    d.text((90, 500), "Сайты · AI-автоматизация · Digital-продвижение",
           font=f_sub, fill=(200, 210, 230, 235))

    # URL chip bottom-right
    url = "lab301.ru"
    bb = d.textbbox((0, 0), url, font=f_chip)
    cw = bb[2] - bb[0] + 32
    ch = 42
    cx2 = w - 90
    cy2 = h - 80
    d.rounded_rectangle([cx2 - cw, cy2 - ch, cx2, cy2], radius=21,
                        fill=(255, 255, 255, 22),
                        outline=(255, 255, 255, 90), width=1)
    d.text((cx2 - cw + 16, cy2 - ch + 8), url, font=f_chip,
           fill=(255, 255, 255, 240))

    # Vignette top + bottom
    vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, w, 60], fill=(0, 0, 0, 90))
    vd.rectangle([0, h - 60, w, h], fill=(0, 0, 0, 70))
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")

    img.save(out_path, "WEBP", quality=86, method=6)
    # also save jpg fallback
    jpg_path = out_path.replace(".webp", ".jpg")
    img.save(jpg_path, "JPEG", quality=88, optimize=True)
    print(f"  saved {out_path}  ({os.path.getsize(out_path)} bytes)")
    print(f"  saved {jpg_path}  ({os.path.getsize(jpg_path)} bytes)")


if __name__ == "__main__":
    print("Generating favicons + og-image …")
    make_icon(16, os.path.join(BASE, "favicon-16x16.png"))
    make_icon(32, os.path.join(BASE, "favicon-32x32.png"))
    make_icon(180, os.path.join(BASE, "apple-touch-icon.png"))
    make_favicon_ico(os.path.join(BASE, "favicon.ico"))
    make_og_image(os.path.join(BASE, "og-image.webp"))
    print("Done.")
