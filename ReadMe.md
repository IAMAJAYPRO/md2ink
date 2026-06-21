# Markdown Tables → SVG (Inkscape Hershey Text Compatible)

Convert Markdown tables and text into SVG tables that work with the **Hershey Text extension in Inkscape**.
Supports both **CLI** and **Inkscape extension GUI**.

This tool is useful for plotter writing, handwriting fonts, or Hershey text workflows where normal text objects are not suitable.

---

# Features

* Convert Markdown tables to SVG
* Auto-fit column widths
* Optional text wrapping per cell
* Optional table borders
* Column gap control
* Works with Hershey Text extension
* CLI + Inkscape GUI version
* Supports text + tables in same Markdown file

---

# Installation (Inkscape Extension)

1. Locate Inkscape extensions folder:

   * Windows:
     `C:\Users\<username>\AppData\Roaming\inkscape\extensions`
   * Linux:
     `~/.config/inkscape/extensions`
   * Mac:
     `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions`

2. Copy these files into the extensions folder:

   ```
   md2svg.inx
   md2svg_gui.py
   md2svg.py
   Objects.py
   ```

3. Restart Inkscape.

4. The extension will appear in:

   ```
   Extensions → Markdown Table → SVG
   ```

---

# Usage (Inkscape GUI)

You can use the extension in two ways:

### Method 1 — Select Text

1. Write Markdown table as text inside Inkscape.
2. Select the text.
3. Run extension.
4. Table SVG will be generated at the text position.

### Method 2 — Use Input Box

Open extension and paste Markdown into **Markdown Input** box.

---

# Usage (CLI)

```
python md2svg.py input.md -o out.svg
```

### Example

```
python md2svg.py table.md --max-chars 20 --col-gap 2
```

---

# CLI Options

| Option         | Description                         |
| -------------- | ----------------------------------- |
| `-o, --output` | Output SVG file                     |
| `--ratio`      | Font width ratio                    |
| `--max-chars`  | Max characters per cell (text wrap) |
| `--no-borders` | Disable table borders               |
| `--col-gap`    | Gap between columns                 |
| `--preset`     | Paper preset (SUNDARAM, NONE)       |
| `--debug`      | Debug output                        |

---

# Inkscape Options (GUI)

## Input Tab

| Option            | Description         |
| ----------------- | ------------------- |
| Markdown Input    | Paste Markdown text |
| Debug Mode        | Print debug info    |
| Preserve Original | Keep original text  |

## Table Tab

| Option             | Description           |
| ------------------ | --------------------- |
| Max chars per cell | Wrap text in cells    |
| Column Gap         | Space between columns |
| Draw Borders       | Draw table borders    |

## Text Tab

| Option           | Description           |
| ---------------- | --------------------- |
| Font Size        | Text size             |
| Line Spacing     | Space between lines   |
| Font Width Ratio | Character width ratio |

---

# Example Markdown Table

```
| Name | Age | City |
|------|-----|------|
| Ajay | 20  | Mumbai |
| Ravi | 22  | Pune |
```

---

# Output

The tool generates an SVG containing:

* Text converted into tspans
* Proper table grid
* Hershey text compatible layout

---

# Notes

* Works best with Hershey Text fonts.
* SVG width is fixed, height auto-expands.
* Tables and normal text can be mixed in Markdown.
* Multiple tables supported in one file.

---

# Author

Made by AJAY MAURYA (**@IAMAJAYPRO**)  -- Backend + CLI + Frontend
VAIBHAV SINGH -- FRONTEND
AKASH HOLSAMBLE **@Beast18akash** -- FRONTEND inside inkscape

---
