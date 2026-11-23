"""Render the one-page newspaper for Monday 23 November 2026.

Entry for the make.fun bounty "news-image-20261123": sum up one day of
world news in a single image. Everything on the page is drawn with PIL
-- no photographs, no downloaded art, no network -- so the picture
stands alone for a judge who sees nothing else. The stories were
researched and cross-checked on the day; see news.md for the sources.

Layout, top to bottom:
  masthead   "THE WORLD IN ONE DAY" with the Monday date line
  lead       Ukraine's sea drones sink a Russian corvette at Benghazi
  panels     NATO's emergency session; the Democrats' House majority;
             the market bounce; Seoul's first woman spy-chief nominee
  wide       Prabowo hands two VP candidates to the MPR in Jakarta
  briefs     a dark "ALSO THAT DAY" strip with four one-line stories

Running this file writes entry.png next to itself.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- page
PAGE = 1024            # square page, PAGE x PAGE pixels
MARGIN = 32            # white border around the printed area
PAPER = (246, 241, 230)
CARD = (255, 253, 246)
LEAD_TINT = (238, 229, 208)

# ----------------------------------------------------------------- ink
BLACK = (26, 24, 20)
BODY_INK = (50, 46, 40)
GREY = (94, 88, 78)
CARD_EDGE = (118, 110, 94)
RED = (148, 38, 28)
STRIP_INK = (224, 218, 202)      # pale text on the black briefs strip

# ------------------------------------------------------- lead motif band
SEA = (24, 44, 58)               # deep harbour water at dusk
WAVE = (96, 138, 158)
SHIP = (188, 178, 158)           # pale silhouette of the corvette
SHIP_DARK = (140, 130, 108)
DRONE = (226, 216, 192)          # the small sea drones
WAKE = (150, 178, 196)

# ------------------------------------------------------------- content
DATE_LINE = "MONDAY 23 NOVEMBER 2026"

LEAD_KICKER = "BENGHAZI · LIBYA"
LEAD_HEADLINE = "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA"
LEAD_DECK = "Sea drones strike a warship 1,500 miles from the front"
LEAD_BODY = (
    "President Zelenskyy confirmed on Monday that seven Ukrainian "
    "naval drones sank the Russian corvette Merkury and hit a Russian "
    "cargo ship in the port of Benghazi, Ukraine's longest-range naval "
    "strike of the war. The Kremlin called it terrorist activity."
)

PANELS = [
    (
        "BRUSSELS · NATO",
        "Emergency session over missiles in Poland",
        "NATO's top council met in emergency session after three "
        "Russian Kh-101 missiles came down in Poland during Friday's "
        "attack on Ukraine. Poland pressed for stronger air defences; "
        "no one in Poland was hurt.",
    ),
    (
        "WASHINGTON · US POLITICS",
        "Democrats clinch historic House majority",
        "House Democrats secured at least 258 seats as the last "
        "midterm results were confirmed, their largest majority since "
        "1992, and began preparing oversight of the Trump White House.",
    ),
    (
        "NEW YORK · MARKETS",
        "Futures bounce after the AI rout",
        "US stock futures rose about 2% early Monday after the AI "
        "sell-off gave the Nasdaq its worst week since 2020. The "
        "S&P 500 is still more than 10% below its October record.",
    ),
    (
        "SEOUL · SOUTH KOREA",
        "First woman picked to run spy agency",
        "President Lee Jae Myung's surprise reshuffle nominated "
        "ex-justice minister Kang Kum-sil to lead the National "
        "Intelligence Service, set to be the country's first female "
        "spy chief.",
    ),
]

WIDE_KICKER = "JAKARTA · INDONESIA"
WIDE_HEADLINE = "Prabowo hands two VP names to the MPR"
WIDE_BODY = (
    "President Prabowo Subianto went to parliament in Jakarta on "
    "Monday to hand the MPR two vice-presidential candidates, Andi "
    "Amran Sulaiman and Sugiono. The assembly votes on 11 December."
)

BRIEFS = [
    "Iran vows to use \u201call available means\u201d against the US "
    "naval blockade, now in its 130th day",
    "Jakarta stocks rebound as MSCI softens on a downgrade; the "
    "IHSG jumps 1.59% on Monday",
    "Alcaraz beats world No. 1 Zverev 6-2, 7-6 in Turin to win his "
    "first ATP Finals title",
    "After the Cikande factory fire, Serang's regent orders a "
    "safety audit of every factory",
]

# --------------------------------------------------------------- fonts
NOTO_DIR = "/usr/share/fonts/truetype/noto"
DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"


def _face(noto_name, dejavu_name):
    """Path of the preferred Noto face, or its DejaVu stand-in."""
    path = os.path.join(NOTO_DIR, noto_name)
    if os.path.isfile(path):
        return path
    return os.path.join(DEJAVU_DIR, dejavu_name)


SERIF_BLACK = _face("NotoSerif-Black.ttf", "DejaVuSerif-Bold.ttf")
SERIF_BOLD = _face("NotoSerif-Bold.ttf", "DejaVuSerif-Bold.ttf")
SANS_BOLD = _face("NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf")
SANS = _face("NotoSans-Regular.ttf", "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_width(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def fit_font(draw, text, path, size, floor, max_width):
    """Shrink from `size` towards `floor` until the text fits."""
    while size > floor and text_width(draw, text, font(path, size)) > max_width:
        size -= 2
    return font(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap, measured in pixels against the real font."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if text_width(draw, trial, fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, fnt, colour, max_width, leading):
    """Draw wrapped text from (x, y); return y below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def draw_centred(draw, cx, y, text, fnt, colour):
    draw.text((cx - text_width(draw, text, fnt) / 2, y), text,
              font=fnt, fill=colour)


