"""
schooled.studio — PDF Design System
====================================
Reusable constants, colours, fonts, and layout utilities for all
Backyard Bug Lab products (and future schooled.studio resources).

Usage:
    from schooled_design import *
    
    c = canvas.Canvas('my-page.pdf', pagesize=A4)
    page_bg(c)
    draw_logo(c, W/2, H - 10*mm)
    footer(c, page_num=1, total=8)

Fonts required (clone from GitHub at session start):
    os.system('git clone --depth 1 https://github.com/julianhoneywill/schooled-assets.git')
    Then register fonts using register_fonts('schooled-assets')

Design rules (learned the hard way):
    1. NEVER use fixed-height boxes — calculate available space and distribute
    2. Every info box uses draw_info_box() for consistent internal spacing
    3. Font sizes are locked — see FONT HIERARCHY below
    4. Footer is sacred: 15mm from bottom, nothing else goes there
    5. Emoji fill dead space better than extra text
    6. Closing/CTA lines need a reserved zone, not a running y position
    7. Text in narrow boxes must be vertically centred using v_centre()
    8. Week/row strips use draw_week_row() for consistent vertical centering
    9. Tally marks use draw_tally_gate() — never use unicode strikethrough
   10. CTA buttons use draw_cta_button() — includes logo, link, and proper sizing
   11. Curriculum alignment lives on the About page only, not on page 1
   12. Notion template is listed as an optional add-on, separate from core inclusions
"""

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

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
ROW_BGS    = [SUN_LIGHT, SKY_LIGHT, GREEN_BG, PURPLE_BG]

W, H   = A4
MARGIN = 18*mm
CW     = W - 2*MARGIN
FOOTER_H = 15*mm
EMOJI_DIR = 'bug_emoji_transparent'

# ── FONT HIERARCHY ──
# Page title:      Baloo2-ExtraBold  24pt
# Section heading: Baloo2-Bold       13pt
# Sub-heading:     Baloo2-SemiBold   9-10pt
# Body text:       Nunito            9-9.5pt
# Body bold:       Nunito-Bold       9-10pt
# Helper text:     Nunito-Italic     7.5pt
# Fine print:      Nunito-Light      6.5-7pt
# Footer:          Nunito-Light      7pt

