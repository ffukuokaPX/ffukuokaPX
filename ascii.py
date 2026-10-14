import numpy as np
from PIL import Image, ImageFilter

RAMP = " .'`,:;~-+=ilt1jfLJCYXUOQ0ZmwqpdbkhaW#M&8%B@"
EDGES = "-/|\\"  # contour char by edge angle: 0, 45, 90, 135 degrees

def ascii_art(path, box, cols, edge=0.5, gamma=1.6):
    img = Image.open(path).convert("RGB").crop(box)
    w, h = img.size
    rows = int(cols * h / w * 0.5)
    a = np.asarray(img, dtype=float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = np.where(g > 2 * r + 10, 0, 0.299 * r + 0.587 * g + 0.114 * b)  # drop the green matrix rain
    mask = Image.fromarray(((lum > 15) * 255).astype(np.uint8))
    mask = mask.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.MaxFilter(15))  # erase leftover glyphs, keep the face
    lum = Image.fromarray((lum * (np.asarray(mask) > 0)).astype(np.uint8))
    lum = lum.filter(ImageFilter.UnsharpMask(radius=6, percent=150, threshold=0)).resize((cols * 4, rows * 8), Image.LANCZOS)
    L = np.asarray(lum, dtype=float)
    L = np.clip(L / np.percentile(L, 98), 0, 1)
    blur = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), dtype=float) / 255
    gy, gx = np.gradient(blur)
    cell = lambda x: x.reshape(rows, 8, cols, 4).mean(axis=(1, 3))
    bright, gxc, gyc, mag = cell(L), cell(gx), cell(gy), cell(np.hypot(gx, gy))
    mag /= mag.max()
    out = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            if mag[y, x] > edge:
                ang = (np.degrees(np.arctan2(-gyc[y, x], gxc[y, x])) + 90) % 180  # edge runs perpendicular to gradient
                line += EDGES[int((ang + 22.5) // 45) % 4]
            else:
                line += RAMP[min(len(RAMP) - 1, int(bright[y, x] ** gamma * (len(RAMP) - 1)))]
        out.append(line.rstrip())
    return out
