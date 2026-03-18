import os
os.chdir('/home/claude')

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Baloo2',           'Baloo2-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Baloo2-Bold',      'Baloo2-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Baloo2-ExtraBold', 'Baloo2-ExtraBold.ttf'))
pdfmetrics.registerFont(TTFont('Baloo2-SemiBold',  'Baloo2-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('Nunito',           'Nunito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Nunito-Bold',      'Nunito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Nunito-SemiBold',  'Nunito-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('Nunito-Light',     'Nunito-Light.ttf'))
pdfmetrics.registerFont(TTFont('Nunito-Italic',    'Nunito-Italic.ttf'))

SUN        = HexColor('#FFB830')
SUN_LIGHT  = HexColor('#FFF0CC')
LEAF       = HexColor('#4CAF7D')
LEAF_DARK  = HexColor('#3A8F64')
SKY        = HexColor('#5BB5E8')
SKY_LIGHT  = HexColor('#E8F4FD')
CREAM      = HexColor('#FFFDF7')
INK        = HexColor('#2D3436')
INK_SOFT   = HexColor('#636E72')
DANGER_RED = HexColor('#E74C3C')
DANGER_BG  = HexColor('#FDF0EF')
GREEN_BG   = HexColor('#E8F8EE')
PURPLE_BG  = HexColor('#F3E8F8')

W, H   = A4
MARGIN = 18*mm
CW     = W - 2*MARGIN

c = canvas.Canvas('bug-hunt-freebie-v5.pdf', pagesize=A4)

EMOJI_DIR = 'bug_emoji_transparent'
BUG = {'Ant':'ant','Spider':'spider','Ladybug':'ladybug','Beetle':'beetle',
       'Worm':'worm','Butterfly':'butterfly','Snail':'snail','Bee':'bee'}

def bug_img(c, name, cx, cy, size_mm):
    path = f'{EMOJI_DIR}/{name}.png'
    s = size_mm * mm
    c.drawImage(path, cx - s/2, cy - s/2, s, s, mask='auto')

def microscope_img(c, cx, cy, size_mm):
    path = f'{EMOJI_DIR}/microscope.png'
    s = size_mm * mm
    c.drawImage(path, cx - s/2, cy - s/2, s, s, mask='auto')

def rr(c, x, y, w, h, r, fill=None, stroke=None, sw=1):
    c.saveState()
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    if fill:   c.setFillColor(fill)
    p = c.beginPath(); p.roundRect(x, y, w, h, r)
    if fill and stroke: c.drawPath(p, fill=1, stroke=1)
    elif fill:          c.drawPath(p, fill=1, stroke=0)
    else:               c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def checkbox(c, x, y, size=14):
    rr(c, x, y, size, size, 3, stroke=HexColor('#BBBBBB'), sw=1.2)

def wline(c, x, y, w, col=HexColor('#D0D0D0')):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(0.6)
    c.line(x, y, x+w, y); c.restoreState()

def grad_bar(c, x, y, w, h):
    sw = w/50
    for i in range(50):
        t = i/50
        r=int(255*(1-t)+255*t); g=int(184*(1-t)+107*t); b=int(48*(1-t)+107*t)
        c.setFillColor(HexColor(f'#{r:02x}{g:02x}{b:02x}'))
        c.rect(x+i*sw, y, sw+0.5, h, fill=1, stroke=0)

def footer(c, n, total=5):
    c.setFont('Nunito-Light', 7); c.setFillColor(INK_SOFT)
    c.drawCentredString(W/2, 12*mm,
        f'schooled.studio  \u2022  A free taster from Backyard Bug Lab  \u2022  Page {n} of {total}')
    grad_bar(c, 0, 0, W, 3*mm)

def page_bg(c):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    grad_bar(c, 0, H-4*mm, W, 4*mm)

def wrap(c, text, font, size, max_w):
    words = text.split(' '); line = ''; lines = []
    for w in words:
        t = (line+' '+w).strip()
        if c.stringWidth(t, font, size) <= max_w: line = t
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

# ── logo — amber pill with microscope inside ──────────────
def draw_logo(c, cx, top_y):
    pw = 13*mm; ph = 13*mm; r = 3.5*mm
    px = cx - pw/2; py = top_y - ph
    rr(c, px, py, pw, ph, r, fill=SUN)
    microscope_img(c, cx, py + ph/2, 9)
    # Brand name
    fs = 22; ny = py - 0.5*mm
    c.setFont('Baloo2-ExtraBold', fs)
    w1 = c.stringWidth('schooled', 'Baloo2-ExtraBold', fs)
    w2 = c.stringWidth('.studio',  'Baloo2-ExtraBold', fs)
    nx = cx - (w1+w2)/2
    c.setFillColor(INK);  c.drawString(nx,    ny, 'schooled')
    c.setFillColor(LEAF); c.drawString(nx+w1, ny, '.studio')
    ty = ny - 5*mm
    c.setFont('Nunito', 8); c.setFillColor(INK_SOFT)
    c.drawCentredString(cx, ty, 'Curiosity-driven learning resources for creative kids')
    return ty

# ═══════════════════════════════════════════════════════════
# PAGE 1
# ═══════════════════════════════════════════════════════════

page_bg(c); grad_bar(c, 0, H-6*mm, W, 6*mm)

y = H - 10*mm
lb = draw_logo(c, W/2, y)

y = lb - 9*mm
c.setFont('Baloo2-ExtraBold', 34); c.setFillColor(INK)
c.drawCentredString(W/2, y, 'Bug Hunt')
y -= 10*mm
c.setFont('Baloo2-SemiBold', 17); c.setFillColor(LEAF)
c.drawCentredString(W/2, y, 'Who Lives in Your Backyard?')
y -= 6*mm
c.setFont('Nunito-Italic', 9); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y, 'A free taster activity from Backyard Bug Lab')

