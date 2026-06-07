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
    pdf.set_x(x0 + 2)
    pdf.cell(5, 5, marker)
    pdf.set_x(x0 + 7)
    pdf.multi_cell(epw - 7, 5, text, markdown=True)
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
    maxw = [0] * ncols
    for row in [header] + body:
        row = (row + [""] * ncols)[:ncols]
        for c in range(ncols):
            w = pdf.get_string_width(strip_inline(row[c]))
            maxw[c] = max(maxw[c], w)
    total = sum(maxw) or 1
    # scale to fit, with a minimum
    raw = [max(14, m / total * epw) for m in maxw]
    s = sum(raw)
    widths = [w / s * epw for w in raw]
    return widths


def draw_row(pdf, cells, widths, bold, fill, size):
    pdf.set_font("DejaVu", "B" if bold else "", size)
    line_h = 4.4
    pad = 1.4
    # measure wrapped height per cell
    heights = []
    for i, txt in enumerate(cells):
        txt = strip_inline(txt)
        nlines = count_wrapped_lines(pdf, txt, widths[i] - 2 * pad)
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
        txt = strip_inline(txt)
        pdf.set_fill_color(*fill)
        pdf.rect(x, y0, widths[i], row_h, style="F")
        pdf.rect(x, y0, widths[i], row_h, style="D")
        pdf.set_xy(x + pad, y0 + pad)
        pdf.set_text_color(*INK)
        pdf.multi_cell(widths[i] - 2 * pad, line_h, txt, markdown=True, align="L")
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
