"""Draw the front page that entry.png holds.

The picture is a single square newspaper page summing up Monday
23 November 2026 for the make.fun contest news-image-20261123. PIL
does all the drawing: there are no photographs, no image assets and
no network involved, so the page has to speak for itself to a judge
who is shown nothing else. The reporting behind each item, and the
outlets it was checked in, live in news.md.

Reading the page from the top:

  * a masthead, THE WORLD IN ONE DAY, with the date picked out in red
  * the lead block: Ukraine's naval drones sink a Russian corvette in
    the harbour at Benghazi, with a small harbour scene drawn into it
  * four panels: the NATO emergency session, the Democrats' House
    majority, the futures bounce, and Seoul's spy-chief nomination
  * one wide panel: Prabowo delivers two VP names to the MPR
  * a black strip of four one-line briefs headed ALSO THAT DAY

Executing this file rewrites entry.png in its own directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --- the sheet -------------------------------------------------------
SIDE = 1024                      # the page is SIDE by SIDE pixels
EDGE = 32                        # margin of bare paper round the print
PAPER = (246, 241, 230)          # warm off-white page
PANEL_BG = (255, 253, 246)       # slightly paler card stock
LEAD_BG = (238, 229, 208)        # tinted block behind the lead story

# --- inks ------------------------------------------------------------
INK = (26, 24, 20)               # headlines and rules
TEXT = (50, 46, 40)              # ordinary body copy
FADED = (94, 88, 78)             # the quiet line above the masthead
BORDER = (118, 110, 94)          # card outlines
ACCENT = (148, 38, 28)           # red: date, kickers, the lead deck
STRIP_TEXT = (224, 218, 202)     # pale lettering on the black strip

# --- colours for the harbour vignette in the lead block --------------
HARBOUR = (24, 44, 58)           # dusk water
RIPPLE = (96, 138, 158)          # wavelets catching the light
WARSHIP = (188, 178, 158)        # the corvette's pale silhouette
WARSHIP_SHADE = (140, 130, 108)  # its darker bridge block
DRONE_HULL = (226, 216, 192)     # the little unmanned boats
DRONE_WAKE = (150, 178, 196)     # the wake trailing each one

# --- what the page says ----------------------------------------------
DATE_TEXT = "MONDAY 23 NOVEMBER 2026"

LEAD_PLACE = "BENGHAZI · LIBYA"
LEAD_TITLE = "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA"
LEAD_STANDFIRST = "Sea drones strike a warship 1,500 miles from the front"
LEAD_TEXT = (
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

WIDE_PLACE = "JAKARTA · INDONESIA"
WIDE_TITLE = "Prabowo hands two VP names to the MPR"
WIDE_TEXT = (
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

# --- type ------------------------------------------------------------
NOTO = "/usr/share/fonts/truetype/noto"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def font_file(noto_name, dejavu_name):
    """Prefer the Noto face; fall back to the DejaVu twin."""
    candidate = os.path.join(NOTO, noto_name)
    if os.path.isfile(candidate):
        return candidate
    return os.path.join(DEJAVU, dejavu_name)


SERIF_HEAVY = font_file("NotoSerif-Black.ttf", "DejaVuSerif-Bold.ttf")
SERIF = font_file("NotoSerif-Bold.ttf", "DejaVuSerif-Bold.ttf")
SANS_HEAVY = font_file("NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf")
SANS_PLAIN = font_file("NotoSans-Regular.ttf", "DejaVuSans.ttf")


def load(path, size):
    return ImageFont.truetype(path, size)


def measure(draw, text, fnt):
    """Pixel width of `text` in `fnt`, from its bounding box."""
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def shrink_to_fit(draw, text, path, size, smallest, width):
    """Step the size down by twos until the text fits `width`."""
    while size > smallest and measure(draw, text, load(path, size)) > width:
        size -= 2
    return load(path, size)


def wrap_words(draw, text, fnt, width):
    """Greedy wrapping: fill each line until the next word overflows."""
    done = []
    line = ""
    for word in text.split():
        attempt = (line + " " + word).strip()
        if measure(draw, attempt, fnt) <= width or not line:
            line = attempt
        else:
            done.append(line)
            line = word
    if line:
        done.append(line)
    return done


def paint_block(draw, x, y, text, fnt, colour, width, leading):
    """Paint `text` wrapped at (x, y); hand back the y underneath it."""
    for line in wrap_words(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def paint_centred(draw, centre_x, y, text, fnt, colour):
    """Paint `text` so that its middle lands on `centre_x`."""
    draw.text((centre_x - measure(draw, text, fnt) / 2, y), text,
              font=fnt, fill=colour)


# --- the pieces of the page ------------------------------------------
def paint_masthead(draw):
    """Paper name, the line above it, and the date in red."""
    usable = SIDE - 2 * EDGE
    paint_centred(draw, SIDE / 2, 20,
                  "ONE PAGE  ·  ONE DAY  ·  THE WHOLE WORLD",
                  load(SANS_HEAVY, 17), FADED)
    draw.line([(EDGE, 44), (SIDE - EDGE, 44)], fill=INK, width=2)
    name = "THE WORLD IN ONE DAY"
    paint_centred(draw, SIDE / 2, 50, name,
                  shrink_to_fit(draw, name, SERIF_HEAVY, 54, 30, usable),
                  INK)
    paint_centred(draw, SIDE / 2, 106, DATE_TEXT,
                  shrink_to_fit(draw, DATE_TEXT, SERIF_HEAVY, 30, 20,
                                usable),
                  ACCENT)
    draw.line([(EDGE, 142), (SIDE - EDGE, 142)], fill=INK, width=4)
    draw.line([(EDGE, 149), (SIDE - EDGE, 149)], fill=INK, width=1)


def paint_harbour(draw, x0, y0, x1, y1):
    """The lead story's little scene: dusk water, a warship, drones.

    The corvette rides low at the right of the band. Three unmanned
    boats hurry at it from the left, each dragging a short pale wake:
    a strike that came a very long way from home, in miniature.
    """
    draw.rectangle([x0, y0, x1, y1], fill=HARBOUR)
    surface = y1 - 8
    # rows of small arcs for wavelets, staggered down the band
    for i, wx in enumerate(range(x0 + 14, x1 - 30, 46)):
        wy = y0 + 8 + (i % 3) * 5
        draw.arc([wx, wy, wx + 22, wy + 8], 180, 360, fill=RIPPLE, width=2)
    # hull first, then the deckhouse, bridge and mast on top of it
    sx = x1 - 250
    draw.polygon([(sx, surface), (sx + 26, surface - 13),
                  (sx + 196, surface - 13), (sx + 214, surface)],
                 fill=WARSHIP)
    draw.rectangle([sx + 62, surface - 24, sx + 128, surface - 13],
                   fill=WARSHIP)
    draw.rectangle([sx + 84, surface - 31, sx + 108, surface - 24],
                   fill=WARSHIP_SHADE)
    draw.line([(sx + 150, surface - 13), (sx + 150, surface - 30)],
              fill=WARSHIP, width=3)
    draw.line([(sx + 150, surface - 30), (sx + 168, surface - 25)],
              fill=WARSHIP, width=2)
    # the three attackers, each drawn wake-first so the hull overlaps it
    for dx, dy in [(x0 + 30, surface - 6),
                   (x0 + 96, surface - 13),
                   (x0 + 168, surface - 4)]:
        draw.line([(dx - 26, dy + 3), (dx - 4, dy + 2)], fill=DRONE_WAKE,
                  width=2)
        draw.polygon([(dx, dy + 3), (dx + 6, dy - 3), (dx + 30, dy - 3),
                      (dx + 38, dy + 3)], fill=DRONE_HULL)
        draw.rectangle([dx + 14, dy - 7, dx + 22, dy - 3], fill=DRONE_HULL)


def paint_lead(draw):
    """The tinted block at the top: place, title, standfirst, story."""
    top, bottom = 157, 404
    inner = SIDE - 2 * EDGE - 32
    draw.rectangle([EDGE, top, SIDE - EDGE, bottom],
                   fill=LEAD_BG, outline=INK, width=2)
    draw.text((EDGE + 16, top + 10), LEAD_PLACE,
              font=load(SANS_HEAVY, 17), fill=ACCENT)
    y = top + 36
    y = paint_block(draw, EDGE + 16, y, LEAD_TITLE,
                    shrink_to_fit(draw, LEAD_TITLE, SERIF_HEAVY, 47, 30,
                                  inner),
                    INK, inner, 54)
    y = paint_block(draw, EDGE + 16, y + 2, LEAD_STANDFIRST,
                    load(SERIF, 21), ACCENT, inner, 26)
    y = paint_block(draw, EDGE + 16, y + 6, LEAD_TEXT,
                    load(SANS_PLAIN, 18), TEXT, inner, 23)
    scene_top = bottom - 46
    assert y <= scene_top - 6, f"lead copy crowds the scene: {y}"
    paint_harbour(draw, EDGE + 2, scene_top, SIDE - EDGE - 2, bottom - 2)


def paint_panel(draw, box, place, title, body):
    """One of the four middle cards; the assert guards its bottom edge."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_BG, outline=BORDER, width=2)
    pad = 14
    inner = (x1 - x0) - 2 * pad
    y = y0 + 8
    draw.text((x0 + pad, y), place, font=load(SANS_HEAVY, 15), fill=ACCENT)
    y += 21
    y = paint_block(draw, x0 + pad, y, title,
                    load(SERIF, 23), INK, inner, 27)
    y = paint_block(draw, x0 + pad, y + 3, body,
                    load(SANS_PLAIN, 17), TEXT, inner, 21)
    assert y <= y1 - 6, f"panel '{title}' spills: ends {y}, box ends {y1}"


