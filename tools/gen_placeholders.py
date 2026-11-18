"""Brand-styled photo placeholders: Cream tint, a soft Sage circle and a simple two-tone line drawing."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
S, C = "#F4A62A", "#57534E"

# 100x100 line drawings, Sunny + Charcoal
DRAW = {
 "interior": f'''<path d="M50 4v16" stroke="{C}"/><path d="M33 38c0-10 8-18 17-18s17 8 17 18z" stroke="{S}"/>
<path d="M14 76h72M26 76v18M74 76v18" stroke="{C}"/><path d="M36 66h11v10H36zM47 69h3a3 3 0 0 1 0 6h-3" stroke="{S}"/><path d="M58 64c0 7 2 12 5 12s5-5 5-12z" stroke="{C}"/>''',
 "bowl": f'''<path d="M14 50h72c0 20-16 34-36 34S14 70 14 50z" stroke="{S}"/><path d="M36 88h28" stroke="{S}"/>
<path d="M64 10L44 46M76 14L54 47" stroke="{C}"/><path d="M30 40c-4-5 4-9 0-15M40 38c-4-5 4-9 0-15" stroke="{C}"/>''',
 "plate": f'''<circle cx="50" cy="52" r="26" stroke="{S}"/><circle cx="50" cy="52" r="16" stroke="{C}"/>
<path d="M12 24v56M8 24v12c0 7 8 7 8 0V24" stroke="{C}"/><path d="M88 24c-6 10-6 22 0 28v28" stroke="{C}"/>''',
 "glass": f'''<path d="M30 12h24c0 22-5 32-12 32S30 34 30 12z" stroke="{S}"/><path d="M42 44v36M32 82h20" stroke="{C}"/>
<path d="M66 32h10v8c4 3 6 8 6 14v28H60V54c0-6 2-11 6-14z" stroke="{C}"/><path d="M60 62h22" stroke="{S}"/>''',
 "awning": f'''<path d="M12 32l8-16h60l8 16" stroke="{S}"/><path d="M12 32c0 7 12 7 12 0 0 7 13 7 13 0 0 7 13 7 13 0 0 7 13 7 13 0 0 7 12 7 12 0 0 7 13 7 13 0" stroke="{S}"/>
<path d="M18 40v50M82 40v50M18 66h64" stroke="{C}"/><path d="M42 58l4-8h8l4 8" stroke="{C}"/>''',
 "heritage": f'''<path d="M10 34L50 12l40 22z" stroke="{S}"/><path d="M16 40h68M12 88h76M16 82h68" stroke="{C}"/>
<path d="M26 46v30M42 46v30M58 46v30M74 46v30" stroke="{C}"/><circle cx="50" cy="26" r="3" stroke="{S}"/>''',
 "pot": f'''<path d="M20 46h60v26c0 9-7 16-16 16H36c-9 0-16-7-16-16z" stroke="{S}"/><path d="M12 52h8M80 52h8" stroke="{S}"/>
<path d="M24 46c3-12 49-12 52 0M46 32h8" stroke="{C}"/><path d="M40 24c-4-5 4-8 0-14M58 24c-4-5 4-8 0-14" stroke="{C}"/>''',
}

LAYOUT = [(640, 190, 150, 860), (170, 170, 650, 860), (660, 840, 140, 150), (130, 820, 660, 150), (650, 200, 160, 840), (180, 220, 640, 850), (620, 830, 170, 170)]
for k, (name, d) in enumerate(DRAW.items()):
    gx, gy, sx, sy = LAYOUT[k % len(LAYOUT)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" preserveAspectRatio="xMidYMid slice">
<rect width="800" height="1000" fill="#EFE7DB"/>
<circle cx="{gx}" cy="{gy}" r="250" fill="#A7B89A" fill-opacity=".28"/>
<circle cx="{sx}" cy="{sy}" r="60" fill="#F4A62A" fill-opacity=".3"/>
<g transform="translate(250 360) scale(3)" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{d}</g>
</svg>'''
    (OUT / f"ph-{name}.svg").write_text(svg, encoding="utf-8")
print("ok", len(DRAW))
