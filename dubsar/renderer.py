"""DUB.SAR 1.0 — Tablet Renderer.

Implements Section 24 and Section 25:
- Clay-tablet-style SVG artwork rendering with authentic case rulings and cuneiform styling
- Terminal text tablet framing
"""

from __future__ import annotations

import html
from typing import Optional


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
    """Renders the source code framed in an authentic terminal box-drawing tablet."""
    lines = source.splitlines()
    max_w = max((len(l) for l in lines), default=20)
    width = max(64, max_w + 6)

    border_top = "╔" + "═" * width + "╗"
    title_padded = title.center(width)
    border_mid = "╠" + "═" * width + "╣"
    border_bot = "╚" + "═" * width + "╝"

    out_lines = [
        border_top,
        f"║{title_padded}║",
        border_mid,
    ]

    for line in lines:
        padded = f"  {line}".ljust(width)
        out_lines.append(f"║{padded}║")

    out_lines.append(border_bot)
    return "\n".join(out_lines)
