#!/usr/bin/env python3
"""Render the front page of THE DAILY GLOBE for Tuesday 17 November 2026.

Revision round 2. Draws a 1024x1024 broadsheet front page with PIL:
masthead, a big-numbers strip, three big leads (Kerch Bridge, Iran-US,
Quad in Manila), ten small illustrated panels, a 35-item day-in-brief
list grouped by region (48 stories in all), a world map with numbered
markers, a DATE CHECK strip naming stories deliberately left out as
pre-dated, and a sources footer.

Every story was checked against reporting from 17 November 2026.
Stories that could not be verified as 17 November news were dropped:
Depardieu, the Epstein "murder" expert claim, Eritrea trachoma,
dual quasars, the Pentagon audit, the Supreme Court UC grants, the
tRNA paper, Cabo Verde's vote (15 Nov), South Sudan's poll delay
(14 Nov), the chip-export rule (15 Nov), the Giller Prize (16 Nov),
the Akeso FDA rejection (15 Nov) and Monday's Chase/United outages.
Run: python3 render.py  ->  writes entry.png beside this file.
"""

import math
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
YELLOW = (242, 232, 190)

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
# (number, kicker, headline, summary, source, art)
LEADS = [
    (1, "UKRAINE WAR",
     "Ukraine brings down Kerch Bridge arch in overnight strike",
     "A road span collapsed into the strait early Tuesday after a "
     "seven-stage Ukrainian operation of drones and missiles. The road "
     "link is severed; rail is partly restored.",
     "AP · Reuters · Kyiv Independent", "bridge"),
    (2, "IRAN – US",
     "Iran drones target US radar in Bahrain; US jets hit back",
     "Iran fired drones at a US radar site at Sheikh Isa, Bahrain; "
     "Bahrain and CENTCOM say all were intercepted, with no damage. "
     "US jets then struck a missile site on Qeshm island.",
     "AP · Reuters · CENTCOM", "gulf"),
    (3, "ASIA",
     "Trump opens Asia trip with first Quad summit in Manila",
     "Trump met Modi, Takaichi and Albanese in Manila for the first "
     "Quad leaders' meeting in two years, then heads to Shenzhen for "
     "a first-ever trilateral with Xi and Putin.",
     "AP · Reuters", "quad"),
]

PANELS = [
    (4, "MARKETS",
     "Nvidia posts record $115.8bn quarter",
     "First report since Huang resigned; revenue +103% to $115.8bn.",
     "Nvidia · Bloomberg", "nvidia"),
    (5, "HORMUZ",
     "Fourth tanker ablaze in 24 hours",
     "Iran said a fourth tanker hit a mine; a crewman is missing.",
     "Reuters · Iran claim", "hormuz"),
    (6, "GAZA",
     "West urges Israel: open Gaza crossings",
     "Four Western states called the aid situation catastrophic.",
     "AP · WFP", "gaza"),
    (7, "RUSSIA",
     "Military plane crashes in Siberia; 19 dead",
     "An-12 came down near Yagunovo; ministry blames a fault.",
     "Reuters", "an12"),
    (8, "QUAKE",
     "M6.6 quake shakes Darwin",
     "Banda Sea tremor felt across N. Australia; no tsunami.",
     "USGS", "quake"),
    (9, "BANKS",
     "Deutsche Bank shares fall 6% on leak",
     "15m leaked files renew scrutiny of Epstein, Russia ties.",
     "Reuters · Le Monde", "bank"),
    (10, "WEATHER",
     "Cyclone Akvan bears down on India",
     "Storm in the Bay of Bengal heads for Andhra Pradesh coast.",
     "IMD", "cyclone"),
    (11, "SERBIA",
     "Students take parliament as Vučić falls",
     "Student List sworn in with 140 seats after 14 years of SNS rule.",
     "Reuters", "parliament"),
    (12, "BANGLADESH",
     "Garment workers clash over pay",
     "Police fire tear gas as thousands demand a Tk30,000 wage.",
     "AFP", "protest"),
    (13, "SPACE",
     "Voyager 1 nears one light-day",
     "NASA asks the world to flash lights tonight; milestone at dawn.",
     "NASA", "voyager"),
]

