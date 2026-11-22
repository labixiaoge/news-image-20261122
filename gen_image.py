#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: a newspaper front page summing up
Sunday 22 November 2026 in five stories, all drawn with PIL primitives.

Stories (all checked against the morning news of 22 Nov 2026 — BBC,
Times of India, ARY News, Daily Jagran, pw.live school-assembly digest):
  1. Iran strikes a US air base in Kuwait and targets Bahrain as the
     Gulf war widens; tankers hit off Oman; Trump says an Iran deal
     could last 20 years and eyes "ultimate regime change".
  2. Russia's war: 400 drones and 110 missiles hit Ukraine; Russian
     missiles crash in Poland and NATO jets scramble; drones hit a
     Russian cargo ship in the Baltic and Finland tightens security.
  3. COP31 climate talks deadlocked over fossil fuels (BBC).
  4. Magnitude 6.9 earthquake shakes Peru's Andes; no damage or
     casualties immediately reported.
  5. Mexican cartel boss "El Chapo Isidro" arrested in a special
     forces raid; deadly violence erupts in Sinaloa, 11 killed.

Run:  python3 gen_image.py   (writes entry.png next to this file)
Deterministic: fixed random seed, no timestamps, no network.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (176, 42, 42)
GREY = (120, 116, 108)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def vgrad(d, box, c_top, c_bot):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        d.line([(x0, y), (x1, y)], fill=lerp(c_top, c_bot, (y - y0) / span))


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def burst(d, cx, cy, r, rng):
    """Explosion burst: orange star, yellow core, sparks."""
    d.polygon(star_points(cx, cy, r, r * 0.42, 8), fill=(232, 116, 24))
    d.polygon(star_points(cx, cy, r * 0.62, r * 0.28, 8, rot=-60),
              fill=(245, 178, 44))
    d.ellipse([cx - r * 0.30, cy - r * 0.30, cx + r * 0.30, cy + r * 0.30],
              fill=(255, 224, 130))
    for _ in range(7):
        a = rng.uniform(0, 2 * math.pi)
        r1 = r * rng.uniform(0.9, 1.15)
        r2 = r * rng.uniform(1.25, 1.6)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(255, 200, 90), width=3)