# What you need
y -= 9*mm
box_h = 11*mm
rr(c, MARGIN, y-box_h, CW, box_h, 6, fill=SKY_LIGHT)
text_y = y - box_h/2 - 3  # proper vertical centre (accounting for font baseline)
c.setFont('Baloo2-SemiBold', 9); c.setFillColor(INK)
c.drawString(MARGIN+4*mm, text_y, 'What you need:')
c.setFont('Nunito', 8.5); c.setFillColor(INK_SOFT)
c.drawString(MARGIN+32*mm, text_y,
    'Your eyes, this sheet, a pencil, and a backyard (or school garden, park, or patch of dirt!)')

# All 8 bugs row
y -= 17*mm
all8 = ['Ladybug','Ant','Butterfly','Bee','Snail','Spider','Worm','Beetle']
for i, name in enumerate(all8):
    bx = MARGIN + (i+0.5)*(CW/8)
    bug_img(c, BUG[name], bx, y, 10)

# Bug terminology note
y -= 8*mm
c.setFont('Nunito-Italic', 7.5); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y,
    'We use the word \u2018bugs\u2019 to mean all the small creatures you might find \u2014 insects, spiders, snails, worms, and more.')
y -= 4*mm
c.drawCentredString(W/2, y, 'Scientists call them invertebrates (animals without a backbone).')

# ── Calculate available space and distribute evenly across 3 boxes ──
y -= 4*mm  # gap before first box

closing_h = 18*mm  # two lines of text + breathing room above footer
avail_space = y - 15*mm - closing_h  # 15mm for footer area
gap = 3*mm
box_space = avail_space - 3*gap
ala_h = box_space / 3
sh    = box_space / 3
ch    = box_space / 3

def draw_info_box(c, y_top, height, items, heading, heading_col, bg, stroke_col, 
                   emoji_name, bullet_col, font_size=9.5):
    """Draw a consistently-spaced info box. Items fill from top to bottom with no dead space."""
    rr(c, MARGIN, y_top - height, CW, height, 8, fill=bg, stroke=stroke_col, sw=1.2)
    ix = MARGIN + 5*mm
    # Heading
    hy = y_top - 7*mm
    c.setFont('Baloo2-Bold', 13); c.setFillColor(heading_col)
    c.drawString(ix, hy, heading)
    # Items — fill from just below heading to just above bottom edge
    first_item_y = hy - 7*mm
    last_item_y = y_top - height + 4*mm
    if len(items) > 1:
        item_gap = (first_item_y - last_item_y) / (len(items) - 1)
    else:
        item_gap = 0
    iy = first_item_y
    c.setFont('Nunito', font_size)
    for item in items:
        c.setFillColor(bullet_col); c.drawString(ix, iy, '\u2022')
        c.setFillColor(INK);        c.drawString(ix + 4*mm, iy, item)
        iy -= item_gap
    # Emoji on right, vertically centred
    bug_img(c, emoji_name, W - MARGIN - 14*mm, y_top - height/2, 16)

