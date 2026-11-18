#!/usr/bin/env python3
"""Render the news-image-20261118 front page.

Draws a newspaper front page for Wednesday 18 November 2026 with PIL, using
only flat vector-style shapes and text. Every story was checked against
reporting published on 18 November 2026. Deterministic: same input gives the
same PNG bytes.

Usage: python3 render.py A|B|C   (writes candidates/<variant>.png)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (22, 21, 19)
RED = (158, 27, 27)
TEAL = (14, 110, 107)
NAVY = (20, 38, 74)
BLUE = (29, 78, 216)
PURPLE = (109, 40, 217)
GREEN = (21, 128, 61)
ORANGE = (194, 65, 12)
GOLD = (166, 124, 0)
OCEAN = (207, 227, 238)
LAND = (232, 221, 192)
LAND_LINE = (138, 127, 92)
GREY = (90, 86, 78)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centered(draw, x, y, s, fnt, fill=INK):
    draw.text((x, y), s, font=fnt, fill=fill, anchor="ma")


def badge(draw, cx, cy, r, n, fill=RED):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=PAPER, width=2)
    f = font(F_SANS_BOLD, int(r * 1.05))
    draw.text((cx, cy), str(n), font=f, fill=(255, 255, 255), anchor="mm")


def rule(draw, x0, y, x1, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


# ---------------------------------------------------------------- stories
LEADS = [
    {"n": 1, "region": "EUROPE", "color": PURPLE,
     "headline": "Ukraine hits Crimea bridge again; a span falls",
     "deck": "A second day of strikes drops a road span into the Kerch Strait; "
             "Russia pounds Kyiv's bridges in reply.",
     "art": "bridge"},
    {"n": 2, "region": "MIDDLE EAST", "color": RED,
     "headline": "US and Iran trade fire over Bahrain",
     "deck": "Iranian drones target a US radar at Sheikh Isa; US jets hit a "
             "missile site on Qeshm Island.",
     "art": "fire"},
    {"n": 3, "region": "ASIA", "color": TEAL,
     "headline": "Trump in Manila for first Quad talks in two years",
     "deck": "He meets Modi, Takaichi and Albanese at the ASEAN sidelines, then "
             "heads to Shenzhen for APEC.",
     "art": "summit"},
]

CARDS = [
    {"n": 4, "region": "MARKETS", "color": TEAL,
     "headline": "Nvidia revenue more than doubles to $115.8bn",
     "deck": "Up 103% in its first results since Huang resigned; the board rules "
             "out his return, and the SEC opens a probe.",
     "icon": "chip"},
    {"n": 5, "region": "WEATHER", "color": BLUE,
     "headline": "Cyclone Akvan bears down on India's east coast",
     "deck": "The severe cyclonic storm crosses Andhra Pradesh on Friday, with "
             "winds above 120 km/h and heavy rain from today.",
     "icon": "storm"},
    {"n": 6, "region": "TRADE", "color": GREEN,
     "headline": "Canada and China extend trade deals as Xi meets Carney",
     "deck": "The two leaders agree to deepen cooperation on the APEC sidelines "
             "in Shenzhen, easing a long chill.",
     "icon": "deal"},
    {"n": 7, "region": "EUROPE", "color": PURPLE,
     "headline": "Britain sanctions Israeli settlement firms",
     "deck": "London blacklists firms linked to West Bank settlements, saying the "
             "move protects the two-state solution.",
     "icon": "ban"},
    {"n": 8, "region": "ENERGY", "color": ORANGE,
     "headline": "India condemns attack on LPG tanker in Hormuz strait",
     "deck": "The Panama-flagged MT TARA GAS was hit on Tuesday; 21 of its 24 "
             "Indian crew were evacuated ashore at Khasab.",
     "icon": "tanker"},
    {"n": 9, "region": "TECH", "color": NAVY,
     "headline": "Baidu chief warns of an AI 'bubble' ahead of APEC",
     "deck": "The head of China's biggest search firm says AI valuations have run "
             "ahead of real returns.",
     "icon": "robot"},
    {"n": 10, "region": "SPORT", "color": RED,
     "headline": "Dhoni ends IPL playing career",
     "deck": "MS Dhoni, 45, retires after 19 seasons; Chennai Super Kings name "
             "him team mentor for 2027.",
     "icon": "bat"},
    {"n": 11, "region": "SPORT", "color": GREEN,
     "headline": "India win record 10th SAFF title",
     "deck": "India beat Pakistan 2-1 in a thrilling final in Dhaka, extending "
             "their record.",
     "icon": "cup"},
]

BRIEFS = [
    (12, "ASEAN adopts AI declaration"),
    (13, "Modi offers free e-visas at ASEAN"),
    (14, "US presses UN over Taiwan flights"),
    (15, "Pope Leo ends tour; rosary hits eye"),
    (16, "Amazon pledges $7bn for India green"),
    (17, "India re-elected to ITU Council"),
    (18, "Jay Shah re-elected ICC chairman"),
    (19, "US loses measles-free status"),
    (20, "Fire in Thailand kills 11"),
    (21, "Anthropic prices IPO; ANT Thursday"),
    (22, "S&P 500 falls 1.03%"),
    (23, "Cyberattack hits 178 top companies"),
    (24, "Pakistan, Iran stress stability"),
    (25, "Japan offers ASEAN energy storage"),
    (26, "UEFA backs Diallo for FIFA top job"),
    (27, "US soldier held in UK on spy claim"),
    (28, "Caribbean fear citizenship costs"),
    (29, "Earthshot Prize ceremony in Mumbai"),
    (30, "El Nino brings droughts, wildfires"),
    (31, "N. Ireland reach Nations League top"),
    (32, "World COPD Day marked worldwide"),
]

TOTAL_STORIES = len(LEADS) + len(CARDS) + len(BRIEFS)


# ---------------------------------------------------------------- illustrations
def art_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 198, 210))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(96, 130, 150))
    for i in range(5):
        draw.line([(x + 20 + i * 62, y + h * 0.62), (x + 30 + i * 62, y + h * 0.80)],
                  fill=(255, 255, 255), width=2)
    # towers
    for tx in (x + w * 0.22, x + w * 0.72):
        draw.rectangle([tx - 5, y + 12, tx + 5, y + h * 0.62], fill=(30, 41, 59))
        draw.rectangle([tx - 26, y + 12, tx + 26, y + 20], fill=(30, 41, 59))
    # deck, broken in the middle
    draw.rectangle([x, y + h * 0.52, x + w * 0.44, y + h * 0.56], fill=(30, 41, 59))
    draw.rectangle([x + w * 0.58, y + h * 0.52, x + w, y + h * 0.56], fill=(30, 41, 59))
    # fallen span, tilted
    draw.polygon([(x + w * 0.44, y + h * 0.56), (x + w * 0.58, y + h * 0.56),
                  (x + w * 0.55, y + h * 0.72), (x + w * 0.46, y + h * 0.70)],
                 fill=(30, 41, 59))
    # cables
    draw.line([(x + w * 0.22, y + 14), (x + w * 0.44, y + h * 0.52)], fill=(60, 70, 80), width=2)
    draw.line([(x + w * 0.72, y + 14), (x + w * 0.58, y + h * 0.52)], fill=(60, 70, 80), width=2)
    # smoke
    for cx, cy, r in ((0.50, 0.30, 16), (0.55, 0.22, 20), (0.47, 0.18, 13)):
        draw.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                     fill=(90, 95, 100))
    # explosion star
    cx, cy = x + w * 0.51, y + h * 0.50
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        draw.line([(cx, cy), (cx + 26 * math.cos(a), cy + 26 * math.sin(a))],
                  fill=(249, 115, 22), width=5)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(250, 204, 21))


def art_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    # missile streaks
    for sx, sy, ln in ((0.15, 0.25, 60), (0.45, 0.12, 70), (0.70, 0.30, 55), (0.30, 0.45, 50)):
        x0, y0 = x + w * sx, y + h * sy
        draw.line([(x0, y0), (x0 + ln, y0 - ln * 0.45)], fill=(249, 115, 22), width=3)
        draw.line([(x0, y0), (x0 + ln * 0.6, y0 - ln * 0.27)], fill=(255, 255, 255), width=2)
    # city silhouette
    for bx, bw, bh in ((0.02, 0.16, 0.30), (0.20, 0.12, 0.42), (0.34, 0.18, 0.34),
                       (0.54, 0.14, 0.46), (0.70, 0.16, 0.32), (0.88, 0.10, 0.38)):
        draw.rectangle([x + w * bx, y + h * (0.98 - bh), x + w * (bx + bw), y + h * 0.98],
                       fill=(10, 10, 14))
        for wy in range(3):
            for wx in range(2):
                draw.rectangle([x + w * bx + 6 + wx * 14, y + h * (0.98 - bh) + 8 + wy * 14,
                                x + w * bx + 12 + wx * 14, y + h * (0.98 - bh) + 14 + wy * 14],
                               fill=(250, 204, 21))
    # flames in front of the skyline
    for fx, fh, fw in ((0.12, 0.52, 34), (0.32, 0.66, 44), (0.55, 0.58, 38), (0.78, 0.48, 30)):
        bx, by = x + w * fx, y + h * 0.98
        draw.polygon([(bx - fw / 2, by), (bx - fw / 4, by - fh * 0.7),
                      (bx, by - fh), (bx + fw / 4, by - fh * 0.7),
                      (bx + fw / 2, by)], fill=(234, 88, 12))
        draw.polygon([(bx - fw / 4, by), (bx, by - fh * 0.55), (bx + fw / 4, by)],
                     fill=(250, 204, 21))
    # smoke, small and high
    for cx, cy, r in ((0.35, 0.30, 12), (0.60, 0.22, 14), (0.82, 0.32, 10)):
        draw.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                     fill=(45, 45, 55))


def art_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 213, 171))
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 72, 32))
    draw.rectangle([x, y + h * 0.68, x + w, y + h * 0.74], fill=(90, 54, 24))
    # flags: US (stripes + canton), India, Japan, Australia (blue + stars)
    for i in range(4):
        fx = x + w * (0.10 + i * 0.23)
        draw.line([(fx, y + 8), (fx, y + h * 0.68)], fill=(60, 50, 40), width=3)
        fy = y + 10
        if i == 0:
            for j in range(5):
                draw.rectangle([fx, fy + j * 7, fx + 52, fy + (j + 1) * 7],
                               fill=(220, 38, 60) if j % 2 == 0 else (255, 255, 255),
                               outline=(60, 50, 40))
            draw.rectangle([fx, fy, fx + 22, fy + 14], fill=(0, 40, 120))
        elif i == 1:
            for j, col in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
                draw.rectangle([fx, fy + j * 12, fx + 52, fy + (j + 1) * 12],
                               fill=col, outline=(60, 50, 40))
            draw.ellipse([fx + 22, fy + 14, fx + 30, fy + 22], fill=(0, 40, 120))
        elif i == 2:
            draw.rectangle([fx, fy, fx + 52, fy + 36], fill=(255, 255, 255),
                           outline=(60, 50, 40))
            draw.ellipse([fx + 20, fy + 11, fx + 32, fy + 23], fill=(188, 0, 45))
        else:
            draw.rectangle([fx, fy, fx + 52, fy + 36], fill=(0, 40, 120),
                           outline=(60, 50, 40))
            for sx, sy in ((10, 6), (26, 14), (40, 8), (18, 24), (36, 26)):
                draw.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2, fy + sy + 2],
                             fill=(255, 255, 255))
    # papers and microphones on the table
    for i in range(4):
        fx = x + w * (0.13 + i * 0.23)
        draw.rectangle([fx - 16, y + h * 0.76, fx + 16, y + h * 0.88],
                       fill=(255, 255, 255), outline=(120, 100, 70))
        draw.line([(fx + 14, y + h * 0.76), (fx + 22, y + h * 0.70)], fill=(40, 40, 48),
                  width=2)
        draw.ellipse([fx + 20, y + h * 0.68, fx + 26, y + h * 0.70 + 6], fill=(40, 40, 48))


ART = {"bridge": art_bridge, "fire": art_fire, "summit": art_summit}


def icon(draw, x, y, kind, s=44):
    c = INK
    if kind == "chip":
        draw.rectangle([x, y, x + s, y + s], outline=c, width=3)
        draw.rectangle([x + 10, y + 10, x + s - 10, y + s - 10], outline=c, width=2)
        for i in range(3):
            for xx in (x - 6, x + s):
                draw.line([(xx, y + 8 + i * 14), (xx + 6 if xx == x - 6 else xx - 6,
                                                  y + 8 + i * 14)], fill=c, width=2)
            for yy in (y - 6, y + s):
                draw.line([(x + 8 + i * 14, yy), (x + 8 + i * 14,
                                                  yy + 6 if yy == y - 6 else yy - 6)],
                          fill=c, width=2)
        draw.line([(x + 12, y + s - 12), (x + s / 2, y + 14), (x + s - 12, y + 10)],
                  fill=TEAL, width=3)
    elif kind == "storm":
        for r in (6, 12, 18):
            draw.arc([x + s / 2 - r, y + s / 2 - r, x + s / 2 + r, y + s / 2 + r],
                     start=20, end=300, fill=BLUE, width=3)
        draw.ellipse([x + s / 2 - 4, y + s / 2 - 4, x + s / 2 + 4, y + s / 2 + 4], fill=BLUE)
    elif kind == "deal":
        draw.line([(x + 4, y + s - 8), (x + s / 2, y + 10), (x + s - 4, y + s - 8)],
                  fill=GREEN, width=3)
        draw.polygon([(x + s / 2 - 8, y + 2), (x + s / 2 + 8, y + 2), (x + s / 2, y + 14)],
                     fill=GREEN)
    elif kind == "ban":
        draw.ellipse([x, y, x + s, y + s], outline=RED, width=4)
        draw.line([(x + 6, y + s - 6), (x + s - 6, y + 6)], fill=RED, width=4)
    elif kind == "tanker":
        draw.rectangle([x + 4, y + s * 0.45, x + s - 4, y + s * 0.72], fill=ORANGE)
        draw.rectangle([x + s * 0.62, y + s * 0.25, x + s * 0.8, y + s * 0.45], fill=INK)
        draw.line([(x, y + s * 0.75), (x + s, y + s * 0.75)], fill=BLUE, width=3)
    elif kind == "robot":
        draw.rectangle([x + 6, y + 10, x + s - 6, y + s - 8], outline=NAVY, width=3)
        draw.ellipse([x + 12, y + 20, x + 20, y + 28], fill=NAVY)
        draw.ellipse([x + s - 20, y + 20, x + s - 12, y + 28], fill=NAVY)
        draw.line([(x + s / 2, y + 10), (x + s / 2, y + 2)], fill=NAVY, width=3)
        draw.ellipse([x + s / 2 - 3, y - 2, x + s / 2 + 3, y + 4], fill=RED)
    elif kind == "bat":
        draw.line([(x + 8, y + s - 6), (x + s - 14, y + 12)], fill=(139, 90, 43), width=7)
        draw.ellipse([x + s - 22, y + 2, x + s - 6, y + 18], fill=RED)
    elif kind == "cup":
        draw.polygon([(x + 10, y + 6), (x + s - 10, y + 6), (x + s - 14, y + s * 0.55),
                      (x + 14, y + s * 0.55)], fill=GOLD)
        draw.line([(x + s / 2, y + s * 0.55), (x + s / 2, y + s - 8)], fill=GOLD, width=4)
        draw.line([(x + 8, y + s - 8), (x + s - 8, y + s - 8)], fill=GOLD, width=4)


# ---------------------------------------------------------------- world map
NA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
      (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
      (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-100, 20), (-105, 23),
      (-110, 28), (-115, 32), (-125, 40), (-125, 48), (-135, 58), (-150, 60),
      (-165, 60)]
GL = [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-25, 70), (-35, 76),
      (-55, 76), (-60, 74)]
SA = [(-80, 10), (-75, 10), (-70, 12), (-62, 10), (-55, 5), (-50, 0),
      (-45, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35),
      (-65, -40), (-70, -50), (-73, -55), (-70, -45), (-72, -35), (-72, -25),
      (-75, -15), (-80, -5), (-80, 5)]
AF = [(-10, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 22),
      (43, 12), (48, 11), (51, 12), (45, 5), (42, -2), (40, -10), (35, -18),
      (32, -26), (28, -33), (20, -35), (15, -28), (12, -18), (12, -8), (9, 4),
      (0, 5), (-8, 5), (-15, 10), (-17, 15), (-16, 20), (-15, 25), (-12, 30)]
EUAS = [(-10, 36), (-9, 43), (-2, 48), (5, 53), (8, 57), (18, 56), (24, 58),
        (30, 62), (30, 68), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76),
        (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
        (150, 50), (142, 45), (140, 40), (135, 35), (130, 33), (127, 35),
        (122, 38), (120, 32), (115, 25), (110, 20), (105, 10), (100, 8),
        (98, 12), (95, 16), (92, 21), (90, 22), (86, 20), (82, 17), (80, 13),
        (77, 8), (75, 12), (72, 20), (68, 22), (65, 25), (60, 25), (57, 26),
        (54, 27), (52, 28), (50, 29), (48, 30), (44, 29), (40, 30), (36, 36),
        (30, 36), (27, 37), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44),
        (3, 42), (0, 40), (-2, 37), (-6, 36)]
AU = [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
      (132, -32), (135, -35), (138, -35), (140, -38), (142, -38), (145, -38),
      (147, -39), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20),
      (146, -19), (142, -15), (142, -11), (140, -15), (137, -12), (135, -12),
      (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
CONTINENTS = [NA, GL, SA, AF, EUAS, AU]

PINS = [(1, 33, 47, "Kerch Strait"), (2, 45, 29, "Bahrain"),
        (3, 122, 14, "Manila"), (5, 88, 6, "Bay of Bengal"),
        (6, 117, 41, "Beijing"), (7, -3, 55, "London"),
        (8, 62, 23, "Hormuz"), (10, 79, 15, "Chennai"),
        (11, 94, 26, "Dhaka")]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=OCEAN, outline=INK, width=2)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -56
    sx = w / (lon1 - lon0)
    sy = h / (lat1 - lat0) * -1
    # use a common scale so shapes are not stretched
    s = min(sx, sy)
    ox = x + (w - (lon1 - lon0) * s) / 2
    oy = y + (h - (lat0 - lat1) * s) / 2

    def proj(lon, lat):
        return (ox + (lon - lon0) * s, oy + (lat0 - lat) * s)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=LAND_LINE)
    for n, lon, lat, _name in PINS:
        px, py = proj(lon, lat)
        badge(draw, px, py, 8, n, fill=RED)


def map_key(draw, x, y, w):
    f = font(F_SANS, 13)
    parts = ["1 Kerch Strait", "2 Bahrain", "3 Manila", "5 Bay of Bengal",
             "6 Beijing", "7 London", "8 Hormuz", "10 Chennai", "11 Dhaka"]
    lines, cur = [], ""
    for p in parts:
        trial = (cur + "  ·  " + p).strip("  ·  ") if cur else p
        if draw.textlength(trial, font=f) <= w:
            cur = trial
        else:
            lines.append(cur)
            cur = p
    if cur:
        lines.append(cur)
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=f, fill=GREY)
        yy += 18
    return yy


# ---------------------------------------------------------------- variant A
def render_a():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # kicker
    text(d, (16, 12), "THE WORLD'S NEWS IN ONE PICTURE", font(F_SANS_BOLD, 15), fill=RED)
    f = font(F_SANS_BOLD, 15)
    s = "%d STORIES · SIX CONTINENTS" % TOTAL_STORIES
    d.text((1008, 12), s, font=f, fill=GREY, anchor="ra")
    # masthead: the date itself
    centered(d, 512, 30, "Wednesday 18 November 2026", font(F_SERIF_BLACK, 60))
    rule(d, 16, 100, 1008, 3)
    rule(d, 16, 105, 1008, 1)
    centered(d, 512, 112,
             "The world's news, in one image — every story below happened or was "
             "first reported today",
             font(F_SERIF_IT, 15), fill=GREY)
    # leads
    xs = [16, 350, 684]
    for lead, lx in zip(LEADS, xs):
        w = 322
        ART[lead["art"]](d, lx, 134, w, 122)
        badge(d, lx + 20, 154, 15, lead["n"], fill=lead["color"])
        yy = 264
        text(d, (lx, yy), lead["region"], font(F_SANS_BOLD, 14), fill=lead["color"])
        yy += 20
        for ln in wrap(d, lead["headline"], font(F_SERIF_BOLD, 26), w):
            text(d, (lx, yy), ln, font(F_SERIF_BOLD, 26))
            yy += 29
        yy += 2
        for ln in wrap(d, lead["deck"], font(F_SERIF, 14), w):
            text(d, (lx, yy), ln, font(F_SERIF, 14))
            yy += 18
    rule(d, 16, 386, 1008, 1)
    # cards 4-11, 4 columns x 2 rows
    cxs = [16, 263, 510, 757]
    for i, card in enumerate(CARDS):
        cx = cxs[i % 4]
        cy = 398 + (i // 4) * 118
        badge(d, cx + 11, cy + 11, 11, card["n"], fill=card["color"])
        text(d, (cx + 28, cy), card["region"], font(F_SANS_BOLD, 12), fill=card["color"])
        yy = cy + 17
        for ln in wrap(d, card["headline"], font(F_SERIF_BOLD, 18), 240):
            text(d, (cx, yy), ln, font(F_SERIF_BOLD, 18))
            yy += 21
        for ln in wrap(d, card["deck"], font(F_SERIF, 13), 240):
            text(d, (cx, yy), ln, font(F_SERIF, 13))
            yy += 16
    rule(d, 16, 640, 1008, 1)
    # bottom left: briefs
    text(d, (16, 652), "ALSO ON WEDNESDAY 18 NOVEMBER",
         font(F_SANS_BOLD, 15), fill=RED)
    rule(d, 16, 674, 556, 1)
    cols = [BRIEFS[:11], BRIEFS[11:]]
    for ci, col in enumerate(cols):
        bx = 16 + ci * 274
        yy = 684
        for n, txt in col:
            text(d, (bx, yy), str(n), font(F_SANS_BOLD, 12), fill=RED)
            text(d, (bx + 24, yy), txt, font(F_SANS, 12))
            yy += 17
    # bottom right: map
    text(d, (572, 652), "WHERE IT HAPPENED", font(F_SANS_BOLD, 15), fill=RED)
    rule(d, 572, 674, 1008, 1)
    draw_map(d, 572, 684, 436, 210)
    yy = map_key(d, 572, 906, 436)
    text(d, (572, yy + 6), "Numbers match the stories above.",
         font(F_SERIF_IT, 13), fill=GREY)
    # footer
    rule(d, 16, 986, 1008, 1)
    centered(d, 512, 992,
             "Every story above happened or was first reported on Wednesday 18 "
             "November 2026, checked against reporting published that day. "
             "Original drawings.",
             font(F_SANS, 11), fill=GREY)
    return img


# ---------------------------------------------------------------- variant B
def render_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # nameplate
    d.rectangle([0, 0, W, 64], fill=(16, 16, 18))
    text(d, (16, 10), "THE DAILY GLOBE", font(F_SERIF_BLACK, 42), fill=(255, 255, 255))
    f = font(F_SANS_BOLD, 15)
    d.text((1008, 24), "ONE DAY · ONE WORLD", font=f, fill=(212, 175, 55), anchor="ra")
    rule(d, 0, 64, W, 4, fill=(166, 124, 0))
    centered(d, 512, 74, "WEDNESDAY 18 NOVEMBER 2026", font(F_SERIF_BLACK, 44),
             fill=TEAL)
    centered(d, 512, 124,
             "THE WORLD'S NEWS, IN ONE IMAGE — EVERY STORY BELOW HAPPENED OR WAS "
             "FIRST REPORTED TODAY",
             font(F_SANS_BOLD, 12), fill=GREY)
    # two leads
    for lead, lx in zip(LEADS[:2], [16, 522]):
        w = 486
        ART[lead["art"]](d, lx, 150, w, 118)
        badge(d, lx + 20, 170, 15, lead["n"], fill=lead["color"])
        yy = 276
        text(d, (lx, yy), "LEAD · " + lead["region"], font(F_SANS_BOLD, 13),
             fill=lead["color"])
        yy += 18
        for ln in wrap(d, lead["headline"], font(F_SERIF_BOLD, 26), w):
            text(d, (lx, yy), ln, font(F_SERIF_BOLD, 26))
            yy += 29
        yy += 2
        for ln in wrap(d, lead["deck"], font(F_SERIF, 14), w):
            text(d, (lx, yy), ln, font(F_SERIF, 14))
            yy += 18
    # summit band
    d.rectangle([16, 400, 1008, 470], fill=TEAL)
    band = [("SUMMIT WEEK", "MANILA", "Trump at ASEAN and Quad talks"),
            ("BEIJING NEXT", "APEC OPENS", "Xi hosts 21 economies"),
            ("TRADE", "OTTAWA-BEIJING", "Canada-China extend trade deals")]
    for i, (kick, head, sub) in enumerate(band):
        bx = 16 + i * 331
        text(d, (bx + 12, 408), kick, font(F_SANS_BOLD, 12), fill=(212, 175, 55))
        text(d, (bx + 12, 426), head, font(F_SERIF_BOLD, 20), fill=(255, 255, 255))
        text(d, (bx + 12, 450), sub, font(F_SANS, 13), fill=(255, 255, 255))
    # continent columns
    cols = [
        ("EUROPE", TEAL, "Britain sanctions Israeli settlement firms",
         "London blacklists firms linked to West Bank settlements."),
        ("MIDDLE EAST", RED, "India condemns tanker attack in Hormuz",
         "MT TARA GAS hit; 21 of 24 Indian crew evacuated at Khasab."),
        ("ASIA", (150, 100, 0), "Cyclone Akvan builds in the Bay of Bengal",
         "Landfall in Andhra Pradesh on Friday; flights cancelled."),
        ("AMERICAS", BLUE, "US loses measles-free status",
         "Worst outbreak since 1991 passes 5,400 cases."),
        ("OCEANIA", GREEN, "Australia's pay gap falls below 20%",
         "Down to 19.7% for the first time, figures show."),
        ("WORLD", PURPLE, "World COPD Day marked around the globe",
         "Health agencies urge earlier checks for lung disease."),
    ]
    cxs = [16, 179, 342, 505, 668, 831]
    for (region, color, head, sub), cx in zip(cols, cxs):
        d.rectangle([cx, 482, cx + 152, 506], fill=color)
        text(d, (cx + 6, 486), region, font(F_SANS_BOLD, 12), fill=(255, 255, 255))
        yy = 512
        for ln in wrap(d, head, font(F_SERIF_BOLD, 15), 152):
            text(d, (cx, yy), ln, font(F_SERIF_BOLD, 15))
            yy += 18
        for ln in wrap(d, sub, font(F_SANS, 11), 152):
            text(d, (cx, yy), ln, font(F_SANS, 11))
            yy += 14
    # rest of the day: cards 4, 9, 10, 11 + briefs 12-28 = 21 items
    rest = [(CARDS[0]["n"], CARDS[0]["headline"], CARDS[0]["deck"]),
            (CARDS[5]["n"], CARDS[5]["headline"], CARDS[5]["deck"]),
            (CARDS[6]["n"], CARDS[6]["headline"], CARDS[6]["deck"]),
            (CARDS[7]["n"], CARDS[7]["headline"], CARDS[7]["deck"])]
    for n, txt in BRIEFS[:17]:
        rest.append((n, txt, ""))
    text(d, (16, 636), "THE REST OF THE DAY", font(F_SANS_BOLD, 15), fill=INK)
    rule(d, 16, 658, 1008, 1)
    for i, (n, head, sub) in enumerate(rest):
        col, row = i % 3, i // 3
        bx = 16 + col * 331
        by = 668 + row * 40
        badge(d, bx + 11, by + 11, 11, n, fill=TEAL)
        yy = by
        for ln in wrap(d, head, font(F_SERIF_BOLD, 14), 290):
            text(d, (bx + 28, yy), ln, font(F_SERIF_BOLD, 14))
            yy += 17
    rule(d, 16, 986, 1008, 1)
    centered(d, 512, 992,
             "THE DAILY GLOBE · WEDNESDAY 18 NOVEMBER 2026 · Every story above "
             "happened or was first reported on 18 November 2026, checked against "
             "reporting published that day.",
             font(F_SANS, 11), fill=GREY)
    return img


# ---------------------------------------------------------------- variant C
def render_c():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 70], fill=NAVY)
    centered(d, 512, 12, "THE WORLD IN ONE DAY", font(F_SERIF_BLACK, 40),
             fill=(255, 255, 255))
    rule(d, 0, 70, W, 4, fill=(166, 124, 0))
    text(d, (16, 80), "WEDNESDAY 18 NOVEMBER 2026", font(F_SANS_BOLD, 15), fill=RED)
    f = font(F_SANS_BOLD, 15)
    d.text((1008, 80), "28 STORIES · WORLDWIDE", font=f, fill=GREY,
           anchor="ra")
    rule(d, 16, 102, 1008, 1)
    # big lead: illustration left, headline right
    lead = LEADS[0]
    ART[lead["art"]](d, 16, 112, 430, 158)
    badge(d, 36, 132, 15, lead["n"], fill=lead["color"])
    text(d, (470, 116), "WAR IN UKRAINE", font(F_SANS_BOLD, 13), fill=RED)
    yy = 136
    for ln in wrap(d, lead["headline"], font(F_SERIF_BOLD, 32), 538):
        text(d, (470, yy), ln, font(F_SERIF_BOLD, 32))
        yy += 36
    yy += 4
    for ln in wrap(d, lead["deck"], font(F_SERIF, 15), 538):
        text(d, (470, yy), ln, font(F_SERIF, 15))
        yy += 19
    rule(d, 16, 282, 1008, 1)
    # three mid stories
    mids = [(LEADS[2], "DIPLOMACY", "Trump in Manila for Quad talks",
             "Then on to China for APEC and Xi."),
            (LEADS[1], "MIDEAST", "Iran hits US radar in Bahrain",
             "Drone strike on a US base; Gulf on edge."),
            (None, "TRADE", "APEC opens in Shenzhen",
             "Xi chairs 21 economies; trade in focus.")]
    for i, (ld, region, head, sub) in enumerate(mids):
        bx = 16 + i * 331
        text(d, (bx, 294), region, font(F_SANS_BOLD, 13), fill=RED)
        yy = 314
        for ln in wrap(d, head, font(F_SERIF_BOLD, 20), 300):
            text(d, (bx, yy), ln, font(F_SERIF_BOLD, 20))
            yy += 23
        text(d, (bx, yy), sub, font(F_SERIF, 14))
        if i < 2:
            d.line([(bx + 315, 294), (bx + 315, 372)], fill=GREY, width=1)
    rule(d, 16, 384, 1008, 1)
    # brief grid: cards 4-11 + briefs 12-27 = 24 items
    grid = []
    for c in CARDS:
        grid.append((c["n"], c["region"], c["headline"]))
    for n, txt in BRIEFS[:16]:
        grid.append((n, "BRIEF", txt))
    text(d, (16, 396), "THE DAY IN BRIEF", font(F_SANS_BOLD, 15), fill=INK)
    f = font(F_SANS_BOLD, 15)
    d.text((1008, 396), "24 MORE STORIES", font=f, fill=RED, anchor="ra")
    rule(d, 16, 418, 1008, 1)
    for i, (n, region, head) in enumerate(grid):
        col, row = i % 4, i // 4
        bx = 16 + col * 248
        by = 430 + row * 92
        d.rectangle([bx, by, bx + 240, by + 84], outline=GREY, width=1)
        text(d, (bx + 8, by + 6), region, font(F_SANS_BOLD, 11), fill=TEAL)
        yy = by + 22
        for ln in wrap(d, head, font(F_SERIF_BOLD, 14), 224):
            text(d, (bx + 8, yy), ln, font(F_SERIF_BOLD, 14))
            yy += 17
    rule(d, 16, 986, 1008, 1)
    centered(d, 512, 992,
             "Headlines checked against reporting published 18 November 2026. "
             "Original drawings.",
             font(F_SANS, 11), fill=GREY)
    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    import os
    os.makedirs("candidates", exist_ok=True)
    if variant == "A":
        img = render_a()
    elif variant == "B":
        img = render_b()
    elif variant == "C":
        img = render_c()
    else:
        raise SystemExit("unknown variant %s" % variant)
    out = "candidates/%s.png" % variant.lower()
    img.save(out, optimize=True)
    import os as _os
    print(out, _os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    main()