# (number, headline, summary, source) — ordered by region:
# Europe 14-20, Middle East 21-30, Asia 31-33, Africa 34-38,
# Americas 39-45, World 46-48.
BRIEF = [
    (14, "Russia hits two Kyiv bridges in reply",
     "Both crossings closed; power, water, heat cut.", "Reuters"),
    (15, "Russian drone flew over Chisinau",
     "Moldova's president said a drone crossed the capital.", "Reuters"),
    (16, "Ukraine peace talks go on, no deal",
     "Kyiv held further talks with US and European envoys.", "Reuters"),
    (17, "Kerch collapse threatens Azov grain trade",
     "Debris blocks the canal; Azov ships a quarter of Russian grain.", "Splash247"),
    (18, "UK sanctions eight settlement firms",
     "Eight settlement firms and aid-blocking Tzav 9 face asset freezes.", "gov.uk"),
    (19, "Turkey seizes opposition channel Sözcü TV",
     "Raid takes opposition channel off air; four executives detained.", "Reuters"),
    (20, "COP31 draft deal debated in Antalya",
     "Draft deal debated: fossil-fuel phaseout, $120bn aid.", "AP"),
    (21, "Israel suspends E1 settlement tender",
     "Attorney general froze the plan that would bisect the West Bank.", "Foreign Exch."),
    (22, "Knesset elects Kahana as speaker",
     "Eisenkot ally Matan Kahana elected speaker of the Knesset.", "Foreign Exch."),
    (23, "Third US carrier reaches the Gulf",
     "USS Theodore Roosevelt joins two carriers in the Middle East.", "CENTCOM"),
    (24, "Qatar–Iran talks; Iran FM in Oman",
     "Tehran says it is reviewing the latest US text, sent via Pakistan.", "Reuters"),
    (25, "Militia defies Iraq pullout deadline",
     "Kataib Hezbollah refuses to leave Jurf al-Sakhar despite an order.", "Arab News"),
    (26, "Houthis advance on Aden",
     "Government forces pull back from the Red Sea coast to defend Aden.", "AP"),
    (27, "Strike kills at least 7 in Hudaydah",
     "Houthis blame a Saudi airstrike on a sponge factory; toll unconfirmed.", "Ansarullah"),
    (28, "Gaza: 1.7m displaced, 1.4m hungry",
     "UN agencies warn of a worsening winter emergency in the Strip.", "WFP · IOM"),
    (29, "Settler mob kills woman, 72, in Jericho",
     "The killing happened overnight in the occupied West Bank.", "Foreign Exch."),
    (30, "Trump: 'dirty bomb' threat taken seriously",
     "Trump is 'looking into' claims Iran may attack Washington.", "USA Today"),
    (31, "Japan scrambles jets on Russian planes",
     "Two suspected Russian aircraft entered Japanese airspace, Tokyo says.", "AP"),
    (32, "Mongolia president quits in scandal",
     "Khurelsukh resigns amid an unproven $110m kickback claim; denies it.", "Foreign Exch."),
    (33, "Canada opens to China on steel, EVs",
     "Carney meets Xi; Canada opens doors to Chinese steel and EVs.", "CBC"),
    (34, "Rwanda hub draws UN alarm",
     "UN rights chief 'concerned'; Amnesty calls the plan 'disgraceful'.", "UN · Amnesty"),
    (35, "Gambia campaign opens for Dec 5 vote",
     "Nine candidates cleared; President Barrow seeks a third term.", "PANA"),
    (36, "Sudan drones killed 1,630+ in 2026",
     "UN: drones caused over 1,630 of 2,230 civilian deaths this year.", "Reuters"),
    (37, "Mondlane trial opens in Maputo",
     "Opposition leader on trial in Maputo; faces up to 24 years.", "Reuters"),
    (38, "AFCON: six teams book their places",
     "Morocco, Senegal, Benin, Burkina Faso, Cameroon and Mali qualify.", "Reuters"),
    (39, "NSA internal network crashes",
     "The spy agency's classified net went down; no cyberattack seen.", "CNN"),
    (40, "Measles: US loses elimination status",
     "PAHO: US, Mexico and Bolivia lose elimination status held since 2000.", "PAHO"),
    (41, "Markets slide: Dow falls 849 points",
     "S&P 500 -1.0%, Nasdaq -0.7% ahead of Nvidia's results after the bell.", "AP"),
    (42, "Bitcoin stalls below $65,000",
     "Stuck below $65,000 after a weekend slide to about $62,000.", "CoinDesk"),
    (43, "Quebec symbols-ban row grows",
     "Conservatives leave door open to PQ plan to bar pupils' symbols.", "CBC"),
    (44, "Haitians march for Bukele mission",
     "Thousands march backing Bukele's anti-gang troops; analysts warn.", "Reuters"),
    (45, "Brazil thrash Singapore 7–0",
     "Vinícius hits a hat-trick in 21 minutes in a 7–0 friendly win.", "Flashscore"),
    (46, "Gold slides as stocks fall",
     "The haven metal drops with equities as yields climb.", "FXStreet"),
    (47, "Bezos: I helped pick Pattinson as Bond",
     "Bezos says he was 'heavily involved' in picking Pattinson as 007.", "Reuters"),
    (48, "WHO: 21 nations pledge obesity cut",
     "Spain and 20 states pledge a 5% cut in obesity prevalence by 2030.", "WHO"),
]