# ── ALA section ──
ala_top = y
rr(c, MARGIN, y - ala_h, CW, ala_h, 8, fill=SKY_LIGHT, stroke=SKY, sw=1)
ix = MARGIN + 5*mm
c.setFont('Baloo2-Bold', 13); c.setFillColor(SKY)
c.drawString(ix, y - 7*mm, 'Before You Go: Find Your Local Bugs')
ala_steps = [
    '1.  Go to ala.org.au \u2192 "Search & analyse" \u2192 "Explore your area"',
    '2.  Type in your suburb, postcode, or school address',
    '3.  Set the radius (1 km, 5 km, or 10 km) to zoom in or out',
    '4.  Click "Insects" or "Arachnids" to filter for bugs',
    '5.  Browse every species recorded near you \u2014 with photos!',
]
first_step_y = y - 14*mm
last_step_y = y - ala_h + 10*mm
step_gap = (first_step_y - last_step_y) / max(len(ala_steps) - 1, 1)
ay = first_step_y
c.setFont('Nunito', 9)
for step in ala_steps:
    c.drawString(ix, ay, step); ay -= step_gap
c.setFont('Nunito-Italic', 7.5); c.setFillColor(INK_SOFT)
c.drawString(ix, y - ala_h + 4*mm,
    'Atlas of Living Australia \u2014 100M+ records. Real scientists use it every day!')
microscope_img(c, W - MARGIN - 14*mm, y - ala_h/2, 18)
y -= ala_h + gap

# ── Stay Safe ──
s_items = [
    'LOOK but don\u2019t TOUCH \u2014 some bugs can bite or sting',
    'NEVER pick up a bug you don\u2019t recognise',
    'Watch out for: Redbacks, Funnel-webs, Bull ants, Wasps',
    'Always wear closed shoes outdoors',
    'Tell an adult if you\u2019re not sure about something',
]
draw_info_box(c, y, sh, s_items, 'Stay Safe!', DANGER_RED, DANGER_BG, DANGER_RED, 'spider', DANGER_RED)
y -= sh + gap

# ── Explorer's Code ──
c_items = [
    'We\u2019re visitors in their home \u2014 observe but don\u2019t disturb',
    'Never squash, collect, or harm any living creature',
    'If you lift a rock or log, always put it back carefully',
    'Bugs are important \u2014 they pollinate, feed birds, keep soil healthy',
    'A real scientist protects the things they study',
]
draw_info_box(c, y, ch, c_items, 'Bug Explorer\u2019s Code', LEAF_DARK, GREEN_BG, LEAF, 'ladybug', LEAF_DARK)
y -= ch

# Closing lines — positioned in the reserved closing_h space
closing_y = 15*mm + closing_h - 4*mm
c.setFont('Nunito-SemiBold', 10); c.setFillColor(INK)
c.drawCentredString(W/2, closing_y, 'Every backyard is home to hundreds of tiny creatures.')
c.setFont('Nunito-SemiBold', 10); c.setFillColor(LEAF)
c.drawCentredString(W/2, closing_y - 5.5*mm, 'Head outside, look closely, and find out who\u2019s living in yours!')

# Curriculum info is on page 5 — no need to duplicate here

footer(c, 1); c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 2 — BUG HUNT + TALLY (combined)
# ═══════════════════════════════════════════════════════════

page_bg(c)
y = H-16*mm
c.setFont('Baloo2-ExtraBold', 24); c.setFillColor(INK)
c.drawCentredString(W/2, y, 'The Bug Hunt')
y -= 7*mm
c.setFont('Nunito', 9); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y, 'Head outside and see how many of these you can spot! Tick each one you find and count how many.')

# Tally reminder — the good version
y -= 8*mm
rr(c, MARGIN, y-10*mm, CW, 12*mm, 6, fill=SKY_LIGHT)
c.setFont('Nunito-SemiBold', 8); c.setFillColor(SKY)
c.drawString(MARGIN+4*mm, y-3*mm, 'Tally marks reminder:')
c.setFont('Nunito', 8); c.setFillColor(INK)
c.drawString(MARGIN+38*mm, y-3*mm,
    'Draw one line for each bug you count.  I = 1    II = 2    III = 3    IIII = 4')