def register_fonts(font_dir='schooled-assets'):
    fonts = {
        'Baloo2':           'Baloo2-Regular.ttf',
        'Baloo2-Bold':      'Baloo2-Bold.ttf',
        'Baloo2-ExtraBold': 'Baloo2-ExtraBold.ttf',
        'Baloo2-SemiBold':  'Baloo2-SemiBold.ttf',
        'Nunito':           'Nunito-Regular.ttf',
        'Nunito-Bold':      'Nunito-Bold.ttf',
        'Nunito-SemiBold':  'Nunito-SemiBold.ttf',
        'Nunito-Light':     'Nunito-Light.ttf',
        'Nunito-Italic':    'Nunito-Italic.ttf',
    }
    for name, filename in fonts.items():
        path = os.path.join(font_dir, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        elif os.path.exists(filename):
            pdfmetrics.registerFont(TTFont(name, filename))
        else:
            print(f"Warning: {filename} not found")

# ── PRIMITIVES ──

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
    sw = w / 50
    for i in range(50):
        t = i / 50
        r = int(255*(1-t) + 255*t)
        g = int(184*(1-t) + 107*t)
        b = int(48*(1-t)  + 107*t)
        c.setFillColor(HexColor(f'#{r:02x}{g:02x}{b:02x}'))
        c.rect(x + i*sw, y, sw + 0.5, h, fill=1, stroke=0)

def wrap(c, text, font, size, max_w):
    words = text.split(' '); line = ''; lines = []
    for w in words:
        t = (line + ' ' + w).strip()
        if c.stringWidth(t, font, size) <= max_w: line = t
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def v_centre(box_y, box_h, font_size_pt=9):
    """Y baseline to vertically centre text in a box. box_y = bottom edge."""
    return box_y + box_h/2 - font_size_pt * 0.35

def emoji_img(c, name, cx, cy, size_mm, emoji_dir=EMOJI_DIR):
    """Draw a transparent emoji PNG centred at (cx, cy). No background box."""
    path = f'{emoji_dir}/{name}.png'
    if os.path.exists(path):
        s = size_mm * mm
        c.drawImage(path, cx - s/2, cy - s/2, s, s, mask='auto')

# ── PAGE FURNITURE ──

def page_bg(c):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    grad_bar(c, 0, H - 4*mm, W, 4*mm)

def footer(c, page_num, total=5, product='Backyard Bug Lab'):
    c.setFont('Nunito-Light', 7); c.setFillColor(INK_SOFT)
    c.drawCentredString(W/2, 12*mm,
        f'schooled.studio  \u2022  A free taster from {product}  \u2022  Page {page_num} of {total}')
    grad_bar(c, 0, 0, W, 3*mm)

def draw_logo(c, cx, top_y, emoji_dir=EMOJI_DIR):
    """Amber pill with microscope, brand name, tagline. Returns bottom y."""
    pw = 13*mm; ph = 13*mm; r = 3.5*mm
    px = cx - pw/2; py = top_y - ph
    rr(c, px, py, pw, ph, r, fill=SUN)
    emoji_img(c, 'microscope', cx, py + ph/2, 9, emoji_dir)
    fs = 22; ny = py - 0.5*mm
    c.setFont('Baloo2-ExtraBold', fs)
    w1 = c.stringWidth('schooled', 'Baloo2-ExtraBold', fs)
    w2 = c.stringWidth('.studio',  'Baloo2-ExtraBold', fs)
    nx = cx - (w1 + w2) / 2
    c.setFillColor(INK);  c.drawString(nx,      ny, 'schooled')
    c.setFillColor(LEAF); c.drawString(nx + w1,  ny, '.studio')
    ty = ny - 5*mm
    c.setFont('Nunito', 8); c.setFillColor(INK_SOFT)
    c.drawCentredString(cx, ty, 'Curiosity-driven learning resources for creative kids')
    return ty

# ── LAYOUT COMPONENTS ──

def draw_info_box(c, y_top, height, items, heading, heading_col, bg, stroke_col,
                  emoji_name, bullet_col, emoji_dir=EMOJI_DIR, font_size=9.5):
    """
    Coloured info box. Items distribute evenly top-to-bottom (no dead space).
    Internal: heading 7mm from top, first item 7mm below heading, 
    last item 4mm from bottom. Emoji 16mm on right, vertically centred.
    """
    rr(c, MARGIN, y_top - height, CW, height, 8, fill=bg, stroke=stroke_col, sw=1.2)
    ix = MARGIN + 5*mm
    hy = y_top - 7*mm
    c.setFont('Baloo2-Bold', 13); c.setFillColor(heading_col)
    c.drawString(ix, hy, heading)
    first_item_y = hy - 7*mm
    last_item_y  = y_top - height + 4*mm
    item_gap = (first_item_y - last_item_y) / (len(items) - 1) if len(items) > 1 else 0
    iy = first_item_y
    c.setFont('Nunito', font_size)
    for item in items:
        c.setFillColor(bullet_col); c.drawString(ix, iy, '\u2022')
        c.setFillColor(INK);        c.drawString(ix + 4*mm, iy, item)
        iy -= item_gap
    emoji_img(c, emoji_name, W - MARGIN - 14*mm, y_top - height/2, 16, emoji_dir)

def draw_page_title(c, y, title, subtitle=None):
    """Page title (24pt) + optional subtitle (10pt). Returns y below."""
    c.setFont('Baloo2-ExtraBold', 24); c.setFillColor(INK)
    c.drawCentredString(W/2, y, title)
    y -= 7*mm
    if subtitle:
        c.setFont('Nunito', 10); c.setFillColor(INK_SOFT)
        c.drawCentredString(W/2, y, subtitle)
        y -= 5*mm
    return y

def distribute_boxes(y_start, y_end, num_boxes, gap=3*mm):
    """Equal box heights to fill y_start to y_end. Returns (box_h, gap)."""
    total_gaps = (num_boxes - 1) * gap
    return (y_start - y_end - total_gaps) / num_boxes, gap

def draw_tally_gate(c, x, y, colour=None):
    """
    Draw a real tally gate (4 vertical lines + diagonal slash) = 5.
    NEVER use unicode strikethrough — it doesn't render in PDFs.
    Returns x position after the gate.
    """
    if colour is None: colour = INK
    c.saveState()
    c.setStrokeColor(colour); c.setLineWidth(1.2)
    h = 4*mm; sp = 2*mm
    for j in range(4):
        c.line(x + j*sp, y - h/2, x + j*sp, y + h/2)
    c.line(x - 1*mm, y - h/2 - 0.5*mm, x + 3*sp + 1*mm, y + h/2 + 0.5*mm)
    c.restoreState()
    return x + 4*sp + 2*mm

def draw_week_row(c, x, y, w, h, week_num, title, desc, bg, r=5):
    """Week row with vertically centred text. For the About page overview."""
    rr(c, x, y, w, h, r, fill=bg)
    ty = y + h/2 - 3
    c.setFont('Baloo2-Bold', 8);    c.setFillColor(INK)
    c.drawString(x + 4*mm, ty, f'Week {week_num}')
    c.setFont('Baloo2-SemiBold', 8);c.setFillColor(LEAF_DARK)
    c.drawString(x + 22*mm, ty, title)
    c.setFont('Nunito', 8);         c.setFillColor(INK_SOFT)
    c.drawString(x + 42*mm, ty, desc)

def draw_cta_button(c, cx, y, label='schooled.studio', url='https://schooled.studio',
                    subtitle='Find out when it launches!', show_logo=True, emoji_dir=EMOJI_DIR):
    """
    Green pill CTA button — sized to content (55mm), with microscope logo 
    and clickable link. Returns y below subtitle.
    """
    upw = 55*mm; uph = 9*mm
    pill_x = cx - upw/2; pill_y = y - uph
    rr(c, pill_x, pill_y, upw, uph, uph/2, fill=LEAF)
    if show_logo:
        emoji_img(c, 'microscope', pill_x + 10*mm, pill_y + uph/2, 6, emoji_dir)
        c.setFont('Baloo2-Bold', 10); c.setFillColor(white)
        c.drawCentredString(cx + 3*mm, pill_y + uph/2 - 3.5, label)
    else:
        c.setFont('Baloo2-Bold', 10); c.setFillColor(white)
        c.drawCentredString(cx, pill_y + uph/2 - 3.5, label)
    c.linkURL(url, (pill_x, pill_y, pill_x + upw, pill_y + uph))
    sub_y = pill_y - 4*mm
    c.setFont('Nunito', 7.5); c.setFillColor(INK_SOFT)
    c.drawCentredString(cx, sub_y, subtitle)
    return sub_y - 3*mm

def draw_want_more_box(c, y_top, y_bottom, emoji_dir=EMOJI_DIR):
    """'Want more?' CTA box. Content vertically centred. Uses draw_cta_button()."""
    ph = y_top - y_bottom
    rr(c, MARGIN, y_bottom, CW, ph, 10, fill=SUN_LIGHT, stroke=SUN, sw=1.5)
    content_block = 43*mm
    py = y_bottom + ph/2 + content_block/2
    c.setFont('Baloo2-Bold', 14); c.setFillColor(INK)
    c.drawCentredString(W/2, py, 'Want more? This is just Week 1!')
    py -= 8*mm
    c.setFont('Nunito', 8.5); c.setFillColor(INK_SOFT)
    c.drawCentredString(W/2, py, 'Backyard Bug Lab is an 8-week cross-curricular unit with a science focus.')
    py -= 5*mm
    c.drawCentredString(W/2, py,
        'The full unit takes kids from their first bug hunt all the way to becoming a Bug Expert!')
    py -= 10*mm
    for i, bname in enumerate(['ladybug', 'butterfly', 'ant', 'bee']):
        total_w = 4 * 15*mm
        sx = W/2 - total_w/2 + 7.5*mm
        emoji_img(c, bname, sx + i*15*mm, py, 11, emoji_dir)
    py -= 12*mm
    draw_cta_button(c, W/2, py, emoji_dir=emoji_dir)

# ── QUICK REFERENCE ──
#
# page_bg(c)                                    — cream bg + top gradient
# footer(c, 1, total=5)                         — footer + bottom gradient
# draw_logo(c, W/2, H-10*mm)                    — logo block, returns bottom y
# draw_page_title(c, y, 'Title', 'Subtitle')    — returns y below
# draw_info_box(c, y, h, items, ...)             — no dead space, emoji on right
# distribute_boxes(y_start, y_end, 3)            — equal heights, returns (h, gap)
# draw_week_row(c, x, y, w, h, 1, 'Discover', 'desc', SUN_LIGHT)
# draw_tally_gate(c, x, y)                       — returns x after gate
# draw_cta_button(c, W/2, y)                     — green pill + logo + link
# draw_want_more_box(c, y_top, 18*mm)            — full CTA section
# emoji_img(c, 'ladybug', cx, cy, 12)            — transparent emoji
# v_centre(box_y, box_h, font_size_pt)           — baseline y for centred text
# wline(c, x, y, w)                              — writing line
# checkbox(c, x, y)                              — empty tick box