# (big number, label)
STATS = [
    ("$115.8bn", "Nvidia revenue, +103%"),
    ("−849", "Dow points on Tuesday"),
    ("19", "killed in An-12 crash"),
    ("2,230", "Sudan civilian deaths, 2026"),
    ("16bn mi", "Voyager 1 from Earth"),
    ("5,412", "US measles cases, 2026"),
]

# (story number, place, lon, lat) — display positions nudged where stories
# cluster, so the numbered dots never sit on top of each other.
MARKERS = [
    (1, "Kerch Strait", 44.0, 44.0),
    (14, "Kyiv", 26.5, 54.0),
    (2, "Bahrain", 47.0, 23.0),
    (2, "Qeshm I.", 56.0, 31.0),
    (5, "Hormuz", 63.0, 20.0),
    (6, "Gaza", 33.0, 29.0),
    (3, "Manila", 121.0, 14.6),
    (7, "Kemerovo", 86.0, 55.5),
    (8, "Tual", 132.7, -5.6),
    (9, "Frankfurt", 6.0, 52.0),
    (10, "Bay of Bengal", 82.0, 8.0),
    (11, "Belgrade", 18.0, 43.0),
    (12, "Gazipur", 90.4, 24.0),
    (34, "Kigali", 30.0, -1.9),
]

DATE_CHECK = (
    "DATE CHECK — Left out on purpose: Ebola passed 11,000 cases on "
    "10 Nov · Cabo Verde voted on 15 Nov · S. Sudan delayed its polls "
    "on 14 Nov · the chip-export rule is from 15 Nov · Monday's Chase "
    "and United outages."
)

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


# ---------------------------------------------------------------- illustrations
# All illustrations are flat vector-style drawings. No photographs, no
# faces of real people, no text inside the artwork.

def draw_bridge(d, x0, y0, w, h):
    """Compact Kerch Bridge scene for a wide, short lead box."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(207, 224, 234))
    d.ellipse([x0 + w - 40, y0 + 4, x0 + w - 16, y0 + 28], fill=(240, 214, 130))
    for cx, cy, r in [(x0 + 30, y0 + 12, 9), (x0 + 46, y0 + 9, 11),
                      (x0 + 62, y0 + 13, 8)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    sea_y = y0 + int(h * 0.62)
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=(127, 168, 201))
    for i in range(6):
        wx = x0 + 14 + i * 52
        d.line([(wx, sea_y + 8 + (i % 2) * 5), (wx + 26, sea_y + 8 + (i % 2) * 5)],
               fill=(255, 255, 255), width=2)
    deck_y = y0 + int(h * 0.44)
    d.rectangle([x0, deck_y, x0 + int(w * 0.38), deck_y + 5], fill=(60, 60, 60))
    d.rectangle([x0 + int(w * 0.62), deck_y, x0 + w, deck_y + 5], fill=(60, 60, 60))
    for tx in (x0 + int(w * 0.17), x0 + int(w * 0.80)):
        d.rectangle([tx - 2, deck_y - 22, tx + 2, deck_y], fill=(60, 60, 60))
        d.line([(tx, deck_y - 22), (x0 + int(w * 0.38), deck_y)], fill=(90, 90, 90), width=1)
        d.line([(tx, deck_y - 22), (x0 + int(w * 0.62), deck_y)], fill=(90, 90, 90), width=1)
    d.polygon([(x0 + int(w * 0.41), deck_y + 3), (x0 + int(w * 0.59), deck_y + 3),
               (x0 + int(w * 0.55), deck_y + 18), (x0 + int(w * 0.45), deck_y + 18)],
              fill=(90, 90, 90))
    for cx, cy, r in [(x0 + int(w * 0.48), deck_y - 6, 7),
                      (x0 + int(w * 0.51), deck_y - 14, 9),
                      (x0 + int(w * 0.54), deck_y - 20, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    ex, ey = x0 + int(w * 0.50), deck_y - 1
    for ang in range(0, 360, 30):
        dx = math.cos(math.radians(ang)) * 10
        dy = math.sin(math.radians(ang)) * 10
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(230, 120, 30), width=2)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(240, 170, 40))


def draw_gulf(d, x0, y0, w, h):
    """Stylised Gulf: Iran above, Arabia below, Bahrain and Qeshm marked."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 50, 80))
    d.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + int(h * 0.30)),
               (x0 + int(w * 0.62), y0 + int(h * 0.34)),
               (x0 + int(w * 0.30), y0 + int(h * 0.26)), (x0, y0 + int(h * 0.22))],
              fill=(232, 219, 184))
    d.polygon([(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + int(h * 0.78)),
               (x0 + int(w * 0.55), y0 + int(h * 0.66)),
               (x0 + int(w * 0.22), y0 + int(h * 0.74)), (x0, y0 + int(h * 0.82))],
              fill=(232, 219, 184))
    bx, by = x0 + int(w * 0.42), y0 + int(h * 0.52)
    qx, qy = x0 + int(w * 0.58), y0 + int(h * 0.40)
    for r in (10, 18, 26):
        d.arc([bx - r, by - r, bx + r, by + r], 200, 340, fill=(90, 200, 120), width=2)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(240, 60, 60))
    d.ellipse([qx - 4, qy - 4, qx + 4, qy + 4], fill=(240, 160, 40))
    for dx, dy in [(bx + 26, by - 18), (bx + 40, by - 6), (bx + 14, by - 26)]:
        d.polygon([(dx - 5, dy), (dx + 5, dy), (dx, dy - 4)], fill=(220, 220, 220))
        d.polygon([(dx - 5, dy), (dx + 5, dy), (dx, dy + 4)], fill=(180, 180, 180))
    d.line([(qx, qy), (qx + 52, qy + 12)], fill=(255, 255, 255), width=2)
    d.polygon([(qx + 52, qy + 12), (qx + 42, qy + 8), (qx + 44, qy + 16)],
              fill=(255, 255, 255))


