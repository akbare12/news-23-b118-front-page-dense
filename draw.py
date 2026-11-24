#!/usr/bin/env python3
"""news-23 b118 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page: masthead, number strip, region bar, 3 hero scenes,
10 cards, world map + ALSO list, DATE CHECK box, footer. All 31 stories dated
23 Nov 2026. Drawn with PIL; output entry.png (<=1 MiB)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# palette
CREAM = (250, 246, 235)
BLACK = (12, 12, 12)
RED = (178, 24, 28)
DARKRED = (140, 18, 22)
GOLD = (201, 162, 39)
GOLD_LT = (226, 190, 90)
NAVY = (20, 38, 74)
GREEN = (29, 107, 52)
TEAL = (18, 110, 105)
PURPLE = (96, 62, 140)
GRAY = (90, 90, 90)
DARKGRAY = (70, 70, 70)
MAPGREEN = (196, 222, 178)
MAPGREEN2 = (178, 212, 158)
CHIP_BG = (30, 60, 130)
CHIP_CLAIM = (178, 24, 28)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def text(x, y, s, f, fill, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(s, f, maxw):
    """Greedy word wrap; returns list of lines fitting maxw."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, claim=False):
    """Small REPORTED/CLAIM chip; returns right edge x."""
    f = font(SANSB, 8)
    w_ = int(d.textlength(label, font=f)) + 10
    h_ = 13
    d.rounded_rectangle([x, y, x + w_, y + h_], radius=2,
                        fill=CHIP_CLAIM if claim else CHIP_BG)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return x + w_

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 58], fill=BLACK)
text(16, 7, "THE WORLD TODAY", font(SERIF, 44), (255, 255, 255))
text(1008, 20, "MONDAY 23 NOVEMBER 2026", font(SANSB, 16), GOLD, anchor="ra")

# ---------------------------------------------------------------- kicker
d.rectangle([0, 58, W, 80], fill=RED)
text(512, 64, "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
     font(SANSB, 13), (255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- number strip (5 cols x 2 rows)
NUMBERS = [
    [("\u22123.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
     ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS")],
    [("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
     ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO")],
]
strip_y0, strip_y1 = 80, 150
col_w = W // 5
for r, row in enumerate(NUMBERS):
    ry = strip_y0 + r * 35
    for c, (val, lab) in enumerate(row):
        cx = c * col_w + 12
        text(cx, ry + 3, val, font(SANSB, 19), BLACK)
        text(cx, ry + 25, lab, font(SANS, 8), DARKGRAY)
d.line([0, strip_y1, W, strip_y1], fill=(200, 190, 170), width=1)

# ---------------------------------------------------------------- region bar
REGIONS = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", TEAL),
           ("EUROPE 5", PURPLE), ("AFRICA 3", (46, 125, 60)), ("WORLD 2", (60, 60, 60))]
seg_w = W // 6
for i, (lab, col) in enumerate(REGIONS):
    x0 = i * seg_w
    d.rectangle([x0, 150, x0 + seg_w, 172], fill=col)
    text(x0 + seg_w // 2, 156, lab, font(SANSB, 10), (255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- UTC strip
d.rectangle([0, 172, W, 188], fill=(235, 228, 210))
text(10, 176, "THE DAY IN UTC   ~00:00 Kospi dives   ·   ~05:30 Guterres opens   ·   ~09:00 Power Index   ·   ~12:00 Paris 2% tax   ·   ~15:00 Kyiv missiles",
     font(SANS, 9), DARKGRAY)
text(1014, 176, "~ APPROX", font(SANS, 9), GRAY, anchor="ra")

# ---------------------------------------------------------------- hero scenes
HX = [8, 346, 684]          # hero column x0
HW = 330                    # hero column width
SY0, SY1 = 188, 296         # scene y range

def hero_scene_kospi(x0):
    d.rectangle([x0, SY0, x0 + HW, SY1], fill=NAVY)
    # buildings with lit windows along the bottom
    import random
    rnd = random.Random(23)
    bx = x0 + 10
    while bx < x0 + HW - 30:
        bw = rnd.randint(22, 40)
        bh = rnd.randint(28, 52)
        by = SY1 - 18 - bh
        d.rectangle([bx, by, bx + bw, SY1 - 18], fill=(24, 48, 92))
        for wy in range(by + 5, SY1 - 22, 9):
            for wx in range(bx + 4, bx + bw - 4, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 214, 110))
        bx += bw + 4
    # orange descending chart line, kept below the big number
    pts = [(x0 + 130, SY0 + 62), (x0 + 165, SY0 + 70), (x0 + 200, SY0 + 66),
           (x0 + 235, SY0 + 78), (x0 + 270, SY0 + 84), (x0 + 305, SY0 + 92)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    text(x0 + 10, SY0 + 6, "\u22123.3%", font(SANSB, 30), (255, 255, 255))
    text(x0 + 10, SY0 + 88, "KOSPI 4,708.54  ·  \u2212161 PTS", font(SANSB, 9), (255, 255, 255))

def hero_scene_guterres(x0):
    d.rectangle([x0, SY0, x0 + HW, SY1], fill=GREEN)
    # globe, right side
    cx, cy, r = x0 + 258, SY0 + 54, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 230, 190))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 180, 120), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 180, 120), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 180, 120), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(120, 180, 120), width=1)
    text(x0 + 12, SY0 + 6, "150", font(SANSB, 44), GOLD_LT)
    for j, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
        text(x0 + 12, SY0 + 52 + j * 17, ln, font(SANSB, 17), GOLD_LT)
    # (source "UNITED NATIONS" lives in the headline block below the scene,
    # so no in-scene caption here — it used to collide with "FRAMEWORK".)

