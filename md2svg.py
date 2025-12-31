import argparse
import re
import textwrap

FONT_FAMILIY = "Myhandwriting"
# mm= px/(DPI:=96)*25.4
# PX = mm*DPI/25.4


class Presets:
    """Class holds configurations of different papers"""
    @staticmethod
    def __SUNDARAM(**params):
        params = {
            "FONT_SIZE": 28,
            "LINE_SPACING": 30.50,
        } | params
        return MarkdownToSVG(**params)

    def __NONE(**params):
        return MarkdownToSVG(**params)


class MarkdownToSVG:

    def __init__(self, FONT_SIZE=28, LINE_SPACING=30.50,
                 MAX_CHARS=None, DRAW_BORDERS=True, COL_GAP=0, RATIO=0.6):
        self.FONT_SIZE = FONT_SIZE
        self.LINE_SPACING = LINE_SPACING
        self.MAX_CHARS = MAX_CHARS
        self.DRAW_BORDERS = DRAW_BORDERS
        self.COL_GAP = COL_GAP
        self.FONT_WIDTH = RATIO*FONT_SIZE
        self.svg_elements = []
        self.y_cursor = 0

    def _wrap_text(self, text) -> list[str]:
        text_lines = textwrap.wrap(text, self.MAX_CHARS, break_long_words=False,
                                   break_on_hyphens=False) if self.MAX_CHARS else [text]
        return [x.rstrip() for x in text_lines]

    def _compute_wrapped_rows_and_widths(self, rows):
        """Wrap all rows and compute optimal column widths in one pass"""
        num_cols = max(len(row) for row in rows)
        col_widths = [0] * num_cols
        wrapped_rows: list[list[object]] = []

        for row in rows:
            wrapped_row = []
            for c, cell in enumerate(row):
                lines = self._wrap_text(cell)
                wrapped_row.append(lines)
                max_len = max(len(line) for line in lines)
                col_widths[c] = max(
                    col_widths[c], max_len * self.FONT_WIDTH)
            wrapped_rows.append(wrapped_row)
        return wrapped_rows, col_widths

    def _inkscape_text(self, x: float, y: float, lines: list[str]):
        """
        Create an SVG text object with multiple tspans for each line.
        """
        tspans = "\n".join(
            # style="font-size:{self.FONT_SIZE}{Made by: @IAMAJAYPRO}px; line-height:{self.FONT_SIZE + 2}px;"
            f' <tspan x="{x}" y="{y + i * self.FONT_SIZE}" >{line}</tspan>'
            for i, line in enumerate(lines)
        )
        return (f'<text xml:space="preserve"  '  # transform="scale(1)"
                f'style="font-size:{self.FONT_SIZE}px; line-height:{self.FONT_SIZE + 2}px; '
                # text-align:start; letter-spacing:-0.01px; white-space:pre; fill:#000000;" '
                f'font-family:{FONT_FAMILIY};" '
                # cords require here too for hershey
                f'x="0" y="0">\n{tspans}\n</text>\n')

    def render_table(self, rows, y_offset):
        elements, lines = [], []
        wrapped_rows, col_widths = self._compute_wrapped_rows_and_widths(rows)

        row_heights = [max(len(cell) for cell in row) *
                       self.LINE_SPACING for row in wrapped_rows]
        table_height = sum(row_heights)
        table_width = sum(col_widths) + self.COL_GAP * (len(col_widths) - 1)

        y_cursor = y_offset
        for wrapped_row, rh in zip(wrapped_rows, row_heights):
            x_cursor = 0
            for c, cell_lines in enumerate(wrapped_row):
                elements.append(self._inkscape_text(
                    x_cursor + 5, y_cursor + self.FONT_SIZE, cell_lines))
                x_cursor += col_widths[c] + self.COL_GAP
            y_cursor += rh

        if self.DRAW_BORDERS:
            # horizontal lines
            y_cursor = y_offset
            for rh in row_heights:
                lines.append(
                    f'<line x1="0" y1="{y_cursor}" x2="{table_width}" y2="{y_cursor}" stroke="black"/>')
                y_cursor += rh
            lines.append(
                f'<line x1="0" y1="{y_cursor}" x2="{table_width}" y2="{y_cursor}" stroke="black"/>')
            # vertical lines
            x_cursor = 0
            for w in col_widths:
                lines.append(
                    f'<line x1="{x_cursor}" y1="{y_offset}" x2="{x_cursor}" y2="{y_offset + table_height}" stroke="black"/>')
                x_cursor += w + self.COL_GAP
            lines.append(
                f'<line x1="{x_cursor}" y1="{y_offset}" x2="{x_cursor}" y2="{y_offset + table_height}" stroke="black"/>')

        return elements, lines, y_offset + table_height + self.LINE_SPACING

    def render_text(self, line, y_offset):
        return [self._inkscape_text(5, y_offset, [line.strip()])]

    def convert(self, md_content):
        buffer = []
        for line in md_content:
            if "|" in line:
                cells = re.findall(r'\s*([^|]+)\s*', line)
                if cells:
                    buffer.append(cells)
            else:
                if buffer:
                    elements, lines, self.y_cursor = self.render_table(
                        buffer, self.y_cursor)
                    self.svg_elements.extend(elements + lines)
                    buffer = []
                if line.strip():
                    self.svg_elements.extend(
                        self.render_text(line, self.y_cursor))
                self.y_cursor += self.LINE_SPACING
        if buffer:
            elements, lines, self.y_cursor = self.render_table(
                buffer, self.y_cursor)
            self.svg_elements.extend(elements + lines)

    def export_svg(self, filename="out.svg"):
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="{self.y_cursor + 50}">\n' + \
            ''.join(self.svg_elements) + '\n</svg>'
        with open(filename, "w") as f:
            f.write(svg_content)
        print(f"SVG created: {filename}")


class Verify:
    @staticmethod
    def preset(name: str):
        name = name.strip().upper()
        if not Presets.__dict__.get(f"_Presets__{name}"):
            raise argparse.ArgumentTypeError(f"Invalid preset: {name}")
        return name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Markdown to SVG with auto-fit columns")
    parser.epilog = """Made by @IAMAJAYPRO"""
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument(
        "-o", "--output", help="Output SVG file", default="out.svg")
    parser.add_argument("--ratio", type=float, default=0.6,
                        help="Ratio of font size:width")
    parser.add_argument("--max-chars", type=int,
                        help="Max characters per cell (wrap)")
    parser.add_argument("--no-borders", "-B",
                        action="store_true", help="Do not draw table borders")
    parser.add_argument("--col-gap", type=float, default=0,
                        help="Gap after each column in px")
    parser.add_argument("--preset", type=Verify.preset,
                        default="NONE", help="Paper preset to use (SUNDARAM, NONE)")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        md_content = f.read().strip().splitlines()

    converter = Presets.__dict__.get(f"_Presets__{args.preset}")(
        MAX_CHARS=args.max_chars,
        DRAW_BORDERS=not args.no_borders,
        COL_GAP=args.col_gap,
        RATIO=args.ratio
    )
    converter.convert(md_content)
    converter.export_svg(args.output)