def draw_gulf(d, box, rng):
    """Night over a Gulf air base: missile streaks, interceptor bursts,
    control tower and jets on the runway below."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (12, 16, 40), (52, 40, 74))
    # stars
    for _ in range(26):
        sx, sy = rng.uniform(x0 + 6, x1 - 6), rng.uniform(y0 + 6, y0 + 120)
        r = rng.uniform(0.8, 2.0)
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(220, 225, 240))
    # crescent moon
    d.ellipse([x1 - 58, y0 + 12, x1 - 26, y0 + 44], fill=(250, 240, 205))
    d.ellipse([x1 - 50, y0 + 9, x1 - 20, y0 + 41], fill=(24, 26, 52))
    # incoming missile streaks (downward) and interceptor streaks (upward)
    for (mx, my, ln, ang) in [(x0 + 70, y0 + 26, 96, 62),
                              (x0 + 250, y0 + 12, 110, 58),
                              (x0 + 360, y0 + 40, 80, 66)]:
        dx, dy = ln * math.cos(math.radians(ang)), ln * math.sin(math.radians(ang))
        d.line([(mx, my), (mx + dx, my + dy)], fill=(255, 214, 120), width=4)
        d.ellipse([mx + dx - 6, my + dy - 6, mx + dx + 6, my + dy + 6],
                  fill=(255, 236, 160))
    for (mx, my, ln, ang) in [(x0 + 120, y1 - 120, 90, -58),
                              (x0 + 300, y1 - 110, 100, -62)]:
        dx, dy = ln * math.cos(math.radians(ang)), ln * math.sin(math.radians(ang))
        d.line([(mx, my), (mx + dx, my + dy)], fill=(150, 200, 255), width=3)
    burst(d, x0 + 330, y0 + 96, 30, rng)
    burst(d, x0 + 130, y0 + 132, 22, rng)
    # ground: air base
    gy = y0 + int((y1 - y0) * 0.74)
    d.rectangle([x0, gy, x1, y1], fill=(38, 34, 44))
    # control tower
    tx = x0 + 60
    d.rectangle([tx, gy - 62, tx + 26, gy], fill=(70, 68, 80))
    d.rectangle([tx - 6, gy - 78, tx + 32, gy - 62], fill=(96, 92, 104))
    d.rectangle([tx - 2, gy - 74, tx + 28, gy - 66], fill=(255, 206, 92))
    # hangar
    hx = x0 + 250
    d.pieslice([hx, gy - 56, hx + 150, gy + 20], start=180, end=360,
               fill=(88, 84, 96))
    d.rectangle([hx + 20, gy - 8, hx + 130, gy], fill=(52, 50, 60))
    # runway lights
    for i in range(9):
        lx = x0 + 20 + i * 46
        d.ellipse([lx - 3, y1 - 14, lx + 3, y1 - 8], fill=(255, 220, 120))
    # parked jet silhouette
    jx, jy = x0 + 150, gy - 16
    d.polygon([(jx, jy), (jx + 46, jy - 6), (jx + 66, jy), (jx + 46, jy + 6)],
              fill=(20, 20, 26))
    d.polygon([(jx + 20, jy - 4), (jx + 34, jy - 18), (jx + 40, jy - 4)],
              fill=(20, 20, 26))


def draw_poland(d, box, rng):
    """Dawn over flat fields: a missile falls with a smoke trail while a
    NATO jet climbs away; a white-red border marker at the corner."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (232, 190, 130), (150, 110, 120))
    # sun low on the horizon
    d.ellipse([x1 - 92, y0 + 22, x1 - 48, y0 + 66], fill=(255, 226, 140))
    horizon = y0 + 78
    d.rectangle([x0, horizon, x1, y1], fill=(96, 130, 74))
    d.polygon([(x0, y1), (x0, horizon + 6), (x1, horizon + 14), (x1, y1)],
              fill=(76, 110, 60))
    # falling missile with smoke trail
    mx, my = x0 + 300, y0 + 18
    for i in range(12):
        t = i / 11.0
        px = mx - t * 150
        py = my + t * 92
        r = 3 + t * 7
        d.ellipse([px - r, py - r, px + r, py + r],
                  fill=(200, 200, 200) if i < 6 else (170, 170, 170))
    d.line([(mx, my), (mx - 150, my + 92)], fill=(220, 220, 220), width=2)
    d.polygon([(mx - 8, my - 4), (mx + 10, my + 2), (mx - 8, my + 10)],
              fill=(60, 60, 66))
    burst(d, mx - 158, my + 100, 24, rng)
    # NATO jet climbing
    jx, jy = x0 + 90, y0 + 44
    d.polygon([(jx, jy), (jx + 52, jy - 10), (jx + 74, jy), (jx + 52, jy + 8)],
              fill=(40, 44, 56))
    d.polygon([(jx + 26, jy - 6), (jx + 42, jy - 24), (jx + 48, jy - 6)],
              fill=(40, 44, 56))
    for i in range(4):
        tx = jx - 8 - i * 14
        ty = jy + 4 + i * 2
        d.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(230, 230, 230))
    # border marker: white over red post
    bx = x0 + 22
    d.rectangle([bx, y1 - 34, bx + 10, y1 - 4], fill=(255, 255, 255))
    d.rectangle([bx, y1 - 19, bx + 10, y1 - 4], fill=(213, 0, 50))
    d.rectangle([bx - 4, y1 - 38, bx + 14, y1 - 34], fill=(40, 40, 44))


