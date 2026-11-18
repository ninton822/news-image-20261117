#!/usr/bin/env python3
"""Render the front page of THE DAILY GLOBE for Tuesday 17 November 2026.

Draws a 1024x1024 broadsheet front page with PIL: masthead, a lead story
on the Kerch Bridge collapse, five illustrated second-tier stories, a world
map with numbered markers, and a 36-item day-in-brief list (42 stories in
all). Every story was checked against reporting from 17 November 2026.
Run: python3 render.py  ->  writes entry.png beside this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (163, 18, 18)
BLUE = (31, 78, 121)
GRAY = (85, 85, 85)
LIGHT = (233, 220, 189)
SEA = (215, 229, 238)
LAND = (232, 219, 184)
RULE = (120, 110, 90)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, f, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, f, fill=INK, leading=None):
    if leading is None:
        leading = int(f.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def trunc(text, f, max_w):
    """Shorten text with an ellipsis so it fits max_w pixels."""
    if f.getlength(text) <= max_w:
        return text
    while text and f.getlength(text + "…") > max_w:
        text = text[:-1].rstrip()
    return text + "…"


def hline(d, x0, x1, y, w=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- stories
# (number, kicker, headline, summary, source)
LEAD = (
    1, "UKRAINE WAR",
    "Ukraine brings down Kerch Bridge arch in overnight strike",
    "A road span of the Kerch Bridge collapsed into the strait early on "
    "Tuesday after a seven-stage Ukrainian operation of drones and missiles. "
    "The road link to occupied Crimea is severed; rail traffic was halted, "
    "then partly restored. Russia answered by striking two bridges in Kyiv, "
    "cutting power, water and heating in parts of the capital.",
    "AP · Reuters · Kyiv Independent",
)

TIER = [
    (2, "IRAN - US",
     "US jets hit Qeshm after Iran drones hit Bahrain",
     "Iran fired drones at a US radar base in Bahrain; all were intercepted.",
     "AP · Reuters"),
    (3, "MARKETS",
     "Nvidia posts record $115.8bn quarter",
     "Revenue rose 103% to $115.8bn, beating estimates; $130bn guided.",
     "Nvidia · Bloomberg"),
    (4, "ASIA",
     "Trump opens Asia trip in Manila",
     "Trump met Quad leaders in Manila to open his Asia trip.",
     "AP · Reuters"),
    (5, "GAZA",
     "West urges Israel: open Gaza crossings",
     "Four Western states called the aid situation catastrophic.",
     "AP · WFP · IOM"),
    (6, "HORMUZ",
     "Fourth tanker ablaze in 24 hours",
     "Iran said a fourth tanker caught fire after hitting a naval mine.",
     "Reuters · Iran claim"),
]

# (number, headline, summary, source)
BRIEF = [
    (7, "Russia hits two Kyiv bridges in reply",
     "Both Dnipro crossings closed; metro damaged, power and heat cut.", "Reuters"),
    (8, "Ukraine peace talks go on, no deal",
     "Kyiv held further talks with US and European envoys on ending the war.", "Reuters"),
    (9, "Russian drone flew over Chisinau",
     "Moldova's president said the drone crossed the capital's airspace.", "Reuters"),
    (10, "Kerch collapse threatens Azov grain trade",
     "Debris blocks the canal; Azov carries a quarter of Russia's grain exports.", "Splash247"),
    (11, "Trump: 'dirty bomb' threat taken seriously",
     "US intelligence says Iran is weighing an attack on Washington; Tehran calls it baseless.", "USA Today"),
    (12, "Third US carrier reaches the Gulf",
     "USS Theodore Roosevelt joins two carriers in the Middle East.", "CENTCOM"),
    (13, "Qatar-Iran talks; Iran FM in Oman",
     "Tehran says it is reviewing the latest US text, sent via Pakistan.", "Reuters"),
    (14, "Militia defies Iraq pullout deadline",
     "Kataib Hezbollah refuses to leave Jurf al-Sakhar despite an order.", "Arab News"),
    (15, "Houthis advance in Yemen",
     "Government forces pull back from the Red Sea coast to defend Aden.", "AP"),
    (16, "Strike kills at least 7 in Hudaydah",
     "Houthis blame a Saudi airstrike on a sponge factory; toll unconfirmed.", "Ansarullah"),
    (17, "Gaza: 1.7m displaced, 1.4m hungry",
     "UN agencies warn of a worsening winter emergency in the Strip.", "WFP · IOM"),
    (18, "Settler mob kills woman, 72, in Jericho",
     "The killing happened overnight in the occupied West Bank.", "Foreign Exch."),
    (19, "Israel suspends E1 settlement tender",
     "The attorney general froze the plan; Eisenkot ally elected Knesset speaker.", "Foreign Exch."),
    (20, "Five EU states plan Rwanda return hub",
     "Austria, Denmark, Germany, Greece and the Netherlands; Amnesty calls it disgraceful.", "AP · Amnesty"),
    (21, "IOM: Rwanda asked about return hub",
     "The migration agency says it received a request from Kigali.", "PANA"),
    (22, "Cabo Verde: Neves re-elected, 64%",
     "ECOWAS hails a peaceful vote; turnout was low, abstention near 68%.", "ECOWAS"),
    (23, "Gambia campaign opens for Dec 5 vote",
     "Nine candidates cleared; President Barrow seeks a third term.", "PANA"),
    (24, "Sudan drones killed 1,600+ in 2026",
     "UN rights body counts the dead; RSF strikes on El Obeid probed as war crimes.", "PANA"),
    (25, "South Sudan vote pushed to Feb 2027",
     "The first general elections since independence are postponed again.", "PANA"),
    (26, "Japan scrambles jets on Russian planes",
     "Two suspected Russian aircraft entered Japanese airspace, Tokyo says.", "AP"),
    (27, "COP31 enters decisive stage",
     "Climate negotiators in Antalya work on a first draft agreement.", "AP"),
    (28, "Eritrea: trachoma eliminated",
     "WHO validates the end of the eye disease as a public-health problem.", "WHO"),
    (29, "Mongolia president quits in scandal",
     "Ukhnaagiin Khurelsukh resigns amid an emerging corruption case.", "Foreign Exch."),
    (30, "Markets slide: Dow falls 850 points",
     "S&P 500 -1.0%, Nasdaq -0.7% ahead of Nvidia's results after the bell.", "MarketWatch"),
    (31, "Bitcoin stalls below $65,000",
     "The coin is down more than 15% in November as traders watch Nvidia.", "Press"),
    (32, "Gold slides as stocks fall",
     "The haven metal drops with equities as yields climb.", "FXStreet"),
    (33, "AFCON: six teams book their places",
     "Morocco, Senegal, Benin, Burkina Faso, Cameroon and Mali qualify.", "Reuters"),
    (34, "US closes Nvidia chip-export loophole",
     "New rule limits third-country data centres renting computing to China.", "Commerce Dept"),
    (35, "Top court lets UC grants ruling stand",
     "The Supreme Court declines to revive $59m in Trump cuts to UC research.", "AP"),
    (36, "Pentagon fails audit, ninth year",
     "The Defence Department fails its annual audit again; 14 of 25 units pass.", "AP"),
    (37, "NSA internal network crashes",
     "The spy agency's communications net went down; no cyberattack seen yet.", "CNN"),
    (38, "Measles: 13 US babies born with it",
     "5,412 US cases since 2025, the most since 1991, CDC figures show.", "CDC"),
    (39, "Depardieu pleads guilty to sex assault",
     "The French actor drops his appeal before a Paris court.", "AP · AFP"),
    (40, "Epstein death 'murder', expert claims",
     "A forensic expert disputes suicide; the claim is contested, not proven.", "Press"),
    (41, "Dual quasars in one early galaxy",
     "Two giant black holes found in a galaxy under a billion years after the Big Bang.", "Astronomers"),
    (42, "AI reads 48 tRNA types at 98.2%",
     "Tokyo researchers classify transfer RNA from nanopore signals.", "Univ. of Tokyo"),
]

# (story number, place, lon, lat) — display positions nudged where stories
# cluster, so the numbered dots never sit on top of each other.
MARKERS = [
    (1, "Kerch Strait", 37.5, 44.0),
    (7, "Kyiv", 29.0, 51.8),
    (2, "Bahrain", 49.5, 26.2),
    (2, "Qeshm I.", 54.0, 28.5),
    (5, "Gaza", 34.5, 31.5),
    (6, "Hormuz", 57.5, 24.0),
    (4, "Manila", 121.0, 14.6),
    (4, "Shenzhen", 114.0, 22.5),
    (26, "Tokyo", 139.7, 35.7),
    (39, "Paris", 2.35, 48.85),
    (20, "Kigali", 30.0, -1.9),
    (15, "Aden", 45.0, 12.8),
    (9, "Chisinau", 30.5, 45.8),
    (22, "Praia", -23.5, 14.9),
    (29, "Ulaanbaatar", 106.9, 47.9),
    (11, "Washington", -77.0, 38.9),
]

# ---------------------------------------------------------------- map data
# Coarse continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 72), (-60, 62), (-55, 52), (-65, 45), (-75, 35), (-80, 25),
     (-90, 20), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 48),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-60, 70)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-70, -20),
     (-80, -5), (-80, 5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (25, -34),
     (18, -35), (12, -18), (9, 4), (-8, 5), (-15, 12)],
    [(-10, 36), (0, 44), (-5, 48), (0, 51), (5, 53), (10, 57), (18, 56),
     (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (50, 69), (60, 70),
     (70, 73), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
     (140, 72), (150, 70), (160, 70), (170, 67), (178, 65), (170, 60),
     (162, 56), (158, 52), (150, 59), (142, 50), (140, 40), (135, 35),
     (130, 33), (127, 35), (122, 38), (120, 32), (110, 20), (108, 10),
     (105, 2), (100, 8), (95, 16), (90, 22), (85, 20), (80, 15), (77, 8),
     (72, 20), (66, 25), (60, 25), (57, 26), (52, 28), (50, 30), (48, 30),
     (44, 29), (40, 32), (36, 36), (30, 36), (26, 38), (22, 37), (19, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37), (-10, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
    [(-4, 54), (-2, 58), (0, 53), (-3, 50), (-5, 52)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38),
     (141, 41), (140, 44), (142, 44), (144, 43), (141, 39), (139, 37),
     (136, 33), (133, 34), (131, 32)],
    [(95, -5), (100, -2), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -9), (130, -5), (135, -4), (140, -5), (138, -8), (132, -9),
     (125, -10), (118, -10), (112, -8), (106, -6), (100, -5)],
    [(167, -45), (169, -43), (172, -41), (175, -40), (177, -38), (175, -38),
     (173, -41), (170, -43), (167, -45)],
]


def project(lon, lat, x0, y0, xscale, yscale, lat_top):
    return (x0 + (lon + 180) * xscale, y0 + (lat_top - lat) * yscale)


# ---------------------------------------------------------------- panels
def draw_bridge(d, x0, y0, w, h):
    """Stylised Kerch Bridge scene: sky, sea, bridge, collapsed span."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(207, 224, 234))
    # sun and clouds
    d.ellipse([x0 + w - 52, y0 + 10, x0 + w - 22, y0 + 40], fill=(240, 214, 130))
    for cx, cy, r in [(x0 + 40, y0 + 22, 12), (x0 + 62, y0 + 18, 15),
                      (x0 + 84, y0 + 24, 11)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    # sea
    sea_y = y0 + int(h * 0.62)
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=(127, 168, 201))
    for i in range(5):
        wx = x0 + 20 + i * 68
        d.line([(wx, sea_y + 14 + (i % 2) * 8), (wx + 34, sea_y + 14 + (i % 2) * 8)],
               fill=(255, 255, 255), width=2)
    # bridge deck: left part intact, middle collapsed, right part intact
    deck_y = y0 + int(h * 0.48)
    d.rectangle([x0, deck_y, x0 + int(w * 0.36), deck_y + 7], fill=(60, 60, 60))
    d.rectangle([x0 + int(w * 0.62), deck_y, x0 + w, deck_y + 7], fill=(60, 60, 60))
    # towers
    for tx in (x0 + int(w * 0.16), x0 + int(w * 0.80)):
        d.rectangle([tx - 3, deck_y - 52, tx + 3, deck_y], fill=(60, 60, 60))
        d.line([(tx, deck_y - 52), (x0 + int(w * 0.36), deck_y)], fill=(90, 90, 90), width=1)
        d.line([(tx, deck_y - 52), (x0 + int(w * 0.62), deck_y)], fill=(90, 90, 90), width=1)
    # fallen span in the water, tilted
    d.polygon([(x0 + int(w * 0.40), deck_y + 4), (x0 + int(w * 0.60), deck_y + 4),
               (x0 + int(w * 0.56), deck_y + 34), (x0 + int(w * 0.44), deck_y + 34)],
              fill=(90, 90, 90))
    d.line([(x0 + int(w * 0.40), deck_y + 4), (x0 + int(w * 0.44), deck_y + 34)],
           fill=(60, 60, 60), width=2)
    # smoke from the break
    for cx, cy, r in [(x0 + int(w * 0.47), deck_y - 14, 13),
                      (x0 + int(w * 0.50), deck_y - 30, 17),
                      (x0 + int(w * 0.54), deck_y - 48, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    # explosion starburst at the break
    ex, ey = x0 + int(w * 0.50), deck_y - 2
    for ang in range(0, 360, 30):
        import math
        dx = math.cos(math.radians(ang)) * 16
        dy = math.sin(math.radians(ang)) * 16
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(230, 120, 30), width=3)
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(240, 170, 40))