c.setFont('Nunito-Bold', 8)
c.drawString(MARGIN+38*mm, y-8*mm, 'Cross through every group of 5 like a gate:')
# Draw an actual tally gate: 4 vertical lines + 1 diagonal
c.saveState()
c.setStrokeColor(INK); c.setLineWidth(1.2)
tg_x = MARGIN + 107*mm; tg_y = y - 7*mm; tg_h = 4*mm; tg_sp = 2*mm
for j in range(4):
    c.line(tg_x + j*tg_sp, tg_y - tg_h/2, tg_x + j*tg_sp, tg_y + tg_h/2)
# Diagonal strike-through
c.line(tg_x - 1*mm, tg_y - tg_h/2 - 0.5*mm, tg_x + 3*tg_sp + 1*mm, tg_y + tg_h/2 + 0.5*mm)
c.restoreState()
c.setFont('Nunito-Bold', 8); c.setFillColor(INK)
c.drawString(tg_x + 4*tg_sp + 2*mm, y-8*mm, '= 5')
y -= 14*mm

# Bug cards — 2 columns, each card has: emoji, name, desc, checkbox, tally area
bugs = [
    ('Ant',       'Tiny and busy \u2014 often in a line',   SUN_LIGHT),
    ('Spider',    'Eight legs \u2014 might have a web',      SKY_LIGHT),
    ('Ladybug',   'Red shell with black spots',              GREEN_BG),
    ('Beetle',    'Hard, shiny shell \u2014 many colours',   PURPLE_BG),
    ('Worm',      'Long and wriggly \u2014 loves damp soil', SUN_LIGHT),
    ('Butterfly', 'Colourful wings \u2014 floats and flutters', SKY_LIGHT),
    ('Snail',     'Carries its house on its back',           GREEN_BG),
    ('Bee',       'Fuzzy and buzzy \u2014 visits flowers',   PURPLE_BG),
]
col_w = (CW-5*mm)/2; row_h = 24*mm

for i, (name, desc, bg) in enumerate(bugs):
    col = i%2; row = i//2
    bx = MARGIN + col*(col_w+5*mm)
    by = y - row*(row_h+3*mm) - row_h
    rr(c, bx, by, col_w, row_h, 8, fill=bg, stroke=HexColor('#E0E0E0'), sw=0.6)
    # Bug emoji
    bug_img(c, BUG[name], bx+11*mm, by+row_h/2+2*mm, 11)
    # Checkbox top-right
    checkbox(c, bx+col_w-5*mm-12, by+row_h-5*mm-12, 12)
    # Name and desc
    tx = bx+22*mm; avail = col_w-24*mm-8*mm
    c.setFont('Baloo2-Bold', 10); c.setFillColor(INK)
    c.drawString(tx, by+row_h/2+4*mm, name)
    c.setFont('Nunito', 7); c.setFillColor(INK_SOFT)
    lines = wrap(c, desc, 'Nunito', 7, avail)
    dy = by+row_h/2-2*mm
    for ln in lines:
        c.drawString(tx, dy, ln); dy -= 4*mm
    # Tally area at bottom of card
    c.setFont('Nunito-Light', 6); c.setFillColor(HexColor('#AAAAAA'))
    c.drawString(bx+4*mm, by+3*mm, 'Tally:')
    wline(c, bx+16*mm, by+3*mm, col_w-20*mm, HexColor('#CCCCCC'))

# Surprise Find — uses remaining space
y = y - 4*(row_h+3*mm) - 5*mm
c.setFont('Baloo2-Bold', 13); c.setFillColor(SUN)
c.drawString(MARGIN, y, 'Surprise Find!')
c.setFont('Nunito', 8.5); c.setFillColor(INK_SOFT)
c.drawString(MARGIN+38*mm, y+1, 'Spotted something not on the list? Draw and investigate it!')

y -= 4*mm
box_h   = y - 20*mm
draw_w  = CW * 0.40
gap     = CW * 0.05
obs_w   = CW - draw_w - gap
obs_x   = MARGIN + draw_w + gap