def draw_quad(d, x0, y0, w, h):
    """Manila skyline with four flags on poles."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(190, 214, 232))
    d.ellipse([x0 + w - 34, y0 + 4, x0 + w - 12, y0 + 26], fill=(240, 214, 130))
    for bx, bh in [(0, 20), (26, 30), (58, 24), (88, 34), (124, 22), (158, 30),
                   (196, 26), (228, 32), (262, 22), (292, 28)]:
        d.rectangle([x0 + bx, y0 + h - 12 - bh, x0 + bx + 22, y0 + h - 12],
                    fill=(90, 95, 100))
        for wy in range(y0 + h - 8 - bh, y0 + h - 14, 8):
            d.line([(x0 + bx + 4, wy), (x0 + bx + 18, wy)], fill=(220, 220, 120), width=1)
    d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(120, 130, 120))
    cols = [(178, 34, 34), (34, 80, 160), (220, 190, 60), (40, 120, 60)]
    for i, col in enumerate(cols):
        fx = x0 + 24 + i * 34
        d.line([(fx, y0 + 6), (fx, y0 + h - 12)], fill=(80, 80, 80), width=2)
        d.rectangle([fx, y0 + 8, fx + 22, y0 + 20], fill=col)


def draw_tier_panel(d, x0, y0, w, h, kind):
    """Small abstract illustration for a second-tier story."""
    if kind == "nvidia":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 42, 28))
        cx, cy = x0 + 34, y0 + h // 2
        d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(46, 160, 67))
        d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=(16, 42, 28))
        for i in range(-1, 2):
            d.line([(cx + i * 11, cy - 22), (cx + i * 11, cy - 16)], fill=(200, 220, 200), width=2)
            d.line([(cx + i * 11, cy + 16), (cx + i * 11, cy + 22)], fill=(200, 220, 200), width=2)
            d.line([(cx - 22, cy + i * 11), (cx - 16, cy + i * 11)], fill=(200, 220, 200), width=2)
            d.line([(cx + 16, cy + i * 11), (cx + 22, cy + i * 11)], fill=(200, 220, 200), width=2)
        pts = [(x0 + 66, y0 + h - 8), (x0 + 92, y0 + h - 22), (x0 + 112, y0 + h - 16),
               (x0 + 136, y0 + h - 30), (x0 + 160, y0 + h - 34)]
        d.line(pts, fill=(120, 220, 140), width=3, joint="curve")
        d.polygon([(x0 + 160, y0 + h - 34), (x0 + 150, y0 + h - 32), (x0 + 158, y0 + h - 24)],
                  fill=(120, 220, 140))
    elif kind == "gaza":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 214, 170))
        d.polygon([(x0 + 22, y0 + h - 8), (x0 + 48, y0 + 10), (x0 + 74, y0 + h - 8)],
                  fill=(200, 170, 120))
        d.polygon([(x0 + 76, y0 + h - 8), (x0 + 102, y0 + 14), (x0 + 128, y0 + h - 8)],
                  fill=(180, 150, 100))
        d.rectangle([x0 + 16, y0 + h - 16, x0 + 38, y0 + h - 4], fill=(150, 110, 70))
        d.rectangle([x0 + 140, y0 + h - 14, x0 + 164, y0 + h - 4], fill=(255, 255, 255))
        d.rectangle([x0 + 148, y0 + h - 12, x0 + 154, y0 + h - 6], fill=(190, 40, 40))
        d.rectangle([x0 + 143, y0 + h - 10, x0 + 161, y0 + h - 8], fill=(190, 40, 40))
    elif kind == "hormuz":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 220, 235))
        d.rectangle([x0, y0 + int(h * 0.58), x0 + w, y0 + h], fill=(70, 110, 150))
        d.polygon([(x0 + 24, y0 + 20), (x0 + 164, y0 + 20), (x0 + 152, y0 + 30),
                   (x0 + 36, y0 + 30)], fill=(40, 40, 40))
        for i in range(4):
            d.rectangle([x0 + 38 + i * 32, y0 + 10, x0 + 58 + i * 32, y0 + 20],
                        fill=(180, 60, 40))
        d.line([(x0 + 152, y0 + 20), (x0 + 160, y0 + 8)], fill=(40, 40, 40), width=3)
        for ang in range(0, 360, 30):
            ex = x0 + 160 + math.cos(math.radians(ang)) * 8
            ey = y0 + 5 + math.sin(math.radians(ang)) * 8
            d.line([(x0 + 160, y0 + 5), (ex, ey)], fill=(240, 140, 30), width=2)
        mx, my = x0 + 28, y0 + h - 8
        for ang in range(0, 360, 45):
            ex = mx + math.cos(math.radians(ang)) * 6
            ey = my + math.sin(math.radians(ang)) * 6
            d.line([(mx, my), (ex, ey)], fill=(30, 30, 30), width=2)
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(30, 30, 30))


def draw_an12(d, x0, y0, w, h):
    """Military transport plane over snowy ground, smoke trail behind."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 220, 235))
    for cx, cy, r in [(x0 + 24, y0 + 8, 7), (x0 + 36, y0 + 6, 9), (x0 + 48, y0 + 9, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    d.rectangle([x0, y0 + int(h * 0.72), x0 + w, y0 + h], fill=(240, 242, 245))
    for tx in (x0 + 16, x0 + 168):
        d.polygon([(tx, y0 + h - 4), (tx + 6, y0 + int(h * 0.72) - 10),
                   (tx + 12, y0 + h - 4)], fill=(60, 90, 60))
    for cx, cy, r in [(x0 + 62, y0 + 16, 5), (x0 + 74, y0 + 13, 7), (x0 + 88, y0 + 15, 5)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 140, 140))
    px, py = x0 + 118, y0 + 18
    d.polygon([(px - 34, py), (px + 30, py - 2), (px + 40, py + 2),
               (px + 30, py + 6), (px - 34, py + 5)], fill=(70, 70, 70))
    d.polygon([(px - 6, py), (px + 8, py - 12), (px + 16, py - 12), (px + 10, py)],
              fill=(90, 90, 90))
    d.polygon([(px - 26, py + 5), (px - 14, py + 14), (px - 6, py + 14), (px - 14, py + 5)],
              fill=(90, 90, 90))
    d.polygon([(px + 30, py - 2), (px + 40, py - 10), (px + 44, py - 10),
               (px + 38, py + 1)], fill=(90, 90, 90))
    d.ellipse([px + 28, py - 1, px + 36, py + 4], fill=(180, 220, 240))


def draw_quake(d, x0, y0, w, h):
    """Seismograph trace on a paper strip above cracked ground."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(235, 228, 210))
    d.rectangle([x0 + 6, y0 + 4, x0 + w - 6, y0 + int(h * 0.52)], fill=(255, 255, 255))
    mid = y0 + int(h * 0.28)
    pts = []
    for i in range(31):
        px = x0 + 10 + i * 6
        amp = 2 if i % 5 else (9 if 10 <= i <= 20 else 4)
        py = mid + (amp if i % 2 else -amp)
        pts.append((px, py))
    d.line(pts, fill=(30, 30, 30), width=2, joint="curve")
    gy = y0 + int(h * 0.62)
    d.rectangle([x0, gy, x0 + w, y0 + h], fill=(150, 110, 70))
    d.line([(x0 + 60, gy), (x0 + 66, y0 + h - 4)], fill=(60, 40, 20), width=2)
    d.line([(x0 + 66, y0 + int(h * 0.80)), (x0 + 78, y0 + int(h * 0.88))],
           fill=(60, 40, 20), width=2)
    d.line([(x0 + 120, gy), (x0 + 114, y0 + h - 6)], fill=(60, 40, 20), width=2)
    bx, by = x0 + 140, gy - 12
    d.polygon([(bx, by), (bx + 26, by), (bx + 24, by + 12), (bx + 2, by + 12)],
              fill=(200, 200, 200))
    d.rectangle([bx + 4, by + 3, bx + 10, by + 8], fill=(90, 130, 180))
    d.rectangle([bx + 16, by + 3, bx + 22, by + 8], fill=(90, 130, 180))


def draw_bank(d, x0, y0, w, h):
    """Bank building with columns, falling chart and scattered files."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 42, 70))
    bx, by = x0 + 14, y0 + 8
    d.polygon([(bx, by), (bx + 62, by), (bx + 31, by + 12)], fill=(200, 200, 200))
    d.rectangle([bx + 4, by + 12, bx + 58, by + 16], fill=(220, 220, 220))
    for i in range(4):
        d.rectangle([bx + 8 + i * 14, by + 16, bx + 14 + i * 14, y0 + h - 8],
                    fill=(220, 220, 220))
    d.rectangle([bx, y0 + h - 8, bx + 62, y0 + h - 4], fill=(200, 200, 200))
    for sx, sy, a in [(x0 + 92, y0 + 8, 8), (x0 + 116, y0 + 16, -10), (x0 + 104, y0 + 26, 5)]:
        d.rectangle([sx, sy, sx + 18, sy + 12], fill=(255, 255, 255))
        d.line([(sx + 3, sy + 4), (sx + 15, sy + 4)], fill=(150, 150, 150), width=1)
        d.line([(sx + 3, sy + 8), (sx + 12, sy + 8)], fill=(150, 150, 150), width=1)
    pts = [(x0 + 140, y0 + 8), (x0 + 154, y0 + 18), (x0 + 168, y0 + 14),
           (x0 + 182, y0 + 30)]
    d.line(pts, fill=(240, 60, 60), width=3, joint="curve")
    d.polygon([(x0 + 182, y0 + 30), (x0 + 172, y0 + 28), (x0 + 180, y0 + 20)],
              fill=(240, 60, 60))


def draw_cyclone(d, x0, y0, w, h):
    """Cyclone spiral over the sea, rain slanting in."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(210, 225, 235))
    cx, cy = x0 + 62, y0 + h // 2 + 2
    for r in (8, 15, 22, 29):
        d.arc([cx - r, cy - r, cx + r, cy + r], 40, 330, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(90, 110, 140))
    for rx in range(x0 + 110, x0 + w - 6, 14):
        d.line([(rx, y0 + 6), (rx - 4, y0 + 16)], fill=(140, 160, 180), width=2)
        d.line([(rx, y0 + 22), (rx - 4, y0 + 32)], fill=(140, 160, 180), width=2)
    d.rectangle([x0, y0 + int(h * 0.78), x0 + w, y0 + h], fill=(70, 110, 150))
    for i in range(4):
        wx = x0 + 12 + i * 46
        d.line([(wx, y0 + h - 6), (wx + 22, y0 + h - 6)], fill=(255, 255, 255), width=2)


def draw_parliament(d, x0, y0, w, h):
    """Parliament building with dome and a crowd below."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(220, 210, 180))
    bx = x0 + 52
    d.rectangle([bx, y0 + 16, bx + 88, y0 + h - 8], fill=(240, 236, 220))
    d.pieslice([bx + 28, y0 - 2, bx + 60, y0 + 22], 180, 360, fill=(120, 60, 60))
    d.rectangle([bx + 42, y0 - 6, bx + 46, y0 + 2], fill=(120, 60, 60))
    for i in range(5):
        d.rectangle([bx + 8 + i * 16, y0 + 18, bx + 13 + i * 16, y0 + h - 8],
                    fill=(200, 192, 170))
    d.rectangle([bx, y0 + h - 8, bx + 88, y0 + h - 4], fill=(180, 170, 150))
    for i in range(9):
        hx = x0 + 14 + i * 9
        d.ellipse([hx, y0 + h - 14, hx + 6, y0 + h - 8], fill=(60, 60, 60))
    for i in range(8):
        hx = x0 + 150 + i * 5
        d.ellipse([hx, y0 + h - 12, hx + 4, y0 + h - 8], fill=(60, 60, 60))
    for fx, col in [(x0 + 8, (178, 34, 34)), (x0 + w - 16, (34, 80, 160))]:
        d.line([(fx, y0 + 4), (fx, y0 + 22)], fill=(80, 80, 80), width=2)
        d.rectangle([fx, y0 + 5, fx + 12, y0 + 12], fill=col)


def draw_protest(d, x0, y0, w, h):
    """Street crowd with placards and a puff of tear gas."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 205, 210))
    d.rectangle([x0, y0 + int(h * 0.68), x0 + w, y0 + h], fill=(120, 120, 120))
    for i in range(10):
        hx = x0 + 10 + i * 15
        d.ellipse([hx, y0 + int(h * 0.42), hx + 8, y0 + int(h * 0.42) + 8],
                  fill=(60, 60, 60))
        d.rectangle([hx + 1, y0 + int(h * 0.42) + 8, hx + 7, y0 + int(h * 0.66)],
                    fill=(90, 90, 120))
    for px, py in [(x0 + 30, y0 + 6), (x0 + 86, y0 + 2), (x0 + 130, y0 + 8)]:
        d.line([(px + 6, py + 10), (px + 6, y0 + int(h * 0.42))], fill=(80, 80, 80), width=2)
        d.rectangle([px, py, px + 20, py + 10], fill=(255, 255, 255))
        d.line([(px + 3, py + 5), (px + 17, py + 5)], fill=(190, 40, 40), width=2)
    for cx, cy, r in [(x0 + 168, y0 + 14, 8), (x0 + 176, y0 + 8, 10), (x0 + 182, y0 + 18, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 170, 170))


def draw_voyager(d, x0, y0, w, h):
    """Voyager 1 probe against the stars, signal arcing home."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 10, 25))
    for sx, sy, r in [(12, 6, 1), (34, 12, 1), (58, 5, 1), (84, 10, 1),
                      (110, 6, 1), (140, 12, 1), (168, 5, 1), (24, 24, 1),
                      (96, 26, 1), (150, 26, 1), (180, 22, 1), (70, 32, 1)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(255, 255, 255))
    px, py = x0 + 118, y0 + 16
    d.polygon([(px - 6, py), (px + 6, py), (px + 14, py - 10), (px + 2, py - 12)],
              fill=(220, 190, 90))
    d.rectangle([px - 10, py, px + 2, py + 6], fill=(200, 200, 200))
    d.line([(px - 10, py + 3), (px - 26, py + 3)], fill=(200, 200, 200), width=2)
    d.line([(px + 2, py - 12), (px + 10, py - 20)], fill=(200, 200, 200), width=2)
    d.ellipse([px + 8, py - 22, px + 12, py - 18], fill=(240, 200, 80))
    for r in (14, 22, 30):
        d.arc([px - r, py - r, px + r, py + r], 200, 340, fill=(90, 200, 120), width=2)
    d.ellipse([x0 + 2, y0 + h - 20, x0 + 26, y0 + h - 2], fill=(40, 90, 160))
    d.ellipse([x0 + 5, y0 + h - 17, x0 + 23, y0 + h - 5], fill=(70, 130, 190))


PANEL_ART = {
    "nvidia": lambda d, x, y, w, h: draw_tier_panel(d, x, y, w, h, "nvidia"),
    "gaza": lambda d, x, y, w, h: draw_tier_panel(d, x, y, w, h, "gaza"),
    "hormuz": lambda d, x, y, w, h: draw_tier_panel(d, x, y, w, h, "hormuz"),
    "an12": draw_an12,
    "quake": draw_quake,
    "bank": draw_bank,
    "cyclone": draw_cyclone,
    "parliament": draw_parliament,
    "protest": draw_protest,
    "voyager": draw_voyager,
}

LEAD_ART = {"bridge": draw_bridge, "gulf": draw_gulf, "quad": draw_quad}


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

    # ---- big-numbers strip
    sw, sgap = 158, 8
    for i, (num, lab) in enumerate(STATS):
        sx = M + i * (sw + sgap)
        d.text((sx, 86), num, font=SANS_B(15), fill=RED)
        draw_lines(d, sx, 105, wrap(lab, SANS(9), sw), SANS(9), fill=GRAY, leading=11)
    hline(d, M, R, 118, 1)

    # ---- three big leads
    lw, lgap = 320, 16
    for i, (n, kick, head, summ, src, art) in enumerate(LEADS):
        cx = M + i * (lw + lgap)
        d.text((cx, 122), kick + "  ·  LEAD STORY", font=SANS_B(11), fill=RED)
        y = draw_lines(d, cx, 138, wrap(head, SERIF_B(19), lw)[:3],
                       SERIF_B(19), leading=23)
        y = draw_lines(d, cx, y + 4, wrap(summ, SERIF(13), lw)[:4],
                       SERIF(13), leading=16)
        iy = y + 6
        LEAD_ART[art](d, cx, iy, lw, 58)
        d.rectangle([cx, iy, cx + lw, iy + 58], outline=INK, width=1)

    # ---- ten small illustrated panels
    d.text((M, 341), "MORE OF THE DAY — TEN STORIES IN PICTURES",
           font=SANS_B(11), fill=RED)
    pw, pgap = 192, 8
    for i, (n2, kick2, head2, summ2, src2, art2) in enumerate(PANELS):
        col, row = i % 5, i // 5
        cx = M + col * (pw + pgap)
        py = 355 + row * 106
        PANEL_ART[art2](d, cx, py, pw, 40)
        d.rectangle([cx, py, cx + pw, py + 40], outline=INK, width=1)
        d.text((cx, py + 43), kick2, font=SANS_B(9), fill=RED)
        draw_lines(d, cx, py + 55, wrap(head2, SERIF_B(12), pw)[:2],
                   SERIF_B(12), leading=13)
        draw_lines(d, cx, py + 82, wrap(summ2, SANS(9), pw)[:2],
                   SANS(9), leading=10)

    # ---- day in brief
    ly0 = 569
    d.text((M, ly0), "THE DAY IN BRIEF  —  48 STORIES, ONE TUESDAY  ·  "
                     "EUROPE · MIDDLE EAST · ASIA · AFRICA · AMERICAS · WORLD",
           font=SANS_B(11), fill=RED)
    hline(d, M, R, ly0 + 16, 1)
    colw, colgap = 325, 8
    item_h = 23
    for idx, (n4, head4, summ4, src4) in enumerate(BRIEF):
        col = idx // 12
        row = idx % 12
        x = M + col * (colw + colgap)
        y = ly0 + 22 + row * item_h
        d.text((x, y), trunc(f"{n4}. {head4}", SANS_B(10), colw),
               font=SANS_B(10), fill=INK)
        d.text((x, y + 12), trunc(summ4, SANS(9), colw), font=SANS(9), fill=GRAY)

    # ---- world map
    my0 = 865
    d.text((M, my0), "WHERE IT HAPPENED", font=SANS_B(11), fill=RED)
    hline(d, M, R, my0 + 15, 1)
    map_x, map_y, map_w, map_h = M, 881, 560, 119
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA)
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=INK, width=1)
    xs = map_w / 360.0
    ys = map_h / 109.0
    lat_top = 77.0
    for poly in CONTINENTS:
        pts = [project(lon, lat, map_x, map_y, xs, ys, lat_top) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(120, 100, 70))
    fnum = SANS_B(9)
    for n3, place, lon, lat in MARKERS:
        px, py = project(lon, lat, map_x, map_y, xs, ys, lat_top)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(n3), font=fnum, fill=(255, 255, 255), anchor="mm")
    # legend: three columns of places
    lx0, lx1, lx2, lx3 = 592, 700, 808, 916
    d.text((lx0, map_y), "Numbers match the stories.", font=SANS_B(10), fill=INK)
    for i, (n3, place, lon, lat) in enumerate(MARKERS):
        col = i // 4
        row = i % 4
        ex = [lx0, lx1, lx2, lx3][col]
        ey = map_y + 20 + row * 13
        d.ellipse([ex, ey + 1, ex + 11, ey + 12], fill=RED)
        d.text((ex + 5, ey + 6), str(n3), font=SANS_B(8), fill=(255, 255, 255), anchor="mm")
        d.text((ex + 15, ey), place, font=SANS(9), fill=INK)
    # DATE CHECK box under the legend
    bx0, by0, bx1, by1 = 592, 954, R, 1000
    d.rectangle([bx0, by0, bx1, by1], fill=YELLOW, outline=RULE, width=1)
    draw_lines(d, bx0 + 6, by0 + 4, wrap(DATE_CHECK, SANS(9), bx1 - bx0 - 12),
               SANS(9), fill=INK, leading=12)

    # ---- footer
    fy = 1004
    hline(d, M, R, fy, 1)
    d.text((M, fy + 4),
           "Sources: AP · Reuters · AFP · USA Today · CNN · Kyiv Independent · "
           "Bloomberg · PANA · WHO · WFP · CDC · CENTCOM · gov.uk · NASA · USGS · "
           "Le Monde · NYT · FT",
           font=SANS(9), fill=GRAY)
    d.text((R, fy + 4), "Compiled from wire reports · 17 Nov 2026",
           font=SANS(9), fill=GRAY, anchor="ra")

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