def draw_cop31(d, box, rng):
    """A warming Earth between two pulling arrows: the climate talks
    deadlocked over fossil fuels."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (214, 232, 244), (178, 200, 220))
    cx, cy, r = x0 + 236, y0 + 58, 46
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 120, 200))
    d.ellipse([cx - r // 2, cy - r // 3, cx + r // 3, cy + r // 4],
              fill=(90, 170, 90))
    d.ellipse([cx - r + 8, cy + r // 4, cx - r // 4, cy + r // 2],
              fill=(90, 170, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=320,
          fill=(255, 255, 255), width=3)
    # thermometer on the right, mercury high and red
    tx = x1 - 52
    d.rectangle([tx, y0 + 14, tx + 16, y0 + 84], outline=(176, 42, 42), width=3)
    d.rectangle([tx + 3, y0 + 30, tx + 13, y0 + 84], fill=(222, 60, 40))
    d.ellipse([tx - 6, y0 + 78, tx + 22, y0 + 106], fill=(222, 60, 40))
    # smoke stacks on the left
    for sx in (x0 + 24, x0 + 58):
        d.rectangle([sx, y0 + 62, sx + 22, y1 - 12], fill=(90, 88, 84))
        for i in range(3):
            d.ellipse([sx - 4 + i * 4, y0 + 44 - i * 12,
                       sx + 12 + i * 4, y0 + 58 - i * 12],
                      fill=(160, 160, 160))
    # two arrows pulling apart = deadlock
    ay = y1 - 8
    d.line([(x0 + 120, ay), (x0 + 210, ay)], fill=(176, 42, 42), width=4)
    d.polygon([(x0 + 120, ay - 7), (x0 + 104, ay), (x0 + 120, ay + 7)],
              fill=(176, 42, 42))
    d.line([(x0 + 260, ay), (x0 + 350, ay)], fill=(27, 42, 74), width=4)
    d.polygon([(x0 + 350, ay - 7), (x0 + 366, ay), (x0 + 350, ay + 7)],
              fill=(27, 42, 74))


def draw_peru(d, box, rng):
    """The Andes shake: peaks, a cracked road, a seismograph zigzag."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (190, 214, 232), (232, 222, 200))
    d.ellipse([x1 - 66, y0 + 10, x1 - 30, y0 + 46], fill=(255, 236, 150))
    # mountain range
    peaks = [(x0, y1), (x0 + 30, y0 + 66), (x0 + 90, y0 + 18),
             (x0 + 150, y0 + 58), (x0 + 210, y0 + 8), (x0 + 280, y0 + 52),
             (x0 + 340, y0 + 26), (x0 + 400, y0 + 60), (x1, y0 + 70),
             (x1, y1)]
    d.polygon(peaks, fill=(110, 96, 84))
    # snow caps
    for (sx, sy) in [(x0 + 90, y0 + 18), (x0 + 210, y0 + 8),
                     (x0 + 340, y0 + 26)]:
        d.polygon([(sx - 16, sy + 16), (sx, sy), (sx + 16, sy + 16),
                   (sx + 6, sy + 12), (sx, sy + 18), (sx - 6, sy + 12)],
                  fill=(255, 255, 255))
    # cracked ground strip at the bottom
    gy = y1 - 26
    d.rectangle([x0, gy, x1, y1], fill=(140, 118, 88))
    crack = [(x0 + 60, gy)]
    cx = x0 + 60
    for i in range(6):
        cx += 55
        crack.append((cx, gy + (10 if i % 2 == 0 else 20)))
    crack.append((cx, y1))
    d.line(crack, fill=(60, 44, 30), width=4)
    # seismograph zigzag across the middle
    pts = []
    sx = x0 + 20
    sy = y0 + 88
    pts.append((sx, sy))
    for i in range(14):
        sx += 30
        sy = y0 + 88 + (rng.choice([-26, -14, 10, 22]) if i % 3 else 0)
        pts.append((sx, sy))
    d.line(pts, fill=(176, 42, 42), width=3)
    # small shaking house
    hx, hy = x0 + 320, y1 - 44
    d.polygon([(hx - 26, hy), (hx, hy - 22), (hx + 26, hy)],
              fill=(176, 42, 42))
    d.rectangle([hx - 22, hy, hx + 22, hy + 18], fill=(250, 246, 236))