# Drawing box
rr(c, MARGIN, y-box_h, draw_w, box_h, 8, fill=white, stroke=SUN_LIGHT, sw=1.5)
c.setFont('Nunito-Light', 7.5); c.setFillColor(HexColor('#C8C8C8'))
c.drawCentredString(MARGIN+draw_w/2, y-box_h/2+2, 'Draw it here')

# Questions — right side
obs_lw = obs_w - 4*mm
obs_lc = HexColor('#E8D8A0')
q_labels = [
    'How many legs?',
    'What colours?',
    'Where did you find it?',
    'What was it doing?',
    'I think it might be a...',
]
total_q = len(q_labels)
q_spacing = box_h / total_q
oy = y - 3*mm
for label in q_labels:
    c.setFont('Nunito-Bold', 7.5); c.setFillColor(LEAF_DARK)
    c.drawString(obs_x, oy, label)
    oy -= 4*mm
    wline(c, obs_x, oy, obs_lw, obs_lc)
    oy -= (q_spacing - 4*mm)

footer(c, 2); c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 3 — LOOK CLOSER (observation drawing + journal)
# ═══════════════════════════════════════════════════════════

page_bg(c)
y = H-16*mm
c.setFont('Baloo2-ExtraBold', 24); c.setFillColor(INK)
c.drawCentredString(W/2, y, 'Look Closer')
y -= 7*mm
c.setFont('Nunito', 10); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y, 'Pick your favourite bug from today and draw it as carefully as you can.')

y -= 8*mm
rr(c, MARGIN, y-14*mm, CW, 14*mm, 6, fill=SKY_LIGHT)
c.setFont('Baloo2-SemiBold', 9); c.setFillColor(SKY)
c.drawString(MARGIN+4*mm, y-5*mm, 'Drawing tips:')
c.setFont('Nunito', 8); c.setFillColor(INK)
c.drawString(MARGIN+28*mm, y-5*mm,
    'Look really closely! How many legs? Wings? Antennae? What shape is its body?')
c.drawString(MARGIN+28*mm, y-10*mm,
    'Draw it BIG so you can show all the details. Add labels if you can!')

y -= 20*mm
draw_box_h = 80*mm
rr(c, MARGIN, y-draw_box_h, CW, draw_box_h, 12, fill=white, stroke=LEAF, sw=1.5)
c.setFont('Nunito-Light', 8); c.setFillColor(HexColor('#C8C8C8'))
c.drawString(MARGIN+5*mm, y-8*mm, 'My observation drawing')

y = y - draw_box_h - 6*mm
c.setFont('Nunito-SemiBold', 10); c.setFillColor(INK)
c.drawString(MARGIN, y, 'Bug name:')
wline(c, MARGIN+25*mm, y-1, CW-25*mm)

# Journal
y -= 8*mm
journal_bottom = 20*mm
journal_h = y - journal_bottom
rr(c, MARGIN, journal_bottom, CW, journal_h, 10, fill=SUN_LIGHT, stroke=SUN, sw=1)

jx = MARGIN+6*mm; jy = y-5*mm
c.setFont('Baloo2-Bold', 14); c.setFillColor(INK)
c.drawString(jx, jy, 'Bug Journal')
c.setFont('Nunito', 8); c.setFillColor(INK_SOFT)
c.drawString(jx+31*mm, jy+1, '\u2014 Write about the bug you drew above')

lc = HexColor('#E0D0B0'); lw = CW-12*mm

def jq(label, italic=None, lines=2):
    global jy
    jy -= 10*mm
    c.setFont('Nunito-Bold', 10); c.setFillColor(LEAF_DARK)
    c.drawString(jx, jy, label)
    if italic:
        lw2 = c.stringWidth(label, 'Nunito-Bold', 10)
        c.setFont('Nunito-Italic', 7.5); c.setFillColor(INK_SOFT)
        c.drawString(jx+lw2+2*mm, jy+1, italic)
    for _ in range(lines):
        jy -= 9*mm; wline(c, jx, jy, lw, lc)

jq('Where did you find it?', lines=2)
jq('What was it doing?', lines=2)
jq('What do you wonder about it?', italic='(This is the most important question!)', lines=3)

# Did You Know
dyk_top    = jy - 6*mm
dyk_bottom = journal_bottom + 4*mm
dyk_h      = dyk_top - dyk_bottom