# ------------------------------------------------------------- drawing
def masthead(draw):
    """Newspaper name, tagline and the red date line."""
    content_w = PAGE - 2 * MARGIN
    draw_centred(draw, PAGE / 2, 20,
                 "ONE PAGE  ·  ONE DAY  ·  THE WHOLE WORLD",
                 font(SANS_BOLD, 17), GREY)
    draw.line([(MARGIN, 44), (PAGE - MARGIN, 44)], fill=BLACK, width=2)
    name = "THE WORLD IN ONE DAY"
    draw_centred(draw, PAGE / 2, 50, name,
                 fit_font(draw, name, SERIF_BLACK, 54, 30, content_w),
                 BLACK)
    draw_centred(draw, PAGE / 2, 106, DATE_LINE,
                 fit_font(draw, DATE_LINE, SERIF_BLACK, 30, 20, content_w),
                 RED)
    draw.line([(MARGIN, 142), (PAGE - MARGIN, 142)], fill=BLACK, width=4)
    draw.line([(MARGIN, 149), (PAGE - MARGIN, 149)], fill=BLACK, width=1)


def sea_motif(draw, x0, y0, x1, y1):
    """Harbour water, one corvette, three sea drones closing in.

    The story is a night strike far from home: a pale warship sits low
    on the right while three small unmanned boats run at it from the
    left, each trailing a thin wake.
    """
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    water_y = y1 - 8
    # wavelets across the band
    for i, wx in enumerate(range(x0 + 14, x1 - 30, 46)):
        wy = y0 + 8 + (i % 3) * 5
        draw.arc([wx, wy, wx + 22, wy + 8], 180, 360, fill=WAVE, width=2)
    # the corvette: hull, deckhouse, mast, sitting low on the right
    sx = x1 - 250
    draw.polygon([(sx, water_y), (sx + 26, water_y - 13),
                  (sx + 196, water_y - 13), (sx + 214, water_y)],
                 fill=SHIP)
    draw.rectangle([sx + 62, water_y - 24, sx + 128, water_y - 13],
                   fill=SHIP)
    draw.rectangle([sx + 84, water_y - 31, sx + 108, water_y - 24],
                   fill=SHIP_DARK)
    draw.line([(sx + 150, water_y - 13), (sx + 150, water_y - 30)],
              fill=SHIP, width=3)
    draw.line([(sx + 150, water_y - 30), (sx + 168, water_y - 25)],
              fill=SHIP, width=2)
    # three sea drones running in from the left, wakes behind them
    for i, (dx, dy) in enumerate([(x0 + 30, water_y - 6),
                                  (x0 + 96, water_y - 13),
                                  (x0 + 168, water_y - 4)]):
        draw.line([(dx - 26, dy + 3), (dx - 4, dy + 2)], fill=WAKE,
                  width=2)
        draw.polygon([(dx, dy + 3), (dx + 6, dy - 3), (dx + 30, dy - 3),
                      (dx + 38, dy + 3)], fill=DRONE)
        draw.rectangle([dx + 14, dy - 7, dx + 22, dy - 3], fill=DRONE)


