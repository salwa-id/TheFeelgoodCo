import math
CX, CY, R = 550, 400, 235
S, C = "#F4A62A", "#57534E"
nodes = [
 dict(n=1, title=["Concept","development"], href="stage-1", label="Concept development", pos="top"),
 dict(n=2, title=["Business planning","& design"], href="stage-2", label="Business planning and design", pos="right"),
 dict(n=3, title=["Team development","& training"], href="stage-3", label="Team development and training", pos="bottom"),
 dict(n=4, title=["Implementation","& launch"], href="stage-4", label="Implementation and launch", pos="bottom"),
 dict(n=5, title=["Post-implementation","& optimisation"], href="stage-5", label="Post-implementation and optimisation", pos="left"),
]
def pt(deg, r=R):
    a = math.radians(deg)
    return CX + r*math.cos(a), CY + r*math.sin(a)

# 100x100 line icons: two-tone (Sunny + Charcoal)
ICONS = {
1: f'''<path d="M50 10C33 10 21 23 21 39c0 10 5 17 11 23v9h36v-9c6-6 11-13 11-23 0-16-12-29-29-29z" stroke="{S}"/>
<path d="M39 82h22M43 90h14M41 52l9-11 9 11" stroke="{C}"/>''',
2: f'''<path d="M24 10h34l18 18v62H24z" stroke="{S}"/><path d="M58 10v18h18" stroke="{S}"/>
<path d="M35 44h30M35 56h18" stroke="{C}"/><circle cx="68" cy="76" r="15" stroke="{C}"/><path d="M61 76l5 5 9-11" stroke="{C}"/>''',
3: f'''<circle cx="38" cy="30" r="13" stroke="{S}"/><path d="M12 82c0-18 11-29 26-29s26 11 26 29z" stroke="{S}"/>
<circle cx="71" cy="38" r="10" stroke="{C}"/><path d="M62 56c3-2 6-3 9-3 13 1 19 12 19 29h-18" stroke="{C}"/>''',
4: f'''<path d="M50 8c15 11 19 30 14 50H36C31 38 35 19 50 8z" stroke="{S}"/><circle cx="50" cy="34" r="7" stroke="{C}"/>
<path d="M36 58L22 74l16-3M64 58l14 16-16-3M43 70c0 9 7 18 7 18s7-9 7-18" stroke="{C}"/>''',
5: f'''<path d="M16 14v72h72" stroke="{C}"/><rect x="28" y="56" width="12" height="30" rx="2" stroke="{S}"/><rect x="48" y="42" width="12" height="44" rx="2" stroke="{S}"/><rect x="68" y="28" width="12" height="58" rx="2" stroke="{S}"/>
<path d="M26 40l18-16 12 8 24-20M68 12h12v12" stroke="{C}"/>''',
}


def arcs(out):
    G = 17
    for i in range(5):
        x0, y0 = pt(-90 + 72*i + G); x1, y1 = pt(-90 + 72*(i+1) - G)
        out.append(f'<path d="M{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{C}" stroke-width="3" stroke-linecap="round"/>')

def build(mobile):
    out = []
    arcs(out)
    if mobile:
        out.append(f'<text text-anchor="middle" font-size="34" font-weight="700" fill="{C}"><tspan x="{CX}" y="{CY-8}">A continuous cycle,</tspan><tspan x="{CX}" y="{CY+34}">not a one-time launch</tspan></text>')
    else:
        out.append(f'<text text-anchor="middle" font-size="26" font-weight="700" fill="{C}"><tspan x="{CX}" y="{CY-2}">A continuous cycle,</tspan><tspan x="{CX}" y="{CY+28}">not a one-time launch</tspan></text>')
    for i, nd in enumerate(nodes):
        x, y = pt(-90 + 72*i)
        out.append(f'<a href="#{nd["href"]}" aria-label="{nd["label"]}"><g transform="translate({x-50:.1f} {y-50:.1f})"><g class="node node-{nd["n"]}" fill="none" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[nd["n"]]}</g></g>')
        if not mobile:
            l1, l2 = nd["title"]
            if nd["pos"] == "top":
                out.append(f'<text text-anchor="middle" font-size="27" font-weight="700" fill="{C}"><tspan x="{x:.1f}" y="{y-96:.1f}">{l1}</tspan><tspan x="{x:.1f}" y="{y-64:.1f}">{l2}</tspan></text>')
            elif nd["pos"] == "bottom":
                out.append(f'<text text-anchor="middle" font-size="27" font-weight="700" fill="{C}"><tspan x="{x:.1f}" y="{y+84:.1f}">{l1}</tspan><tspan x="{x:.1f}" y="{y+114:.1f}">{l2}</tspan></text>')
            elif nd["pos"] == "right":
                out.append(f'<text font-size="27" font-weight="700" fill="{C}"><tspan x="{x+66:.1f}" y="{y-2:.1f}">{l1}</tspan><tspan x="{x+66:.1f}" y="{y+28:.1f}">{l2}</tspan></text>')
            else:
                out.append(f'<text text-anchor="end" font-size="27" font-weight="700" fill="{C}"><tspan x="{x-66:.1f}" y="{y-2:.1f}">{l1}</tspan><tspan x="{x-66:.1f}" y="{y+28:.1f}">{l2}</tspan></text>')
        out.append('</a>')
    x, y = pt(-90)
    out.append(f'<g class="orbit" aria-hidden="true"><circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{C}"/></g>')
    if mobile:
        cls, vb = "cycle mx-auto block h-auto w-full max-w-md md:hidden", "262 100 576 556"
    else:
        cls, vb = "cycle hidden h-auto w-full max-w-4xl md:block", "0 0 1100 760"
    return (f'<svg class="{cls}" viewBox="{vb}" role="img" '
            'aria-label="The five stages of the F&amp;B lifecycle shown as a loop: concept development, business planning and design, team development and training, implementation and launch, post-implementation and optimisation.">\n'
            + "\n".join(out) + '\n</svg>')

svg = build(False) + "\n" + build(True)
open("tools/cycle.svg.html", "w", encoding="utf-8").write(svg)
print(len(svg))