if dyk_h >= 18*mm:
    rr(c, jx-2*mm, dyk_bottom, CW-8*mm, dyk_h, 6, fill=GREEN_BG)
    icon_size = min(dyk_h - 4*mm, 14*mm)
    bug_img(c, 'ladybug', jx + icon_size/2 + 1*mm, dyk_bottom + dyk_h/2, icon_size/mm)
    tx = jx + icon_size + 4*mm
    avail_w = CW - 18*mm - icon_size
    c.setFont('Baloo2-Bold', 9); c.setFillColor(LEAF_DARK)
    c.drawString(tx, dyk_top - 5*mm, 'Did you know?')
    c.setFont('Nunito', 7.5); c.setFillColor(INK)
    facts = [
        'There are more than 320,000 known beetle species \u2014 about 1 in 4 of all known animals is a beetle.',
        'Australia has over 350,000 invertebrate species. Most haven\u2019t even been named yet.',
        'Worms breathe through their skin \u2014 that\u2019s why they come out when it rains!',
    ]
    ty = dyk_top - 11*mm
    for fact in facts:
        if ty < dyk_bottom + 5*mm: break
        fl = wrap(c, fact, 'Nunito', 7.5, avail_w)
        for ln in fl:
            if ty < dyk_bottom + 5*mm: break
            c.drawString(tx, ty, ln); ty -= 5*mm
        ty -= 2*mm

footer(c, 3); c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 4 — BUG FACT FILE + REFLECTION + WHAT'S NEXT
# ═══════════════════════════════════════════════════════════

page_bg(c)
y = H-16*mm
c.setFont('Baloo2-ExtraBold', 24); c.setFillColor(INK)
c.drawCentredString(W/2, y, 'Bug Fact File')
y -= 7*mm
c.setFont('Nunito', 9); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y, 'Choose 3 bugs you found today. Write a mini fact file for each one!')

# 3 fact file cards — open-ended, not locked to specific bugs
y -= 7*mm
card_bgs = [SUN_LIGHT, SKY_LIGHT, GREEN_BG]
card_strokes = [SUN, SKY, LEAF]
card_emojis = ['ant', 'butterfly', 'beetle']
card_h = 42*mm

for idx in range(3):
    cy = y - idx*(card_h + 3*mm) - card_h
    rr(c, MARGIN, cy, CW, card_h, 8, fill=card_bgs[idx], stroke=card_strokes[idx], sw=1)
    # Bug number badge
    badge_x = MARGIN + 8*mm; badge_y = cy + card_h - 7*mm
    c.setFont('Baloo2-Bold', 11); c.setFillColor(card_strokes[idx])
    c.drawCentredString(badge_x, badge_y, f'Bug {idx+1}')
    # Emoji on right
    bug_img(c, card_emojis[idx], W - MARGIN - 12*mm, cy + card_h/2, 12)
    # Fields
    fx = MARGIN + 5*mm; fw = CW - 30*mm
    fy = cy + card_h - 10*mm
    fields = [
        ('What type of bug?', fw * 0.5),
        ('Where did you find it?', fw * 0.5),
        ('Describe it:', fw),
    ]
    for flabel, fwidth in fields:
        fy -= 8*mm
        c.setFont('Nunito-Bold', 7.5); c.setFillColor(INK)
        c.drawString(fx, fy, flabel)
        lbl_w = c.stringWidth(flabel, 'Nunito-Bold', 7.5) + 2*mm
        wline(c, fx + lbl_w, fy - 1, fwidth - lbl_w, HexColor('#C8C8C8'))

# Think About It — two questions now
y = y - 3*(card_h + 3*mm) - 5*mm
c.setFont('Baloo2-Bold', 13); c.setFillColor(SKY)
c.drawString(MARGIN, y, 'Think About It')
y -= 8*mm
c.setFont('Nunito-Bold', 9); c.setFillColor(INK)
c.drawString(MARGIN, y, 'Which bug was the hardest to find? Why do you think that is?')
for _ in range(2):
    y -= 7*mm; wline(c, MARGIN, y, CW)
y -= 5*mm
c.setFont('Nunito-Bold', 9); c.setFillColor(INK)
c.drawString(MARGIN, y, 'If you could be any bug for a day, which one would you choose? Why?')
for _ in range(2):
    y -= 7*mm; wline(c, MARGIN, y, CW)