def draw_tier_panel(d, x0, y0, w, h, kind):
    """Small abstract illustration for a second-tier story."""
    if kind == "iran":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 32, 58))
        for r in (14, 26, 38):
            d.arc([x0 + w // 2 - r, y0 + h // 2 - r, x0 + w // 2 + r, y0 + h // 2 + r],
                  200, 340, fill=(90, 200, 120), width=2)
        d.line([(x0 + w // 2, y0 + h // 2), (x0 + w // 2 + 34, y0 + h // 2 - 22)],
               fill=(200, 220, 200), width=2)
        dx, dy = x0 + w // 2 + 34, y0 + h // 2 - 22
        d.polygon([(dx - 8, dy), (dx + 8, dy), (dx, dy - 5)], fill=(220, 220, 220))
        d.polygon([(dx - 8, dy), (dx + 8, dy), (dx, dy + 5)], fill=(180, 180, 180))
        for ang in range(0, 360, 45):
            import math
            ex = x0 + 24 + math.cos(math.radians(ang)) * 9
            ey = y0 + 22 + math.sin(math.radians(ang)) * 9
            d.line([(x0 + 24, y0 + 22), (ex, ey)], fill=(240, 160, 40), width=2)
    elif kind == "nvidia":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 42, 28))
        cx, cy = x0 + 44, y0 + h // 2
        d.rectangle([cx - 22, cy - 22, cx + 22, cy + 22], fill=(46, 160, 67))
        d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=(16, 42, 28))
        for i in range(-1, 2):
            d.line([(cx + i * 14, cy - 30), (cx + i * 14, cy - 22)], fill=(200, 220, 200), width=2)
            d.line([(cx + i * 14, cy + 22), (cx + i * 14, cy + 30)], fill=(200, 220, 200), width=2)
            d.line([(cx - 30, cy + i * 14), (cx - 22, cy + i * 14)], fill=(200, 220, 200), width=2)
            d.line([(cx + 22, cy + i * 14), (cx + 30, cy + i * 14)], fill=(200, 220, 200), width=2)
        pts = [(x0 + 84, y0 + h - 18), (x0 + 112, y0 + h - 38), (x0 + 132, y0 + h - 30),
               (x0 + 158, y0 + h - 52), (x0 + 180, y0 + h - 62)]
        d.line(pts, fill=(120, 220, 140), width=3, joint="curve")
        d.polygon([(x0 + 180, y0 + h - 62), (x0 + 168, y0 + h - 60), (x0 + 178, y0 + h - 50)],
                  fill=(120, 220, 140))
    elif kind == "asia":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(190, 214, 232))
        d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(120, 130, 120))
        for i, col in enumerate([(178, 34, 34), (34, 80, 160), (220, 190, 60), (40, 120, 60)]):
            fx = x0 + 28 + i * 40
            d.line([(fx, y0 + 12), (fx, y0 + h - 26)], fill=(80, 80, 80), width=2)
            d.rectangle([fx, y0 + 14, fx + 26, y0 + 30], fill=col)
        d.rectangle([x0 + w - 62, y0 + 34, x0 + w - 12, y0 + h - 26], fill=(90, 95, 100))
        for fy in range(y0 + 40, y0 + h - 30, 10):
            d.line([(x0 + w - 56, fy), (x0 + w - 18, fy)], fill=(220, 220, 120), width=2)
    elif kind == "gaza":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 214, 170))
        d.polygon([(x0 + 30, y0 + h - 20), (x0 + 62, y0 + 22), (x0 + 94, y0 + h - 20)],
                  fill=(200, 170, 120))
        d.polygon([(x0 + 96, y0 + h - 20), (x0 + 128, y0 + 30), (x0 + 160, y0 + h - 20)],
                  fill=(180, 150, 100))
        d.rectangle([x0 + 22, y0 + h - 34, x0 + 52, y0 + h - 12], fill=(150, 110, 70))
        d.rectangle([x0 + 140, y0 + h - 30, x0 + 168, y0 + h - 10], fill=(255, 255, 255))
        d.rectangle([x0 + 150, y0 + h - 26, x0 + 158, y0 + h - 14], fill=(190, 40, 40))
        d.rectangle([x0 + 144, y0 + h - 22, x0 + 164, y0 + h - 18], fill=(190, 40, 40))
    elif kind == "hormuz":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 220, 235))
        d.rectangle([x0, y0 + int(h * 0.58), x0 + w, y0 + h], fill=(70, 110, 150))
        d.polygon([(x0 + 30, y0 + 44), (x0 + 162, y0 + 44), (x0 + 150, y0 + 62),
                   (x0 + 42, y0 + 62)], fill=(40, 40, 40))
        for i in range(4):
            d.rectangle([x0 + 44 + i * 32, y0 + 28, x0 + 66 + i * 32, y0 + 44],
                        fill=(180, 60, 40))
        d.line([(x0 + 150, y0 + 44), (x0 + 158, y0 + 22)], fill=(40, 40, 40), width=3)
        for ang in range(0, 360, 30):
            import math
            ex = x0 + 158 + math.cos(math.radians(ang)) * 10
            ey = y0 + 16 + math.sin(math.radians(ang)) * 10
            d.line([(x0 + 158, y0 + 16), (ex, ey)], fill=(240, 140, 30), width=2)
        mx, my = x0 + 34, y0 + h - 16
        for ang in range(0, 360, 45):
            import math
            ex = mx + math.cos(math.radians(ang)) * 8
            ey = my + math.sin(math.radians(ang)) * 8
            d.line([(mx, my), (ex, ey)], fill=(30, 30, 30), width=2)
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(30, 30, 30))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16
    R = W - M  # right edge of content

    # ---- masthead
    d.text((W // 2, 6), "THE DAILY GLOBE", font=SERIF_B(46), fill=INK, anchor="ma")
    hline(d, M, R, 58, 3)
    d.text((M, 63), "TUESDAY 17 NOVEMBER 2026", font=SANS_B(13), fill=RED)
    d.text((W // 2, 63), "THE WORLD IN ONE PAGE", font=SANS(12), fill=GRAY, anchor="ma")
    d.text((R, 63), "No. 321  ·  PRICE: ONE DAY", font=SANS(12), fill=GRAY, anchor="ra")
    hline(d, M, R, 80, 1)

    # ---- lead story
    num, kick, head, summ, src = LEAD
    tx, tw = M, 624
    d.text((tx, 90), kick + "  ·  LEAD STORY", font=SANS_B(12), fill=RED)
    y = draw_lines(d, tx, 110, wrap(head, SERIF_B(29), tw), SERIF_B(29), leading=34)
    y += 6
    y = draw_lines(d, tx, y, wrap(summ, SERIF(14), tw), SERIF(14), leading=19)
    y += 8
    d.text((tx, y), "— " + src, font=SANS(11), fill=GRAY)
    # lead illustration
    ix, iw, iy, ih = 656, R - 656, 88, 208
    draw_bridge(d, ix, iy, iw, ih - 30)
    d.rectangle([ix, iy, ix + iw, iy + ih - 30], outline=INK, width=1)
    d.text((ix, iy + ih - 26), "A road span of the Kerch Bridge after the",
           font=SANS(10), fill=GRAY)
    d.text((ix, iy + ih - 13), "overnight strike. — Illustration",
           font=SANS(10), fill=GRAY)

    # ---- second tier
    y0 = 306
    d.text((M, y0), "ALSO TODAY", font=SANS_B(12), fill=RED)
    hline(d, M, R, y0 + 18, 1)
    kinds = ["iran", "nvidia", "asia", "gaza", "hormuz"]
    cw, gap = 192, 8
    for i, (n2, kick2, head2, summ2, src2) in enumerate(TIER):
        cx = M + i * (cw + gap)
        py = y0 + 24
        draw_tier_panel(d, cx, py, cw, 76, kinds[i])
        d.rectangle([cx, py, cx + cw, py + 76], outline=INK, width=1)
        yy = py + 82
        d.text((cx, yy), kick2, font=SANS_B(10), fill=RED)
        yy = draw_lines(d, cx, yy + 14, wrap(head2, SERIF_B(13), cw)[:2],
                        SERIF_B(13), leading=16)
        draw_lines(d, cx, yy + 2, wrap(summ2, SANS(10), cw)[:2],
                   SANS(10), leading=13)

    # ---- world map
    my0 = 492
    d.text((M, my0), "WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
    hline(d, M, R, my0 + 18, 1)
    map_x, map_y, map_w, map_h = M, my0 + 24, 700, 156
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA)
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=INK, width=1)
    xs = map_w / 360.0
    ys = map_h / 109.0
    lat_top = 77.0
    for poly in CONTINENTS:
        pts = [project(lon, lat, map_x, map_y, xs, ys, lat_top) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(120, 100, 70))
    fnum = SANS_B(10)
    for n3, place, lon, lat in MARKERS:
        px, py = project(lon, lat, map_x, map_y, xs, ys, lat_top)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(n3), font=fnum, fill=(255, 255, 255), anchor="mm")
    # legend
    lx = 724
    d.text((lx, map_y), "Numbers match the stories.", font=SANS_B(11), fill=INK)
    fleg = SANS(11)
    for i, (n3, place, lon, lat) in enumerate(MARKERS):
        col = i % 2
        row = i // 2
        ex = lx + col * 142
        ey = map_y + 22 + row * 17
        d.ellipse([ex, ey + 2, ex + 12, ey + 14], fill=RED)
        d.text((ex + 6, ey + 8), str(n3), font=SANS_B(9), fill=(255, 255, 255), anchor="mm")
        d.text((ex + 16, ey), f"{place}", font=fleg, fill=INK)

    # ---- day in brief
    ly0 = 684
    d.text((M, ly0), "THE DAY IN BRIEF  —  42 STORIES, ONE TUESDAY",
           font=SANS_B(12), fill=RED)
    hline(d, M, R, ly0 + 18, 1)
    colw, colgap = 325, 8
    item_h = 24
    for idx, (n4, head4, summ4, src4) in enumerate(BRIEF):
        col = idx // 12
        row = idx % 12
        x = M + col * (colw + colgap)
        y = ly0 + 24 + row * item_h
        d.text((x, y), trunc(f"{n4}. {head4}", SANS_B(11), colw), font=SANS_B(11), fill=INK)
        d.text((x, y + 13), trunc(summ4, SANS(10), colw), font=SANS(10), fill=GRAY)

    # ---- footer
    fy = 996
    hline(d, M, R, fy, 1)
    d.text((M, fy + 5),
           "Sources: AP · Reuters · AFP · USA Today · CNN · Kyiv Independent · Bloomberg · "
           "PANA · WHO · WFP · ECOWAS · CDC · CENTCOM",
           font=SANS(10), fill=GRAY)
    d.text((R, fy + 5), "Compiled from wire reports · 17 Nov 2026",
           font=SANS(10), fill=GRAY, anchor="ra")

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