def lead_story(draw):
    """The tinted lead block: kicker, headline, deck, body, motif."""
    top, bottom = 157, 404
    inner_w = PAGE - 2 * MARGIN - 32
    draw.rectangle([MARGIN, top, PAGE - MARGIN, bottom],
                   fill=LEAD_TINT, outline=BLACK, width=2)
    draw.text((MARGIN + 16, top + 10), LEAD_KICKER,
              font=font(SANS_BOLD, 17), fill=RED)
    y = top + 36
    y = draw_wrapped(draw, MARGIN + 16, y, LEAD_HEADLINE,
                     fit_font(draw, LEAD_HEADLINE, SERIF_BLACK, 47, 30,
                              inner_w),
                     BLACK, inner_w, 54)
    y = draw_wrapped(draw, MARGIN + 16, y + 2, LEAD_DECK,
                     font(SERIF_BOLD, 21), RED, inner_w, 26)
    y = draw_wrapped(draw, MARGIN + 16, y + 6, LEAD_BODY,
                     font(SANS, 18), BODY_INK, inner_w, 23)
    band_top = bottom - 46
    assert y <= band_top - 6, f"lead text reaches motif: {y} > {band_top}"
    sea_motif(draw, MARGIN + 2, band_top, PAGE - MARGIN - 2, bottom - 2)


def story_card(draw, box, kicker, headline, body):
    """One bordered panel; the assert keeps every word on the page."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=CARD_EDGE, width=2)
    inset = 14
    inner_w = (x1 - x0) - 2 * inset
    y = y0 + 8
    draw.text((x0 + inset, y), kicker, font=font(SANS_BOLD, 15), fill=RED)
    y += 21
    y = draw_wrapped(draw, x0 + inset, y, headline,
                     font(SERIF_BOLD, 23), BLACK, inner_w, 27)
    y = draw_wrapped(draw, x0 + inset, y + 3, body,
                     font(SANS, 17), BODY_INK, inner_w, 21)
    assert y <= y1 - 6, f"panel overflow: '{headline}' ends {y}, box {y1}"


def wide_panel(draw):
    """Full-width card for the Jakarta vice-president story."""
    top, bottom = 796, 904
    inner_w = PAGE - 2 * MARGIN - 28
    draw.rectangle([MARGIN, top, PAGE - MARGIN, bottom],
                   fill=CARD, outline=CARD_EDGE, width=2)
    draw.text((MARGIN + 14, top + 8), WIDE_KICKER,
              font=font(SANS_BOLD, 15), fill=RED)
    y = draw_wrapped(draw, MARGIN + 14, top + 27, WIDE_HEADLINE,
                     font(SERIF_BOLD, 24), BLACK, inner_w, 28)
    y = draw_wrapped(draw, MARGIN + 14, y + 3, WIDE_BODY,
                     font(SANS, 17), BODY_INK, inner_w, 21)
    assert y <= bottom - 6, f"wide panel overflow: {y} > {bottom}"


def briefs_strip(draw):
    """The black ALSO THAT DAY strip: four briefs in four columns."""
    top, bottom = 912, 1008
    draw.rectangle([MARGIN, top, PAGE - MARGIN, bottom],
                   fill=BLACK, outline=BLACK, width=2)
    draw.text((MARGIN + 14, top + 7), "ALSO THAT DAY",
              font=font(SANS_BOLD, 18), fill=PAPER)
    col_w = (PAGE - 2 * MARGIN - 28 - 24) // 4
    for i, brief in enumerate(BRIEFS):
        bx = MARGIN + 14 + i * (col_w + 8)
        end = draw_wrapped(draw, bx, top + 31, "·  " + brief,
                           font(SANS, 14), STRIP_INK, col_w, 17)
        assert end <= bottom - 4, f"brief {i} overflow: {end} > {bottom}"


def build():
    """Assemble the whole front page and return the PIL image."""
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([14, 14, PAGE - 14, PAGE - 14], outline=BLACK, width=3)

    masthead(draw)
    lead_story(draw)

    col_w = (PAGE - 2 * MARGIN - 12) // 2
    left = (MARGIN, MARGIN + col_w)
    right = (MARGIN + col_w + 12, PAGE - MARGIN)
    rows = [(412, 596), (604, 788)]
    for i, (kicker, headline, body) in enumerate(PANELS):
        x0, x1 = left if i % 2 == 0 else right
        y0, y1 = rows[i // 2]
        story_card(draw, (x0, y0, x1, y1), kicker, headline, body)

    wide_panel(draw)
    briefs_strip(draw)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    img = build()
    img.save(target, format="PNG", optimize=True)
    print(f"wrote {target} size={os.path.getsize(target)} "
          f"dims={img.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
