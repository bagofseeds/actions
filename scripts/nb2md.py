#!/usr/bin/env python3
"""
nb2md.py -- Convert Jupyter notebooks to clean Markdown.

Renders each notebook's *saved* outputs (cells are not executed) into a
Markdown file written next to the notebook (``foo.ipynb`` -> ``foo.md``).
Figures are embedded inline as base64 data URIs (or raw SVG), so no sidecar
image files are produced. Pure standard library.

Usage:
    python nb2md.py docs/examples/*.ipynb
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_ansi(text):
    """Remove ANSI escape sequences from terminal output."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def clean_html(text):
    """
    Strip most HTML tags that Jupyter injects into text/html output,
    keeping the raw content. Also collapses excessive blank lines.
    """
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(
        r"</(div|p|tr|thead|tbody|table)>", "\n", text, flags=re.IGNORECASE
    )
    text = re.sub(r"<t[dh][^>]*>", "\t", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = (text
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&nbsp;", " ")
            .replace("&quot;", '"')
            .replace("&#39;", "'"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def join_lines(lines):
    return "".join(lines)


# ---------------------------------------------------------------------------
# Output data handlers
# ---------------------------------------------------------------------------

def handle_image(mime, data):
    """Return inline HTML for base64-encoded (or raw SVG) image data."""
    if mime == "image/svg+xml":
        return f"{data}\n"
    return f'<img src="data:{mime};base64,{data}" alt="Output figure" />\n'


def render_output(output):
    """Convert a single cell output to Markdown text."""
    output_type = output.get("output_type", "")
    parts = []

    if output_type in ("display_data", "execute_result"):
        data = output.get("data", {})

        for mime in ("image/png", "image/jpeg", "image/svg+xml", "image/gif"):
            if mime in data:
                raw = data[mime]
                if isinstance(raw, list):
                    raw = join_lines(raw)
                parts.append(handle_image(mime, raw))
                return "".join(parts)

        if "text/html" in data:
            html = data["text/html"]
            html = join_lines(html) if isinstance(html, list) else html
            cleaned = clean_html(html)
            if cleaned:
                parts.append(f"```\n{cleaned}\n```\n")
            return "".join(parts)

        if "text/plain" in data:
            text = data["text/plain"]
            text = join_lines(text) if isinstance(text, list) else text
            text = strip_ansi(text).rstrip()
            if text:
                parts.append(f"```\n{text}\n```\n")

    elif output_type == "stream":
        text = join_lines(output.get("text", []))
        text = strip_ansi(text).rstrip()
        if text:
            name = output.get("name", "stdout")
            label = "" if name == "stdout" else f"  <!-- {name} -->"
            parts.append(f"```{label}\n{text}\n```\n")

    elif output_type == "error":
        ename = output.get("ename", "Error")
        evalue = output.get("evalue", "")
        traceback = output.get("traceback", [])
        tb_clean = strip_ansi("\n".join(traceback))
        parts.append(f"```\n{ename}: {evalue}\n{tb_clean}\n```\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Cell handlers
# ---------------------------------------------------------------------------

def render_code_cell(cell):
    source = join_lines(cell.get("source", []))
    outputs = cell.get("outputs", [])

    parts = []
    if source.strip():
        parts.append(f"```python\n{source}\n```\n")

    for output in outputs:
        rendered = render_output(output)
        if rendered:
            parts.append(rendered)

    return "\n".join(parts)


def render_markdown_cell(cell):
    source = join_lines(cell.get("source", []))
    return source.rstrip() + "\n"


def render_raw_cell(cell):
    source = join_lines(cell.get("source", []))
    if source.strip():
        return f"```\n{source.rstrip()}\n```\n"
    return ""


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------

def convert(nb_path):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    cells = nb.get("cells", [])
    sections = []

    for cell in cells:
        cell_type = cell.get("cell_type", "")
        if cell_type == "code":
            rendered = render_code_cell(cell)
        elif cell_type == "markdown":
            rendered = render_markdown_cell(cell)
        elif cell_type == "raw":
            rendered = render_raw_cell(cell)
        else:
            continue

        if rendered.strip():
            sections.append(rendered)

    return "\n\n".join(sections) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to Markdown."
    )
    parser.add_argument("notebooks", type=Path, nargs="*",
                        help="Paths to .ipynb files")
    args = parser.parse_args()

    for notebook in args.notebooks:
        if not notebook.exists():
            print(f"Error: {notebook} not found.", file=sys.stderr)
            continue
        md = convert(notebook)
        out = notebook.with_suffix(".md")
        out.write_text(md, encoding="utf-8")
        print(f"Written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
