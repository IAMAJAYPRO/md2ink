import sys
import os
sys.path.append(os.path.dirname(__file__))

import inkex
from md2svg import MarkdownToSVG


class Extension(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--md_input", default="")
        pars.add_argument("--font_size", type=int, default=28)
        pars.add_argument("--line_spacing", type=float, default=30.5)
        pars.add_argument("--max_chars", type=int, default=0)
        pars.add_argument("--col_gap", type=float, default=0)
        pars.add_argument("--ratio", type=float, default=0.6)
        pars.add_argument("--draw_borders", type=inkex.Boolean, default=True)
        pars.add_argument("--preset")

        pars.add_argument("--tabs", default="")  # <<< ignore Inkscape tab argument
        pars.add_argument("--debug", type=inkex.Boolean, default=False,
                  help="Enable debug output")

    def effect(self):
        import tempfile
        import os

        selected = self.svg.selection

        md_lines = []
        start_x = 0
        start_y = 0

        if selected:
            first = list(selected.values())[0]
            start_x = float(first.get("x", 0))
            start_y = float(first.get("y", 0))

            for elem in selected.values():
                if isinstance(elem, inkex.TextElement):
                    text = "".join(elem.itertext())
                    md_lines.extend(text.splitlines())
        else:
            md_lines = self.options.md_input.splitlines()

        scale = self.svg.unittouu("1px")

        converter = MarkdownToSVG(
            FONT_SIZE=self.options.font_size * scale,
            LINE_SPACING=self.options.line_spacing * scale,
            MAX_CHARS=self.options.max_chars,
            DRAW_BORDERS=self.options.draw_borders,
            COL_GAP=self.options.col_gap * scale,
            RATIO=self.options.ratio
        )

        if self.options.debug:
            inkex.utils.debug("Debug ON: Selected elements and parsed data")
            inkex.utils.debug(f"Selected nodes: {list(selected.keys())}")
            # you can also dump md_lines or converter repr
            inkex.utils.debug(f"Markdown lines:\n{md_lines}\n")
            inkex.utils.debug(f"Converter object:\n{converter!r}")


        converter.y_cursor = start_y
        converter.convert(md_lines)

        # create temp svg file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
        tmp.close()

        converter.export_svg(tmp.name)

        # import svg into document
        self.document.getroot().append(
            inkex.load_svg(tmp.name).getroot()[0]
        )

        os.remove(tmp.name)


if __name__ == "__main__":
    Extension().run()