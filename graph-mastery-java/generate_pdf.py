#!/usr/bin/env python3
"""Render GraphMasteryJava.md into a clean, syntax-friendly PDF.

A small purpose-built Markdown subset renderer (headings, paragraphs, bullet
lists, fenced code blocks, tables, horizontal rules) built on fpdf2 with the
DejaVu Unicode fonts so arrows/math glyphs (->, <=, alpha, x) render correctly.
"""
import re
import sys
from fpdf import FPDF

HERE = "/home/user/microservices/graph-mastery-java"
SRC = f"{HERE}/GraphMasteryJava.md"
OUT = f"{HERE}/GraphMasteryJava.pdf"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# Palette
INK = (30, 33, 38)
MUTED = (110, 116, 124)
ACCENT = (200, 60, 30)          # Java-ish warm red/orange for headings
RULE = (210, 213, 218)
CODE_BG = (244, 245, 247)
CODE_INK = (40, 44, 52)
TABLE_HEAD_BG = (231, 233, 236)
TABLE_ROW_BG = (249, 250, 251)
LINK_INK = (30, 90, 200)

LINK_RE = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Graph Mastery — Java Edition   ·   Page {self.page_no()}",
                  align="C")


def strip_inline(text: str) -> str:
    """Drop backticks (inline code) so text reads cleanly; keep bold markers."""
    text = text.replace("`", "")
    return text


def cell_display(text: str) -> str:
    """Visible text of a table cell for width/height measurement.

    Converts a whole-cell markdown link [label](url) to just `label`, and
    strips backticks/bold markers so a long URL never widens a column.
    """
    text = text.strip()
    m = LINK_RE.match(text)
    if m:
        text = m.group(1)
    return strip_inline(text).replace("**", "")


def main():
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(16, 14, 16)

    pdf.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("Mono", "", f"{FONT_DIR}/DejaVuSansMono.ttf")
    pdf.add_font("Mono", "B", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf")

    pdf.add_page()

    with open(SRC, encoding="utf-8") as f:
        lines = f.read().split("\n")

    epw = pdf.epw  # effective page width
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            render_code(pdf, code, epw)
            continue

        # Table
        if line.lstrip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            tbl = [line]
            i += 1
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            render_table(pdf, tbl, epw)
            continue

        # Horizontal rule
        if line.strip() == "---":
            pdf.ln(1.5)
            y = pdf.get_y()
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, y, pdf.l_margin + epw, y)
            pdf.ln(3)
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            render_heading(pdf, strip_inline(line[4:]), 11.5, space_before=2.5)
            i += 1
            continue
        if line.startswith("## "):
            render_heading(pdf, strip_inline(line[3:]), 14, space_before=4, rule=True)
            i += 1
            continue
        if line.startswith("# "):
            render_title(pdf, strip_inline(line[2:]))
            i += 1
            continue

        # Bullet / numbered list
        m_bullet = re.match(r"^(\s*)-\s+(.*)$", line)
        m_num = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m_bullet:
            render_list_item(pdf, strip_inline(m_bullet.group(2)), "•", epw)
            i += 1
            continue
        if m_num:
            render_list_item(pdf, strip_inline(m_num.group(3)),
                             f"{m_num.group(2)}.", epw)
            i += 1
            continue

        # Blank line
        if line.strip() == "":
            pdf.ln(2)
            i += 1
            continue

        # Paragraph
        render_paragraph(pdf, strip_inline(line), epw)
        i += 1

    pdf.output(OUT)
    print("wrote", OUT, "pages:", pdf.page_no())


def render_title(pdf, text):
    pdf.set_font("DejaVu", "B", 22)
    pdf.set_text_color(*ACCENT)
    pdf.multi_cell(0, 9, text, markdown=True)
    pdf.ln(1)


def render_heading(pdf, text, size, space_before=3, rule=False):
    # keep heading with following content
    if pdf.get_y() > pdf.h - 40:
        pdf.add_page()
    pdf.ln(space_before)
    if rule:
        y = pdf.get_y()
        pdf.set_draw_color(*RULE)
        pdf.set_line_width(0.2)
        pdf.line(pdf.l_margin, y, pdf.l_margin + pdf.epw, y)
        pdf.ln(2)
    pdf.set_font("DejaVu", "B", size)
    pdf.set_text_color(*ACCENT)
    pdf.multi_cell(0, size * 0.5 + 1, text, markdown=True)
    pdf.ln(1.2)


def render_paragraph(pdf, text, epw):
    pdf.set_font("DejaVu", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5, text, markdown=True)
    pdf.ln(1)


def render_list_item(pdf, text, marker, epw):
    pdf.set_font("DejaVu", "", 9.5)
    pdf.set_text_color(*INK)
    x0 = pdf.l_margin
    indent = 9            # room for two-digit markers like "13."
    pdf.set_x(x0 + 2)
    pdf.cell(indent - 2, 5, marker)
    pdf.set_x(x0 + indent)
    pdf.multi_cell(epw - indent, 5, text, markdown=True)
    pdf.ln(0.5)