# Want more — fills remainder, content centred vertically
y -= 5*mm
pb = 18*mm; ph = y-pb
rr(c, MARGIN, pb, CW, ph, 10, fill=SUN_LIGHT, stroke=SUN, sw=1.5)

# Vertically centre all content within the box
# Content block: title(~6) + 2 desc lines(~10) + bugs(~12) + button(~10) + subtext(~5) = ~43mm
content_block = 43*mm
content_start = pb + ph/2 + content_block/2

py = content_start
c.setFont('Baloo2-Bold', 14); c.setFillColor(INK)
c.drawCentredString(W/2, py, 'Want more? This is just Week 1!')
py -= 8*mm
c.setFont('Nunito', 8.5); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, py, 'Backyard Bug Lab is an 8-week cross-curricular unit with a science focus.')
py -= 5*mm
c.drawCentredString(W/2, py,
    'The full unit takes kids from their first bug hunt all the way to becoming a Bug Expert!')

# Centred bug row
py -= 10*mm
bug_row = ['ladybug', 'butterfly', 'ant', 'bee']
total_w = len(bug_row) * 15*mm
sx = W/2 - total_w/2 + 7.5*mm
for i, bname in enumerate(bug_row):
    bug_img(c, bname, sx + i*15*mm, py, 11)

# Green pill — smaller, with microscope logo, and clickable link
py -= 12*mm
upw = 55*mm; uph = 9*mm
pill_x = W/2 - upw/2; pill_y = py - uph
rr(c, pill_x, pill_y, upw, uph, uph/2, fill=LEAF)
# Microscope inside pill on left
microscope_img(c, pill_x + 10*mm, pill_y + uph/2, 6)
c.setFont('Baloo2-Bold', 10); c.setFillColor(white)
c.drawCentredString(W/2 + 3*mm, py - uph/2 - 1.5*mm, 'schooled.studio')
# Clickable link over the pill
from reportlab.lib.units import mm as _mm
c.linkURL('https://schooled.studio', (pill_x, pill_y, pill_x + upw, pill_y + uph))
py -= uph + 3*mm
c.setFont('Nunito', 7.5); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, py, 'Find out when it launches!')

footer(c, 4); c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 5 — ABOUT
# ═══════════════════════════════════════════════════════════

page_bg(c)
y = H-16*mm
c.setFont('Baloo2-ExtraBold', 22); c.setFillColor(INK)
c.drawCentredString(W/2, y, 'About Backyard Bug Lab')
y -= 7*mm
c.setFont('Nunito', 10); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, y, 'The full 8-week unit \u2014 here\u2019s what\u2019s inside:')

y -= 10*mm
weeks = [
    ('Week 1','Discover','Who lives in your backyard? (this freebie!)',SUN_LIGHT),
    ('Week 2','Observe', 'Look closer \u2014 detailed drawing and body parts',SKY_LIGHT),
    ('Week 3','Sort',    'Same and different \u2014 grouping bugs by features',GREEN_BG),
    ('Week 4','Habitat', 'Where do they live? Mapping bugs to places',PURPLE_BG),
    ('Week 5','Life',    'What do bugs need? Living vs non-living',SUN_LIGHT),
    ('Week 6','Change',  'Growing up bug \u2014 life cycles',SKY_LIGHT),
    ('Week 7','Protect', 'Bug guardians \u2014 why bugs matter',GREEN_BG),
    ('Week 8','Share',   'Bug Expert Report \u2014 present your findings!',PURPLE_BG),
]
rwh = 9*mm
for i,(wk,title,desc,bg) in enumerate(weeks):
    wy = y - i*(rwh+1.5*mm) - rwh
    rr(c, MARGIN, wy, CW, rwh, 5, fill=bg)
    ty = wy + rwh/2 - 3  # vertically centred (3pt below baseline centre for 8pt text)
    c.setFont('Baloo2-Bold', 8);    c.setFillColor(INK);      c.drawString(MARGIN+4*mm,  ty, wk)
    c.setFont('Baloo2-SemiBold', 8);c.setFillColor(LEAF_DARK);c.drawString(MARGIN+22*mm, ty, title)
    c.setFont('Nunito', 8);         c.setFillColor(INK_SOFT); c.drawString(MARGIN+42*mm, ty, desc)

