from md2svg import MarkdownToSVG
import inkex


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

        # <<< ignore Inkscape tab argument
        pars.add_argument("--tabs", default="")
        pars.add_argument("--debug", type=inkex.Boolean, default=False,
                          help="Enable debug output")
        pars.add_argument("--preserve_original",
                          type=inkex.Boolean, default=True)

    def effect(self):
        selected = self.svg.selection
        selected_elements = list(selected.values())  # save originals

        md_lines = []
        start_x = 0
        start_y = 0

        if selected:
            first = selected_elements[0]
            #bbox = first.bounding_box()
            
            #start_x = bbox.left
            #start_y = bbox.top

            if self.options.debug:
                inkex.utils.debug(f"x={first.get('x')}")
                inkex.utils.debug(f"y={first.get('y')}")
                #inkex.utils.debug(
                 #   f"bbox=({bbox.left}, {bbox.top}) -> ({bbox.right}, {bbox.bottom})")

            for elem in selected.values():
                if isinstance(elem, inkex.TextElement):
                    text = "".join(elem.itertext())
                    md_lines.extend(text.splitlines())
        else:
            md_text = self.options.md_input.replace("\\n", "\n")
            md_lines = md_text.splitlines()

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

        converter.y_cursor = 0
        converter.convert(md_lines)

        from io import StringIO

        # get SVG string directly
        svg_string = converter.convert_svg()

        # load SVG from string
        svg_io = StringIO(svg_string)
        loaded_svg = inkex.load_svg(svg_io)
        loaded_svg.getroot()[0].set(
            "transform", f"translate({start_x},{start_y})")
        # append imported elements into current document
        self.document.getroot().append(
            loaded_svg.getroot()[0]
        )

        # remove originals if preserve_original is disabled
        if not self.options.preserve_original:
            for elem in selected_elements:
                parent = elem.getparent()
                if parent is not None:
                    parent.remove(elem)


if __name__ == "__main__":
    Extension().run()
