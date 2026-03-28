class Group:
    "Group of objects"

    def __init__(self, label="group", iterable=[]):
        self.label = label
        self.items:list = iterable.copy()

    def __str__(self):
        return f'<g inkscape:label="{self.label}">\n{" ".join(str(item) for item in self.items)}</g>\n'

    def append(self, item):
        self.items.append(item)

    def extend(self, iterable):
        self.items.extend(iterable)

    def __iter__(self):
        return iter(self.items)


class Line:
    "Line with cords"

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return (
            f' <line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" y2="{self.y2}" '
            f'stroke="#1f2937" stroke-width="1.5"/>\n'
        )
    
def textSpan(x,y,line):
    # style="font-size:{self.FONT_SIZE}{Made by: @IAMAJAYPRO}px; line-height:{self.FONT_SIZE + 2}px;"
    return f' <tspan x="{x}" y="{y}" >{line}</tspan>'