def hero_scene_power(x0):
    d.rectangle([x0, SY0, x0 + HW, SY1], fill=(244, 238, 222))
    text(x0 + 10, SY0 + 4, "NARROWEST SINCE 2018", font(SANSB, 10), BLACK)
    text(x0 + HW - 10, SY0 + 4, "GAP 5.3", font(SANSB, 10), RED, anchor="ra")
    bars = [("US", 78.9, NAVY, 44), ("CHINA", 73.6, RED, 41), ("INDIA", 40.5, GOLD, 23)]
    bw = 74
    gap = (HW - 3 * bw - 20) // 4
    base = SY0 + 96
    for i, (lab, val, col, bh) in enumerate(bars):
        bx = x0 + 10 + gap + i * (bw + gap)
        text(bx + bw // 2, SY0 + 26, f"{val}", font(SANSB, 15), BLACK, anchor="ma")
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        text(bx + bw // 2, base - 14, lab, font(SANSB, 9), (255, 255, 255), anchor="ma")

hero_scene_kospi(HX[0])
hero_scene_guterres(HX[1])
hero_scene_power(HX[2])

# ---------------------------------------------------------------- hero text blocks
HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi closes \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(HEROES):
    x0 = HX[i]
    lines = wrap(head, font(SANSB, 15), HW - 4)
    y = 302
    for ln in lines[:2]:
        text(x0, y, ln, font(SANSB, 15), BLACK)
        y += 17
    blines = wrap(body, font(SANS, 10), HW - 4)
    y = 342
    for ln in blines[:2]:
        text(x0, y, ln, font(SANS, 10), DARKGRAY)
        y += 12
    text(x0, 398, src, font(SANS, 8), GRAY)
    chip(x0 + HW - 62, 396, "REPORTED")

# ---------------------------------------------------------------- MORE OF THE DAY strip
d.rectangle([0, 420, W, 442], fill=BLACK)
text(10, 426, "MORE OF THE DAY  \u2014  10 STORIES", font(SANSB, 13), (255, 255, 255))

# ---------------------------------------------------------------- cards (2 rows x 5 cols)
CARDS = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", False),
    ("AMERICAS", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", False),
    ("WHITE HOUSE", (120, 70, 20), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", False),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", False),
    ("SPORT", GOLD, "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", False),
    ("SPORT", GOLD, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", False),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", False),
    ("TECH", (30, 90, 160), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", False),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", True),
    ("SPACE", (60, 60, 60), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", True),
]
CW, CG = 195, 8
for idx, (cat, ccol, head, body, src, claim) in enumerate(CARDS):
    row, col = divmod(idx, 5)
    x0 = 8 + col * (CW + CG)
    y0 = 446 + row * 66
    d.rectangle([x0, y0, x0 + CW, y0 + 62], outline=(210, 200, 180), width=1)
    text(x0 + 5, y0 + 4, cat, font(SANSB, 7), ccol)
    text(x0 + CW - 5, y0 + 4, str(idx + 1), font(SANSB, 9), RED, anchor="ra")
    hlines = wrap(head, font(SANSB, 10), CW - 10)
    y = y0 + 17
    for ln in hlines[:2]:
        text(x0 + 5, y, ln, font(SANSB, 10), BLACK)
        y += 11
    text(x0 + 5, y0 + 41, body, font(SANS, 9), DARKGRAY)
    text(x0 + 5, y0 + 52, src, font(SANS, 8), GRAY)
    chip(x0 + CW - 62, y0 + 50, "CLAIM" if claim else "REPORTED", claim=claim)

# ---------------------------------------------------------------- WHERE IT HAPPENED strip
d.rectangle([0, 580, W, 602], fill=BLACK)
text(10, 586, "WHERE IT HAPPENED", font(SANSB, 13), (255, 255, 255))

# ---------------------------------------------------------------- map (left column x 8..330)
MAPX0, MAPX1 = 8, 330
MAPY0, MAPY1 = 606, 794
# stylised continents
d.polygon([(24, 612), (90, 606), (150, 618), (158, 660), (140, 700), (110, 712),
           (70, 700), (30, 668), (18, 640)], fill=MAPGREEN)          # N America
d.polygon([(60, 712), (95, 716), (105, 760), (88, 800), (66, 795), (52, 750)],
          fill=MAPGREEN)                                              # S America
d.polygon([(180, 612), (240, 606), (300, 614), (326, 640), (322, 700), (300, 745),
           (270, 775), (220, 770), (185, 730), (172, 680), (176, 640)], fill=MAPGREEN2)  # Eurasia/Africa
PINS = {1: (315, 650), 2: (70, 782), 3: (305, 630), 4: (60, 690), 5: (85, 665),
        6: (270, 660), 7: (235, 672), 8: (225, 655), 9: (255, 645), 10: (215, 640),
        11: (275, 700), 12: (265, 720), 13: (250, 745)}
for n, (px, py) in PINS.items():
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    text(px, py - 4, str(n), font(SANSB, 8), (255, 255, 255), anchor="ma")
# legend, 4 short rows inside the map column
LEGEND = ["Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
          "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris",
          "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut",
          "12 Gaza \u00b7 13 Khartoum"]
for j, ln in enumerate(LEGEND):
    text(MAPX0 + 2, 800 + j * 10, ln, font(SANS, 8), DARKGRAY)

# ---------------------------------------------------------------- ALSO list (right, 2 cols x 9)
ALSO_A = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
]
ALSO_B = [
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe",
    "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom \u22127.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
text(340, 606, "ALSO ON MONDAY", font(SANSB, 12), BLACK)
for i, item in enumerate(ALSO_A):
    text(340, 628 + i * 24, item, font(SANS, 10), BLACK)
for i, item in enumerate(ALSO_B):
    text(680, 628 + i * 24, item, font(SANS, 10), BLACK)
    if i in (1, 2):
        text(680 + int(d.textlength(item, font=font(SANS, 10))) + 6, 628 + i * 24,
             "[CLAIM]", font(SANSB, 9), RED)

# ---------------------------------------------------------------- DATE CHECK box
BOX = [8, 838, 1016, 918]
d.rectangle(BOX, outline=RED, width=2)
text(16, 844, "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
     font(SANSB, 11), RED)
text(16, 864, "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov)",
     font(SANS, 9), BLACK)
text(16, 878, "EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
     font(SANS, 9), BLACK)
text(16, 896, "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
     font(SANS, 9), BLACK)

# ---------------------------------------------------------------- footer
text(10, 926, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     font(SANS, 8), GRAY)
text(10, 940, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing.",
     font(SANS, 8), GRAY)
text(10, 954, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     font(SANS, 8), GRAY)
text(512, 972, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     font(SANSB, 12), GOLD, anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
