# Markdown Tables to Inkscape Convertor
#### Video Demo: https://youtu.be/EBj2WXKmZUs
#### Description:
Convert Markdown (tables + text) to Hershey text compatible table in inkscape.
```
>py md2svg.py  table.md --max-chars 20 -h
usage: md2svg.py [-h] [-o OUTPUT] [--ratio RATIO] [--max-chars MAX_CHARS] [--no-borders] [--col-gap COL_GAP] [--preset PRESET] input

Markdown to SVG with auto-fit columns

positional arguments:
  input                 Input Markdown file

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output SVG file
  --ratio RATIO         Ratio of font size:width
  --max-chars MAX_CHARS
                        Max characters per cell (wrap)
  --no-borders, -B      Do not draw table borders
  --col-gap COL_GAP     Gap after each column in px
  --preset PRESET       Paper preset to use (SUNDARAM, NONE)

Made by @IAMAJAYPRO
```