def draw_sinaloa(d, box, rng):
    """Dusk raid on a desert highway: helicopter searchlight, convoy
    with flashing lights, a road sign."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (240, 186, 120), (120, 80, 96))
    d.ellipse([x1 - 70, y0 + 12, x1 - 34, y0 + 48], fill=(255, 226, 140))
    horizon = y0 + 74
    d.rectangle([x0, horizon, x1, y1], fill=(168, 128, 84))
    # cacti
    for cx in (x0 + 26, x0 + 420):
        d.rectangle([cx, horizon - 26, cx + 8, horizon + 6], fill=(46, 110, 60))
        d.rectangle([cx - 8, horizon - 16, cx, horizon - 6], fill=(46, 110, 60))
        d.rectangle([cx + 8, horizon - 12, cx + 16, horizon - 2],
                    fill=(46, 110, 60))
    # helicopter with searchlight beam
    hx, hy = x0 + 250, y0 + 30
    d.ellipse([hx - 34, hy - 12, hx + 34, hy + 12], fill=(40, 44, 56))
    d.line([(hx - 44, hy - 12), (hx + 44, hy - 12)], fill=(40, 44, 56), width=3)
    d.line([(hx + 30, hy), (hx + 58, hy + 6)], fill=(40, 44, 56), width=3)
    d.polygon([(hx + 52, hy - 24), (hx + 66, hy - 6), (hx + 60, hy + 4),
               (hx + 46, hy - 10)], fill=(40, 44, 56))
    d.polygon([(hx - 10, hy + 10), (hx - 60, horizon + 22),
               (hx - 20, horizon + 22)], fill=(255, 244, 190))
    # highway
    d.polygon([(x0, y1), (x0 + 120, horizon), (x1 - 120, horizon), (x1, y1)],
              fill=(52, 50, 56))
    for i in range(4):
        t = i / 3.0
        cx = x0 + 236 + (i - 1.5) * 8
        cy = horizon + 8 + t * (y1 - horizon - 14)
        d.line([(cx, cy), (cx, cy + 8)], fill=(255, 220, 120), width=3)
    # convoy vehicles with flashing lights
    for (vx, vw, col) in [(x0 + 150, 52, (30, 60, 120)),
                          (x0 + 260, 46, (30, 60, 120))]:
        vy = y1 - 34
        d.rectangle([vx, vy - 16, vx + vw, vy], fill=col)
        d.rectangle([vx + 6, vy - 26, vx + vw - 14, vy - 16], fill=col)
        d.ellipse([vx + 8, vy - 4, vx + 16, vy + 4], fill=(20, 20, 20))
        d.ellipse([vx + vw - 16, vy - 4, vx + vw - 8, vy + 4],
                  fill=(20, 20, 20))
        d.ellipse([vx + vw // 2 - 6, vy - 32, vx + vw // 2 + 6, vy - 22],
                  fill=(255, 60, 60))
    # road sign (kept clear of the right-hand cactus)
    sx = x0 + 368
    d.line([(sx, horizon + 6), (sx, horizon + 34)], fill=(90, 88, 84), width=3)
    d.rectangle([sx - 30, horizon - 14, sx + 30, horizon + 6],
                fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    d.text((sx, horizon - 4), "SINALOA", font=font(SANS_B, 9),
           fill=(26, 26, 26), anchor="ma")


def main():
    rng = random.Random(20261122)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle([16, 16, 1008, 1008], outline=INK, width=2)

    # ---- masthead ----
    d.text((512, 30), "SUNDAY 22 NOVEMBER 2026", font=font(SANS_B, 22),
           fill=RED, anchor="ma")
    d.text((512, 54), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=NAVY, anchor="ma")
    d.line([(28, 116), (996, 116)], fill=INK, width=3)
    d.line([(28, 122), (996, 122)], fill=INK, width=1)

    # ---- lead story: the Gulf ----
    lead_box = (28, 132, 468, 424)
    draw_gulf(d, lead_box, rng)
    d.rectangle(lead_box, outline=NAVY, width=2)
    tx = 488
    d.text((tx, 136), "THE GULF WAR", font=font(SANS_B, 20),
           fill=RED, anchor="la")
    head = "Iran strikes US base in Kuwait as Gulf war widens"
    y = 164
    for line in wrap(d, head, font(SERIF_B, 40), 508):
        d.text((tx, y), line, font=font(SERIF_B, 40), fill=INK, anchor="la")
        y += 48
    deck = ("Iran hits a US air base in Kuwait and targets Bahrain; "
            "tankers struck off Oman. Trump says an Iran deal could "
            "last 20 years and eyes \u201cultimate regime change\u201d.")
    y = 316
    for line in wrap(d, deck, font(SANS, 21), 508):
        d.text((tx, y), line, font=font(SANS, 21), fill=(58, 58, 58),
               anchor="la")
        y += 26

    d.line([(28, 434), (996, 434)], fill=INK, width=2)

    # ---- half panels ----
    panels = [
        # (x, y, illustration fn, headline, deck)
        (28, 444, draw_poland,
         "Russia's missiles rain down \u2014 and fall in Poland",
         "400 drones and 110 missiles hit Ukraine; Russian missiles "
         "crash in Poland and NATO jets scramble."),
        (523, 444, draw_cop31,
         "COP31 deadlocked over fossil fuels",
         "Fight over fossil fuels leaves the climate talks stuck; "
         "no deal as the summit runs out of time."),
        (28, 704, draw_peru,
         "6.9 quake shakes Peru's Andes",
         "Strong earthquake hits the Andes; no damage or casualties "
         "reported at first."),
        (523, 704, draw_sinaloa,
         "\u2018El Chapo Isidro\u2019 arrested in Mexico",
         "Special forces seize the cartel boss in a raid; deadly "
         "violence erupts in Sinaloa, 11 killed."),
    ]
    for (px, py, ill, head, deck) in panels:
        ill_box = (px, py, px + 473, py + 118)
        ill(d, ill_box, rng)
        d.rectangle(ill_box, outline=NAVY, width=2)
        y = py + 126
        for line in wrap(d, head, font(SERIF_B, 27), 473):
            d.text((px, y), line, font=font(SERIF_B, 27), fill=INK,
                   anchor="la")
            y += 33
        y = py + 194
        for line in wrap(d, deck, font(SANS, 18), 473):
            d.text((px, y), line, font=font(SANS, 18), fill=(58, 58, 58),
                   anchor="la")
            y += 22
    d.line([(512, 444), (512, 684)], fill=GREY, width=1)
    d.line([(512, 704), (512, 944)], fill=GREY, width=1)
    d.line([(28, 694), (996, 694)], fill=GREY, width=1)

    # ---- footer ----
    d.line([(28, 954), (996, 954)], fill=INK, width=2)
    d.text((28, 964), "Also: Estonia to close its border with Russia  \u00b7  "
                       "Bolsonaro in ICU  \u00b7  Shenzhen summit hailed "
                       "\u2018momentous\u2019",
           font=font(SANS, 15), fill=INK, anchor="la")
    d.text((996, 984), "Sources: BBC \u00b7 Times of India \u00b7 ARY News",
           font=font(SANS, 14), fill=GREY, anchor="ra")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