def paint_wide(draw):
    """The full-width Jakarta card, sitting above the briefs strip."""
    top, bottom = 796, 904
    inner = SIDE - 2 * EDGE - 28
    draw.rectangle([EDGE, top, SIDE - EDGE, bottom],
                   fill=PANEL_BG, outline=BORDER, width=2)
    draw.text((EDGE + 14, top + 8), WIDE_PLACE,
              font=load(SANS_HEAVY, 15), fill=ACCENT)
    y = paint_block(draw, EDGE + 14, top + 27, WIDE_TITLE,
                    load(SERIF, 24), INK, inner, 28)
    y = paint_block(draw, EDGE + 14, y + 3, WIDE_TEXT,
                    load(SANS_PLAIN, 17), TEXT, inner, 21)
    assert y <= bottom - 6, f"wide panel spills: {y} past {bottom}"


def paint_briefs(draw):
    """The black strip along the foot: four briefs in four columns."""
    top, bottom = 912, 1008
    draw.rectangle([EDGE, top, SIDE - EDGE, bottom],
                   fill=INK, outline=INK, width=2)
    draw.text((EDGE + 14, top + 7), "ALSO THAT DAY",
              font=load(SANS_HEAVY, 18), fill=PAPER)
    column = (SIDE - 2 * EDGE - 28 - 24) // 4
    for i, brief in enumerate(BRIEFS):
        bx = EDGE + 14 + i * (column + 8)
        end = paint_block(draw, bx, top + 31, "·  " + brief,
                          load(SANS_PLAIN, 14), STRIP_TEXT, column, 17)
        assert end <= bottom - 4, f"brief {i} spills: {end} past {bottom}"


def render_page():
    """Paint every piece onto a fresh sheet and return the image."""
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([14, 14, SIDE - 14, SIDE - 14], outline=INK, width=3)

    paint_masthead(draw)
    paint_lead(draw)

    col = (SIDE - 2 * EDGE - 12) // 2
    left_col = (EDGE, EDGE + col)
    right_col = (EDGE + col + 12, SIDE - EDGE)
    row_bands = [(412, 596), (604, 788)]
    for i, (place, title, body) in enumerate(PANELS):
        x0, x1 = left_col if i % 2 == 0 else right_col
        y0, y1 = row_bands[i // 2]
        paint_panel(draw, (x0, y0, x1, y1), place, title, body)

    paint_wide(draw)
    paint_briefs(draw)
    return img


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(folder, "entry.png")
    img = render_page()
    img.save(target, format="PNG", optimize=True)
    print(f"wrote {target} size={os.path.getsize(target)} "
          f"dims={img.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
