"""DUB.SAR 1.0 — Tablet Renderer.

Implements Section 24 and Section 25:
- Clay-tablet-style SVG artwork rendering with authentic case rulings and cuneiform styling
- Terminal text tablet framing
"""

from __future__ import annotations

import html
import unicodedata
from typing import Optional


def get_char_width(ch: str) -> int:
    """Returns the monospace terminal column width of a character."""
    cp = ord(ch)
    if unicodedata.category(ch) in ("Mn", "Me", "Cf"):
        return 0
    # Cuneiform blocks (U+12000 to U+1247F) render as double-width (2 columns) in monospace terminals
    if 0x12000 <= cp <= 0x1247F:
        return 2
    # East Asian Wide (W) or Fullwidth (F)
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    return 1


def get_display_width(text: str) -> int:
    """Calculates the total visual terminal column display width of a string."""
    return sum(get_char_width(c) for c in text)


def pad_to_display_width(text: str, target_width: int) -> str:
    """Pads text with spaces so its visual display width matches target_width."""
    w = get_display_width(text)
    padding = max(0, target_width - w)
    return text + (" " * padding)


def render_svg(source: str, title: str = "DUB.SAR TABLET — 𒁾𒊬") -> str:
    """Renders the DUB.SAR tablet source into an authentic Mesopotamian clay tablet SVG artwork."""
    lines = source.splitlines()
    line_height = 28
    header_height = 90
    padding_top = 40
    padding_bottom = 50
    padding_x = 55

    max_line_len = max((len(l) for l in lines), default=20)
    width = max(680, max_line_len * 14 + padding_x * 2)
    height = max(400, len(lines) * line_height + header_height + padding_top + padding_bottom)

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>',
        '    <!-- Clay gradient -->',
        '    <linearGradient id="clayGradient" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#dfb890" />',
        '      <stop offset="30%" stop-color="#caa074" />',
        '      <stop offset="70%" stop-color="#b6895b" />',
        '      <stop offset="100%" stop-color="#9a6e42" />',
        '    </linearGradient>',
        '    <!-- Edge shadow gradient -->',
        '    <linearGradient id="edgeGlow" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#fff" stop-opacity="0.25" />',
        '      <stop offset="100%" stop-color="#000" stop-opacity="0.35" />',
        '    </linearGradient>',
        '    <!-- Filter for clay bevel shadow -->',
        '    <filter id="clayShadow" x="-10%" y="-10%" width="130%" height="130%">',
        '      <feDropShadow dx="4" dy="8" stdDeviation="6" flood-color="#3c200c" flood-opacity="0.55" />',
        '    </filter>',
        '  </defs>',
        '',
        '  <!-- Background Canvas -->',
        f'  <rect width="{width}" height="{height}" fill="#2a1f18" />',
        '',
        '  <!-- Clay Tablet Body -->',
        f'  <rect x="25" y="25" width="{width - 50}" height="{height - 50}" rx="32" ry="32"',
        '        fill="url(#clayGradient)" filter="url(#clayShadow)" stroke="#744a25" stroke-width="3" />',
        f'  <rect x="25" y="25" width="{width - 50}" height="{height - 50}" rx="32" ry="32"',
        '        fill="url(#edgeGlow)" />',
        '',
        '  <!-- Tablet Header / Case Ruling -->',
        f'  <text x="{width / 2}" y="65" text-anchor="middle" font-family="sans-serif, Arial" font-weight="bold" font-size="20" fill="#3a1c06" letter-spacing="2">',
        f'    {html.escape(title)}',
        '  </text>',
        f'  <text x="{width / 2}" y="88" text-anchor="middle" font-family="sans-serif, Arial" font-size="12" fill="#5c3413" letter-spacing="1">',
        '    IM.GID.DA — MATHEMATICAL TABLET PRESCRIPTION',
        '  </text>',
        f'  <line x1="{padding_x}" y1="105" x2="{width - padding_x}" y2="105" stroke="#683d18" stroke-width="2.5" stroke-linecap="round" />',
        f'  <line x1="{padding_x}" y1="109" x2="{width - padding_x}" y2="109" stroke="#dfb890" stroke-width="1" stroke-linecap="round" />',
        '',
        '  <!-- Inscribed Text and Case Registers -->',
        '  <g font-family="\'Noto Sans Cuneiform\', \'Segoe UI Historic\', monospace" font-size="15" fill="#331904">',
    ]

    curr_y = header_height + padding_top
    for idx, line in enumerate(lines):
        escaped = html.escape(line)
        # Register line below text
        rule_y = curr_y + 8
        svg_lines.append(
            f'    <line x1="{padding_x}" y1="{rule_y}" x2="{width - padding_x}" y2="{rule_y}" stroke="#78481e" stroke-width="0.75" stroke-dasharray="3,3" opacity="0.4" />'
        )
        # Text imprint (wedge shadow effect)
        svg_lines.append(
            f'    <text x="{padding_x + 10}" y="{curr_y}">{escaped}</text>'
        )
        curr_y += line_height

    svg_lines.extend([
        '  </g>',
        '',
        '  <!-- Colophon Bottom Seal -->',
        f'  <line x1="{padding_x}" y1="{curr_y + 15}" x2="{width - padding_x}" y2="{curr_y + 15}" stroke="#683d18" stroke-width="2" />',
        f'  <text x="{width / 2}" y="{curr_y + 35}" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6d411b" letter-spacing="1">',
        '    * DUB.SAR 1.0 CANONICAL TABLET *',
        '  </text>',
        '</svg>',
    ])

    return "\n".join(svg_lines)


def render_terminal_tablet(source: str, title: str = "DUB.SAR TABLET — 𒁾𒊬 𒅎𒁍𒁕") -> str:
    """Renders the source code framed in an authentic terminal box-drawing tablet with straight borders."""
    lines = source.splitlines()

    content_widths = [get_display_width(f"  {l}") for l in lines]
    max_content_w = max(content_widths, default=20)
    title_w = get_display_width(title)
    inner_width = max(64, max_content_w + 4, title_w + 4)

    border_top = "╔" + ("═" * inner_width) + "╗"
    border_mid = "╠" + ("═" * inner_width) + "╣"
    border_bot = "╚" + ("═" * inner_width) + "╝"

    pad_left = (inner_width - title_w) // 2
    pad_right = inner_width - title_w - pad_left
    title_line = "║" + (" " * pad_left) + title + (" " * pad_right) + "║"

    out_lines = [
        border_top,
        title_line,
        border_mid,
    ]

    for line in lines:
        content = f"  {line}"
        padded = pad_to_display_width(content, inner_width)
        out_lines.append(f"║{padded}║")

    out_lines.append(border_bot)
    return "\n".join(out_lines)