def render_code(pdf, code_lines, epw):
    # strip leading/trailing blank lines
    while code_lines and code_lines[0].strip() == "":
        code_lines.pop(0)
    while code_lines and code_lines[-1].strip() == "":
        code_lines.pop()
    if not code_lines:
        return

    pdf.set_font("Mono", "", 8)
    line_h = 4.0
    pad = 2.2
    # wrap long lines on width
    avail = epw - 2 * pad
    char_w = pdf.get_string_width("M")  # mono width
    max_chars = max(20, int(avail / char_w))

    wrapped = []
    for ln in code_lines:
        ln = ln.replace("\t", "    ")
        if ln == "":
            wrapped.append("")
            continue
        while len(ln) > max_chars:
            cut = ln[:max_chars]
            wrapped.append(cut)
            ln = "        " + ln[max_chars:]  # hang-indent continuation
        wrapped.append(ln)

    block_h = line_h * len(wrapped) + 2 * pad

    # page break if block won't fit and is reasonably sized
    if pdf.get_y() + block_h > pdf.h - pdf.b_margin and block_h < pdf.h - 30:
        pdf.add_page()

    x0 = pdf.l_margin
    y0 = pdf.get_y()

    # draw background incrementally to survive page breaks
    pdf.set_fill_color(*CODE_BG)
    pdf.set_draw_color(*RULE)

    pdf.ln(0.5)
    y0 = pdf.get_y()
    # background rect for the portion on this page
    remaining = wrapped[:]
    while remaining:
        space = pdf.h - pdf.b_margin - pdf.get_y()
        fit = max(1, int((space - 2 * pad) / line_h))
        chunk = remaining[:fit]
        remaining = remaining[fit:]
        h = line_h * len(chunk) + 2 * pad
        yc = pdf.get_y()
        pdf.set_fill_color(*CODE_BG)
        pdf.rect(x0, yc, epw, h, style="F")
        pdf.set_xy(x0 + pad, yc + pad)
        pdf.set_text_color(*CODE_INK)
        pdf.set_font("Mono", "", 8)
        for cl in chunk:
            pdf.set_x(x0 + pad)
            pdf.cell(avail, line_h, cl)
            pdf.ln(line_h)
        pdf.set_y(yc + h)
        if remaining:
            pdf.add_page()
    pdf.ln(2)


def render_table(pdf, tbl_lines, epw):
    rows = []
    for ln in tbl_lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    # drop the separator row (index 1)
    header = rows[0]
    body = rows[2:]
    ncols = len(header)

    # choose column widths heuristically
    widths = compute_widths(pdf, header, body, epw)

    if pdf.get_y() > pdf.h - 30:
        pdf.add_page()

    # header
    draw_row(pdf, header, widths, bold=True, fill=TABLE_HEAD_BG, size=8.5)
    for idx, r in enumerate(body):
        # pad/truncate to ncols
        r = (r + [""] * ncols)[:ncols]
        fill = TABLE_ROW_BG if idx % 2 == 1 else (255, 255, 255)
        draw_row(pdf, r, widths, bold=False, fill=fill, size=8.5)
    pdf.ln(2)


def compute_widths(pdf, header, body, epw):
    ncols = len(header)
    pdf.set_font("DejaVu", "", 8.5)
    pad2 = 2 * 1.4 + 0.8                     # cell padding + a hair of slack
    content = [0.0] * ncols                 # widest full cell (ideal width)
    floor = [0.0] * ncols                   # widest single word (never wrap mid-word)
    for ri, row in enumerate([header] + body):
        row = (row + [""] * ncols)[:ncols]
        pdf.set_font("DejaVu", "B" if ri == 0 else "", 8.5)  # header is bold (wider)
        for c in range(ncols):
            disp = cell_display(row[c])
            content[c] = max(content[c], pdf.get_string_width(disp) + pad2)
            for word in disp.split():
                floor[c] = max(floor[c], pdf.get_string_width(word) + pad2)

    # Start at the per-column floor; hand the leftover space out in proportion
    # to how much each column actually wants (content beyond its floor).
    base = sum(floor)
    if base >= epw:                          # pathological: scale floors to fit
        return [f / base * epw for f in floor]
    extra = epw - base
    want = [max(0.0, content[c] - floor[c]) for c in range(ncols)]
    twant = sum(want) or 1.0
    return [floor[c] + extra * want[c] / twant for c in range(ncols)]


def draw_row(pdf, cells, widths, bold, fill, size):
    pdf.set_font("DejaVu", "B" if bold else "", size)
    line_h = 4.4
    pad = 1.4
    # measure wrapped height per cell
    heights = []
    for i, txt in enumerate(cells):
        nlines = count_wrapped_lines(pdf, cell_display(txt), widths[i] - 2 * pad)
        heights.append(nlines * line_h + 2 * pad)
    row_h = max(heights) if heights else line_h + 2 * pad

    if pdf.get_y() + row_h > pdf.h - pdf.b_margin:
        pdf.add_page()
        pdf.set_font("DejaVu", "B" if bold else "", size)

    x0 = pdf.l_margin
    y0 = pdf.get_y()
    x = x0
    pdf.set_draw_color(*RULE)
    pdf.set_line_width(0.15)
    for i, txt in enumerate(cells):
        pdf.set_fill_color(*fill)
        pdf.rect(x, y0, widths[i], row_h, style="F")
        pdf.rect(x, y0, widths[i], row_h, style="D")
        pdf.set_xy(x + pad, y0 + pad)
        m = LINK_RE.match(txt.strip())
        if m:                                   # clickable LeetCode link cell
            pdf.set_text_color(*LINK_INK)
            pdf.set_font("DejaVu", "U", size)
            pdf.multi_cell(widths[i] - 2 * pad, line_h, m.group(1),
                           align="L", link=m.group(2))
            pdf.set_font("DejaVu", "B" if bold else "", size)
        else:
            pdf.set_text_color(*INK)
            pdf.multi_cell(widths[i] - 2 * pad, line_h, strip_inline(txt),
                           markdown=True, align="L")
        x += widths[i]
    pdf.set_y(y0 + row_h)


def count_wrapped_lines(pdf, text, width):
    if width <= 1:
        return 1
    words = text.replace("**", "").split()
    if not words:
        return 1
    lines = 1
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdf.get_string_width(trial) <= width:
            cur = trial
        else:
            lines += 1
            cur = w
    return lines


if __name__ == "__main__":
    sys.exit(main())