y = y - 8*(rwh+1.5*mm) - 10*mm
c.setFont('Baloo2-Bold', 12); c.setFillColor(INK)
c.drawString(MARGIN, y, 'Each product includes:')
y -= 7*mm
for item in [
    'Student activity sheets (PDF \u2014 ready to print)',
    'Teacher\u2019s Guide with week-by-week plans, learning intentions, and assessment rubric',
    'Full curriculum alignment (see below)',
    'Safety guidelines and conservation principles',
    'Differentiation suggestions for support and extension',
]:
    c.setFont('Nunito', 8.5); c.setFillColor(LEAF)
    c.drawString(MARGIN+2*mm, y, '\u2713')
    c.setFillColor(INK); c.drawString(MARGIN+7*mm, y, item); y -= 5.5*mm
# Notion as separate add-on
c.setFont('Nunito', 8.5); c.setFillColor(LEAF)
c.drawString(MARGIN+2*mm, y, '\u2713')
c.setFillColor(INK); c.drawString(MARGIN+7*mm, y, 'Notion template (digital version students can duplicate)')
c.setFont('Nunito-Italic', 7); c.setFillColor(INK_SOFT)
c.drawString(MARGIN+7*mm, y-4.5*mm, 'Available as an optional add-on')
y -= 10*mm

y -= 6*mm
c.setFont('Baloo2-Bold', 12); c.setFillColor(INK)
c.drawString(MARGIN, y, 'Available for:')
y -= 7*mm
for stage, aud in [
    ('Stage 1','Year 1\u20132 (Ages 5\u20137)'),
    ('Stage 2','Year 3\u20134 (Ages 8\u20139)'),
    ('Stage 3','Year 5\u20136 (Ages 10\u201311)'),
    ('Bundle', 'All three stages at a discount'),
]:
    c.setFont('Nunito-Bold', 8.5); c.setFillColor(LEAF_DARK)
    c.drawString(MARGIN+4*mm, y, stage)
    c.setFont('Nunito', 8.5); c.setFillColor(INK_SOFT)
    c.drawString(MARGIN+28*mm, y, aud); y -= 5.5*mm

y -= 8*mm
c.setFont('Baloo2-Bold', 12); c.setFillColor(INK)
c.drawString(MARGIN, y, 'Curriculum Alignment')
y -= 7*mm
for label, desc in [
    ('NSW NESA',
     'Science & Technology K\u20136 Syllabus (2017) \u2014 Living World strand'),
    ('Australian Curriculum v9',
     'Science: Biological Sciences (covers QLD, VIC, SA, WA, TAS, NT, ACT)'),
    ('Cross-curricular',
     'Integrates English (writing, reports), Maths (data, tallying, measurement), Creative Arts (drawing, design)'),
]:
    c.setFont('Nunito-Bold', 8.5); c.setFillColor(LEAF_DARK)
    c.drawString(MARGIN+4*mm, y, label)
    c.setFont('Nunito', 8); c.setFillColor(INK_SOFT)
    c.drawString(MARGIN+4*mm, y-5*mm, desc); y -= 13*mm

y -= 2*mm
rr(c, MARGIN, y-14*mm, CW, 16*mm, 6, fill=SKY_LIGHT)
microscope_img(c, MARGIN + 10*mm, y - 6*mm, 10)
c.setFont('Baloo2-SemiBold', 9); c.setFillColor(SKY)
c.drawString(MARGIN+18*mm, y-4*mm, 'Recommended resource:')
c.setFont('Nunito', 8); c.setFillColor(INK)
c.drawString(MARGIN+18*mm, y-10*mm,
    'Atlas of Living Australia (ala.org.au) \u2014 enter your postcode to see what species live near you!')

c.setFont('Nunito-Light', 7); c.setFillColor(INK_SOFT)
c.drawCentredString(W/2, 18*mm,
    'schooled.studio  \u2022  A free taster from Backyard Bug Lab  \u2022  Page 5 of 5')
c.setFont('Nunito-Light', 6.5)
c.drawCentredString(W/2, 12*mm,
    '\u00A9 schooled.studio. For personal and single-classroom use only. Not for redistribution.')
grad_bar(c, 0, 0, W, 3*mm)

c.save()
print("PDF v5 created successfully!")
