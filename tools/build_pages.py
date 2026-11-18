"""Generates index.html and about.html (static, Tailwind classes only).

Run:  py tools/gen_cycle.py   (only if the lifecycle diagram changes)
      py tools/build_pages.py
      npm run build
"""
import html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CYCLE = (ROOT / "tools" / "cycle.svg.html").read_text(encoding="utf-8")
e = html.escape

# ------------------------------------------------------------------ design tokens
# One container, one section rhythm and one type scale, used everywhere.
WRAP = "mx-auto w-full px-6 md:px-10"
SECTION = "py-20 md:py-28"
H2 = "text-[26px] font-bold uppercase leading-[1.15] tracking-[.06em] md:text-[32px]"
H3 = "text-[19px] font-bold leading-snug md:text-[20px]"
LABEL = "text-[13px] font-bold uppercase tracking-[.16em]"
BODY = "text-[17px] leading-[1.65]"
SMALL = "text-[15px] leading-[1.6]"
LEAD = "text-[22px] font-light leading-[1.4] md:text-[28px]"
P = f"reveal {BODY}"
NAV = ("touch-manipulation py-2 text-[13px] uppercase tracking-[.14em] text-charcoal transition-colors duration-200 "
       "hover:text-cream data-[active]:font-black data-[active]:text-cream md:text-[15px]")
BTN = ("group/btn inline-flex min-h-12 cursor-pointer touch-manipulation select-none items-center gap-3 rounded-full bg-sunny px-7 "
       "text-[15px] font-bold uppercase tracking-[.12em] text-charcoal transition-transform duration-150 ease-out active:scale-[.97]")
DOT = '<span aria-hidden="true" class="size-2.5 flex-none rounded-full bg-sunny"></span>'
PLUS = ('<svg class="transition-transform duration-300 ease-out group-aria-expanded/btn:rotate-45" width="16" height="16" viewBox="0 0 16 16" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 2v12M2 8h12"/></svg>')
CHEVRON = ('<svg class="transition-transform duration-300 ease-out group-aria-expanded/btn:rotate-180" width="14" height="14" viewBox="0 0 16 16" '
           'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6l5 5 5-5"/></svg>')
PANEL = "grid grid-rows-[0fr] transition-[grid-template-rows] duration-300 ease-out motion-reduce:transition-none"


def heading(title):
    return (f'<div class="flex flex-col gap-4"><h2 class="reveal {H2}">{title}</h2>'
            f'<div class="reveal-bar h-0.5 w-12 bg-sunny" aria-hidden="true"></div></div>')

LOADER = '''<div id="loader" aria-hidden="true" class="fixed inset-0 z-[100] hidden flex-col items-center justify-center gap-8 bg-cream transition-opacity duration-500 ease-out data-[done]:opacity-0 [.js:not(.no-loader)_&]:flex [&>*]:transition-opacity [&>*]:duration-150 data-[done]:delay-150 data-[done]:[&>*]:opacity-0">
<img src="assets/img/logo.png" alt="" class="w-[180px] animate-loader-in md:w-[220px]">
<div class="flex gap-2.5">
<span class="size-2.5 animate-loader-dot rounded-full bg-charcoal motion-reduce:animate-none"></span>
<span class="size-2.5 animate-loader-dot rounded-full bg-charcoal [animation-delay:150ms] motion-reduce:animate-none"></span>
<span class="size-2.5 animate-loader-dot rounded-full bg-charcoal [animation-delay:300ms] motion-reduce:animate-none"></span>
</div>
</div>
'''


def head(title, desc, loader=True):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F4A62A">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/img/logo.png">
<link rel="preload" href="assets/fonts/lato-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
<script>(function(d){{d.classList.add('js');try{{if(sessionStorage.getItem('fg-intro'))d.classList.add('no-loader')}}catch(e){{}}}})(document.documentElement)</script>
</head>
<body>
{LOADER if loader else ""}'''



def nav_links(active):
    items = [("Home", "index.html", "home"), ("About", "about.html", "about"), ("Services", "index.html#services", "services")]
    out = []
    for label, href, key in items:
        on = ' data-active aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}" data-nav="{key}"{on} class="{NAV}">{label}</a>')
    return "\n".join(out)


def header(active):
    return f'''<header class="sticky top-0 z-50 bg-sunny pt-[env(safe-area-inset-top)]">
<div class="{WRAP} max-w-6xl flex items-center justify-between gap-4 py-3 md:py-4">
<a href="index.html" aria-label="The Feelgood Co. home" class="flex-none"><img src="assets/img/logo.png" alt="The Feelgood Co." class="block h-10 w-auto md:h-[52px]"></a>
<nav aria-label="Main" class="flex items-center gap-5 sm:gap-8 md:gap-10">
{nav_links(active)}
</nav>
</div>
</header>
'''


def footer(active):
    return f'''<footer class="bg-sunny text-charcoal">
<div class="{WRAP} max-w-6xl flex flex-col gap-8 pb-[max(2.5rem,env(safe-area-inset-bottom))] pt-12">
<div class="grid grid-cols-1 items-center gap-6 md:grid-cols-[1fr_auto_1fr]">
<a href="index.html" aria-label="The Feelgood Co. home" class="justify-self-center md:justify-self-start"><img src="assets/img/logo.png" alt="The Feelgood Co." class="block h-16 w-auto md:h-[72px]"></a>
<nav aria-label="Footer" class="flex items-center justify-center gap-6 md:gap-8">
{nav_links(active)}
</nav>
<a href="#" aria-label="Instagram" class="flex size-11 items-center justify-center justify-self-center text-charcoal transition-colors duration-200 hover:text-cream md:justify-self-end"><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.3" fill="currentColor" stroke="none"/></svg></a>
</div>
<div class="flex flex-col items-center gap-1.5 border-t border-charcoal/20 pt-6 text-center">
<p class="text-[14px] tracking-[.04em]">Hospitality concepts, capabilities, experience and people.</p>
<p class="text-[12px] tracking-[.04em]">© 2026 The Feelgood Co. All rights reserved.</p>
</div>
</div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def bubble(left, size, colour, delay=0, dur=None, bottom=60, phone=False):
    extra = "" if phone else " max-md:hidden"
    extra += f" [animation-delay:{delay}s]" if delay else ""
    extra += f" [animation-duration:{dur}s]" if dur else ""
    return (f'<span aria-hidden="true" class="pointer-events-none absolute left-[{left}%] bottom-[-{bottom}px] size-[{size}px] '
            f'animate-rise rounded-full bg-{colour} opacity-0{extra}"></span>')


def bullet_list(items, extra=""):
    lis = "\n".join(f'<li class="reveal flex items-start gap-4 py-3.5"><span aria-hidden="true" class="mt-[9px] size-2.5 flex-none rounded-full bg-sunny"></span><span class="{BODY}">{e(t)}</span></li>' for t in items)
    return f'<ul class="divide-y divide-sage {extra}">\n{lis}\n</ul>'

def numbered_row(i, title, body_html, group=None):
    """Row used by services (expandable) and principles (static)."""
    num = f'<span aria-hidden="true" class="w-8 flex-none text-[14px] font-bold tabular-nums text-charcoal/70">{i + 1:02d}</span>'
    if group is None:
        return f'''<li class="reveal flex gap-5 border-sage py-6">
{num}
<div class="flex flex-col gap-1.5"><h3 class="{H3}">{e(title)}</h3>{body_html}</div>
</li>'''
    pid = f"{group}-{i}"
    return f'''<li class="reveal border-sage">
<h3><button type="button" data-acc data-acc-group="{group}" aria-expanded="false" aria-controls="{pid}" class="group group/btn flex min-h-16 w-full cursor-pointer touch-manipulation select-none items-center gap-5 py-5 text-left">
{num}
<span class="flex-1 {H3} transition-transform duration-300 ease-out group-hover:translate-x-1.5">{e(title)}</span>
<span aria-hidden="true" class="flex size-9 flex-none items-center justify-center rounded-full border border-charcoal/30 transition-colors duration-200 group-hover:border-sunny group-hover:bg-sunny group-aria-expanded/btn:border-sunny group-aria-expanded/btn:bg-sunny">{PLUS}</span>
</button></h3>
<div id="{pid}" inert class="{PANEL}">
<div class="overflow-hidden"><div class="flex max-w-3xl flex-col gap-3 pb-7 pl-[52px] md:pr-16">
{body_html}
</div></div>
</div>
</li>'''


def placeholder(img, alt, extra=""):
    return f'<img src="assets/img/ph-{img}.svg" alt="{e(alt)}" class="size-full object-cover {extra}" loading="lazy">'


def initials(name):
    parts = [w for w in name.replace("/", " ").split() if w.lower() != "the"]
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

# ------------------------------------------------------------------ content
STAGES = [
 ("Concept development", "Every business begins with a clear proposition.", [
  "We help define the concept, customer experience, market positioning, food and beverage offering, brand direction and commercial opportunity.",
  "This includes market research, competitor benchmarking, customer profiling, concept ideation and the development of a distinctive hospitality identity."]),
 ("Business planning & design", "Once the concept is established, we translate the vision into a practical business model.", [
  "This includes business planning, pricing strategy, operational requirements, menu development, kitchen planning, equipment recommendations, staffing structures and implementation planning.",
  "The objective is to create a concept that is both appealing to customers and operationally achievable."]),
 ("Team development & training", "People are central to the hospitality experience.", [
  "We support recruitment, team structures, standard operating procedures and practical training across kitchen, service and bar operations.",
  "Training covers product knowledge, recipes, service standards, operational routines, quality control and team coordination."]),
 ("Implementation & launch", "We help bring the concept to life.", [
  "Our involvement may include pre-opening coordination, menu testing, operational readiness, mock services, marketing campaigns, launch activations and hands-on support during opening.",
  "We focus on ensuring that the experience promised by the concept can be delivered consistently in practice."]),
 ("Post-implementation & optimisation", "Opening is the beginning of the next stage.", [
  "We review performance, customer feedback, product quality, costs, service standards and operational efficiency to identify opportunities for improvement.",
  "This may include menu engineering, pricing adjustments, staff development, marketing initiatives and operational restructuring.",
  "The insights gained feed into the next cycle of business development and growth."]),
]
SERVICES = [
 ("Concept & brand development", ["We develop hospitality concepts with a clear identity, relevant market positioning and a compelling customer experience.", "Services include concept creation, brand positioning, competitive analysis, customer journey development, food and beverage direction and creative strategy."]),
 ("Menu development & engineering", ["We create and refine menus that balance creativity, customer appeal, operational feasibility and profitability.", "Our work includes dish ideation, recipe development, ingredient sourcing, recipe costing, menu pricing, margin analysis, tastings, plating standards and menu optimisation.", "We also assess menu performance and identify opportunities to improve profitability, simplify execution and reduce waste."]),
 ("Kitchen & back-of-house development", ["We help build efficient kitchen operations that support the intended menu and service model.", "Services include kitchen workflow planning, equipment specifications, station design, procurement guidance, production systems, hygiene procedures, recipe documentation and back-of-house training."]),
 ("Front-of-house development", ["We help create service experiences that are welcoming, efficient and consistent.", "This includes service procedures, guest experience standards, staffing coordination, team training, service simulations and ongoing quality assessment."]),
 ("Bar & beverage development", ["We support beverage concepts through menu development, cocktail creation, costing, presentation, operational setup and bar team training.", "Our focus is on delivering a beverage experience that complements the wider concept while remaining practical and commercially sound."]),
 ("Marketing, programming & activations", ["We help hospitality businesses build awareness, connect with their audiences and create reasons for customers to visit.", "Services include marketing strategy, content direction, social media planning, launch campaigns, event programming, collaborations, pop-ups and temporary hospitality activations."]),
 ("Operations & management", ["We support the day-to-day and strategic requirements of hospitality operations.", "This includes operational reviews, staffing structures, procurement, cost control, performance management, service standards, quality assurance and continuous improvement."]),
 ("Corporate development & strategic advisory", ["We support business owners and investors in evaluating opportunities, planning expansion and developing sustainable growth strategies.", "Areas of focus include commercial planning, investment evaluation, partnership development, business development and strategic growth initiatives."]),
]
CAPS = ["Hospitality concept development and positioning", "Business planning and commercial strategy", "Food and beverage menu development and engineering", "Kitchen design and operational planning", "Recruitment, training and team development", "Front-of-house and back-of-house operations", "Bar and beverage development", "Brand development, marketing and activations", "Pre-opening planning and implementation", "Post-opening management and performance improvement", "Strategic advisory, investment and growth support"]
BRAND_CARDS = [
 ("Ramenara", "Upper-casual dining & bar", "Upper-casual dining and bar service, shaped by the founders' hands-on restaurant experience.", "bg-sunny"),
 ("Manos", "Upper-casual dining", "Upper-casual dining and sports-club food service, including Manos at The Rugby Club.", "bg-sage"),
 ("Zimari", "To be confirmed", "Part of the founders' hospitality portfolio. The full story will follow.", "bg-butter"),
 ("Ramenaki", "Pop-up", "An experiential dining pop-up built on creative, temporary hospitality.", "bg-terracotta"),
 ("The Phoenix / Bapco Club", "Heritage residency", "A heritage-led residency covering concept, food and beverage, programming and operations.", "bg-sunny"),
 ("Good Neighbour", "Menu development", "Menu and back-of-house development, from kitchen planning to culinary training.", "bg-sage"),
]
PHIL = [("A compelling idea.", "A concept that has a reason to exist and gives people a reason to visit."),
        ("Great execution.", "The people, products, systems and service standards that make the experience work."),
        ("A sustainable business.", "The commercial discipline required to operate, adapt and grow.")]
FOUNDERS = [
 ("Pavlos Babiolakis", "Co-founder | Operations & execution", ["Pavlos brings an operational perspective to hospitality development, with experience across restaurant operations, culinary execution, procurement, kitchen management and people development.", "His focus is on translating concepts into workable operating models and building the systems, teams and processes required to deliver them consistently."]),
 ("Ahmed Al Balooshi", "Co-founder | Concept & creative development", ["Ahmed focuses on the creative and experiential side of hospitality, including concept development, menu direction, culinary execution and customer experience.", "His work connects a concept's identity with the products, service and overall experience delivered to customers."]),
]
SPECIALISTS = [
 ("Farrah", "Marketing", ["Farrah supports the marketing and communications side of the business, helping translate hospitality concepts into clear, engaging messages and customer-facing campaigns.", "Her area of focus includes brand communications, content, marketing coordination and promotional activities."]),
 ("Amando Lazaro", "Back-of-house specialist", ["Amando specialises in culinary execution, recipe development, food costing and back-of-house training.", "He supports kitchen teams in translating menus into consistent, practical production systems, with a focus on quality, efficiency and operational readiness."]),
 ("Ivy Batino", "Front-of-house specialist", ["Ivy brings experience in project coordination, staffing, administration and front-of-house operations.", "Her focus includes service readiness, team coordination, guest-facing operations and the practical organisation required to deliver a consistent customer experience."]),
 ("John", "Bar specialist", ["John supports beverage execution, bar menu development and practical bar training.", "His role focuses on beverage preparation, consistency, presentation and developing the skills and systems needed for effective bar operations."]),
 ("Khalid", "Corporate development", ["Khalid supports the corporate development and strategic growth side of The Feelgood Company.", "His focus includes commercial planning, business development, partnership opportunities and supporting the wider growth and development of the business."]),
]
PRINCIPLES = [
 ("Creative thinking", "We believe strong concepts need originality, personality and a clear understanding of the customer."),
 ("Commercial discipline", "Every recommendation must consider operational feasibility, cost, profitability and long-term sustainability."),
 ("Hands-on execution", "We believe good ideas are only valuable when they can be implemented effectively."),
 ("Continuous improvement", "Hospitality businesses evolve, and we help them respond to changing customer expectations, operational realities and commercial opportunities."),
]
WORKWITH = ["Entrepreneurs developing their first concept", "Established restaurant and café operators", "Hospitality groups", "Investors", "Clubs", "Lifestyle destinations", "Businesses looking to reposition or improve their existing offering"]

BRAND_ART = ["bowl", "plate", "glass", "awning", "heritage", "pot"]


def stage_row(i, s):
    n = i + 1
    t, lead, paras = s
    left = i % 2 == 0
    col = "md:col-start-1 md:mr-8" if left else "md:col-start-3 md:ml-8"
    side = "tl-card-left" if left else "tl-card-right"
    ps = "\n".join(f'<p class="{SMALL}">{e(p)}</p>' for p in paras)
    return f'''<div id="stage-{n}" class="tl-row relative grid grid-cols-[56px_1fr] items-center md:grid-cols-[1fr_72px_1fr]">
<div class="relative z-10 col-start-1 row-start-1 flex justify-center md:col-start-2"><div class="rounded-full bg-cream p-2"><span class="tl-dot flex size-14 items-center justify-center rounded-full bg-sunny text-[24px] font-black" aria-hidden="true">{n}</span></div></div>
<div class="col-start-2 row-start-1 ml-4 md:ml-0 {col}">
<div class="tl-card {side} flex flex-col gap-3 rounded-3xl border border-sage bg-cream p-7 transition-colors duration-200 hover:bg-cream-deep md:p-8">
<p class="{LABEL}">Phase {n}</p>
<h3 class="{H3} md:text-[22px]">{e(t)}</h3>
<p class="text-[18px] leading-[1.5]">{e(lead)}</p>
{ps}
</div>
</div>
</div>'''


def brand_card(i, b):
    name, tag, line, _ = b
    return f'''<article class="reveal group">
<div class="relative aspect-[4/5] overflow-hidden rounded-[2rem] bg-cream-deep">
{placeholder(BRAND_ART[i % len(BRAND_ART)], f"Placeholder for {name} photography", "transition-transform duration-700 ease-out group-hover:scale-[1.04]")}
<span class="absolute bottom-4 left-4 flex translate-y-2 items-center gap-2 rounded-full bg-cream px-4 py-2 text-[14px] font-bold opacity-0 transition duration-300 ease-out group-hover:translate-y-0 group-hover:opacity-100 [@media(hover:none)]:translate-y-0 [@media(hover:none)]:opacity-100">{DOT}{e(tag)}</span>
</div>
<div class="mt-5 flex items-center gap-3">
<span aria-hidden="true" class="flex size-9 flex-none items-center justify-center rounded-xl border border-sage text-[14px] font-black">{initials(name)}</span>
<h3 class="{H3}">{e(name)}</h3>
</div>
<p class="mt-2 max-w-sm {SMALL}">{e(line)}</p>
</article>'''


def phil_row(p):
    return f'''<div class="reveal grid grid-cols-1 items-baseline gap-1 py-2 md:grid-cols-[240px_1fr] md:gap-8">
<h3 class="text-[18px] font-bold leading-snug text-sunny">{e(p[0])}</h3>
<p class="{BODY}">{e(p[1])}</p>
</div>'''


index = head("The Feelgood Co. | Hospitality concepts, capabilities, experience and people",
             "The Feelgood Company is a Bahrain-based hospitality and management consulting group. Website mockup.", loader=False) + header("home") + f'''
<main id="main">
<!-- Hero: three scenes on a virtual scroll; Charcoal confetti on load -->
<section id="hero" aria-label="The Feelgood Company introduction" class="hero-stage relative h-[calc(100svh-var(--header-h,72px))] min-h-[520px] overflow-hidden bg-cream">
<h1 class="sr-only">The Feelgood Company</h1>
<canvas id="confetti" aria-hidden="true" class="pointer-events-none absolute inset-0 size-full"></canvas>

<div id="scene-logo" class="hero-panel pointer-events-none absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
<button type="button" id="replay" aria-label="Replay the confetti" class="pointer-events-auto cursor-pointer touch-manipulation transition-transform duration-150 ease-out active:scale-[.98]"><img src="assets/img/logo.png" alt="The Feelgood Co. logo" class="block w-[260px] max-w-[62vw] md:w-[360px]"></button>
<a href="#who" id="cue" aria-label="Scroll to the next section" class="pointer-events-auto absolute bottom-8 left-1/2 flex -translate-x-1/2 touch-manipulation flex-col items-center gap-3 {LABEL}">Scroll
<span aria-hidden="true" class="flex size-11 animate-nudge items-center justify-center rounded-full bg-butter">{CHEVRON}</span></a>
</div>

<div id="scene-intro" class="hero-panel pointer-events-none absolute inset-0 flex flex-col items-center justify-center p-6 text-center opacity-0">
<p class="max-w-4xl text-[22px] font-light leading-[1.4] md:text-[34px]">The Feelgood Company is a Bahrain-based hospitality and management consulting group. We create, operate and grow distinctive food, beverage and lifestyle concepts.</p>
</div>

<div id="scene-philosophy" class="hero-panel pointer-events-none absolute inset-0 flex flex-col items-center justify-center gap-6 p-6 text-center opacity-0">
<h2 class="{H2}">Our philosophy</h2>
<div class="h-0.5 w-12 bg-sunny" aria-hidden="true"></div>
<p class="max-w-4xl text-[22px] font-light leading-[1.4] md:text-[34px]">The creativity of hospitality, with the discipline of business. Experiences that feel good for customers and make commercial sense for the business behind them.</p>
</div>
</section>

<!-- Who we are -->
<section id="who" class="bg-cream {SECTION}">
<div class="{WRAP} max-w-6xl grid grid-cols-1 items-center gap-12 md:grid-cols-2 md:gap-16">
<div class="flex flex-col gap-8">
{heading("Who we are")}
<div class="max-w-xl">
<div class="flex flex-col gap-5">
<p class="{P}">We bring together creative thinking, commercial understanding and hands-on operational expertise to help hospitality businesses go from first idea to sustainable operation.</p>
<p class="{P}">Whether we are developing a new concept, improving an existing business or bringing a temporary activation to life, our approach remains practical, collaborative and focused on execution.</p>
</div>
<div id="who-more" inert class="{PANEL}"><div class="overflow-hidden"><div class="flex flex-col gap-5 pt-5">
<p class="{BODY}">Our experience spans concept development, restaurant operations, food and beverage strategy, menu development, branding, marketing, team development and business advisory.</p>
<p class="{BODY}">We believe that great hospitality is about more than good food or attractive spaces. It is about creating an experience that people enjoy, remember and want to return to.</p>
</div></div></div>
</div>
<div class="reveal"><button type="button" data-acc data-acc-group="who" data-more="Read more" data-less="Read less" aria-expanded="false" aria-controls="who-more" class="{BTN}"><span data-label>Read more</span>{CHEVRON}</button></div>
</div>
<div class="reveal-img relative aspect-[4/5] overflow-hidden rounded-[2rem] bg-cream-deep md:aspect-[5/6]">{placeholder("interior", "Placeholder for interior photography")}</div>
</div>
</section>

<!-- What we do -->
<section id="what" class="relative overflow-hidden bg-cream-deep {SECTION}">
{bubble(6, 90, "sunny", phone=True)}
{bubble(30, 48, "sage", 3, 11, 40)}
{bubble(58, 72, "butter", 6, 16, 70)}
{bubble(88, 60, "sage", 8, 15)}
<div class="{WRAP} max-w-4xl relative z-10">
{heading("What we do")}
<div class="mt-8 flex max-w-4xl flex-col gap-5">
<p class="{P}">The Feelgood Company supports hospitality businesses throughout their entire development and operating journey.</p>
<p class="{P}">We work with entrepreneurs, investors, operators and established businesses to develop concepts, strengthen operations and identify opportunities for growth.</p>
<p class="{P}">Our involvement can begin at the earliest stages of an idea or at any point in an existing business's lifecycle.</p>
</div>
<div class="mx-auto mt-16 max-w-2xl">
<p class="reveal {LABEL}">Our core capabilities include</p>
{bullet_list(CAPS, "mt-5")}
<p class="{P} mt-10">Our strength is bringing these disciplines together into one coordinated approach.</p>
</div>
</div>
</section>

<!-- Lifecycle -->
<section id="lifecycle" class="bg-cream {SECTION}">
<div class="{WRAP} max-w-6xl grid grid-cols-1 items-center gap-10 md:grid-cols-[5fr_7fr] md:gap-12">
<div class="flex flex-col gap-8">
{heading("Our approach: the F&amp;B business lifecycle")}
<div class="flex flex-col gap-5">
<p class="reveal text-[20px] font-light leading-[1.45] md:text-[24px]">We see hospitality development as a continuous cycle rather than a one-time launch.</p>
<p class="{P}">Every successful concept requires a clear idea, a sound business plan, the right people, disciplined execution and a commitment to continuous improvement.</p>
</div>
</div>
<div class="reveal flex items-center justify-center">
{CYCLE}
</div>
</div>
<div class="{WRAP} max-w-6xl mt-16 md:mt-20">
<div id="tl" class="relative flex flex-col gap-8 md:gap-10">
<div aria-hidden="true" class="absolute bottom-0 left-7 top-0 w-[3px] -translate-x-1/2 bg-sage/50 md:left-1/2"></div>
<div id="tl-fill" aria-hidden="true" class="tl-fill absolute bottom-0 left-7 top-0 w-[3px] -translate-x-1/2 bg-sunny md:left-1/2"></div>
{chr(10).join(stage_row(i, s) for i, s in enumerate(STAGES))}
</div>
</div>
</section>

<!-- Services -->
<section id="services" class="bg-cream-deep {SECTION}">
<div class="{WRAP} max-w-6xl">
{heading("Our services")}
<p class="{P} mt-8 max-w-3xl">Eight ways we help, from the first concept to ongoing performance.</p>
<ul class="mt-12 divide-y divide-sage">
{chr(10).join(numbered_row(i, t, chr(10).join(f'<p class="{BODY}">{e(p)}</p>' for p in paras), "svc") for i, (t, paras) in enumerate(SERVICES))}
</ul>
</div>
</section>

<!-- Brands -->
<section id="brands" class="bg-cream {SECTION}">
<div class="{WRAP} max-w-6xl">
{heading("Brands &amp; hospitality experience")}
<p class="{P} mt-8 max-w-3xl">Experience from developing, operating and contributing to hospitality concepts across different formats.</p>
<div class="mt-12 grid grid-cols-1 gap-x-8 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join(brand_card(i, b) for i, b in enumerate(BRAND_CARDS))}
</div>
</div>
</section>

<!-- Vision and philosophy -->
<section id="vision" class="relative overflow-hidden bg-cream-deep {SECTION}">
{bubble(5, 80, "butter", 2, phone=True)}
{bubble(36, 46, "sunny", 6, 12, 50)}
{bubble(68, 90, "sage", 9, 17, 70)}
<div class="{WRAP} max-w-4xl relative z-10">
{heading("Our vision")}
<p class="reveal mt-8 max-w-4xl {LEAD}">Our ambition is to develop, support and grow hospitality businesses that combine memorable experiences with strong operational and commercial foundations.</p>
<div class="mt-8 flex max-w-4xl flex-col gap-5">
<p class="{P}">We want to be recognised as a trusted partner for hospitality entrepreneurs, operators and investors who value both creative thinking and practical execution.</p>
<p class="{P}">By combining our experience across brands, operations, food and beverage, marketing and corporate development, we aim to create businesses that customers enjoy and teams are proud to operate.</p>
</div>
<div class="mt-20 md:mt-24">{heading("The Feelgood philosophy")}</div>
<p class="{P} mt-8 max-w-4xl">We believe the best hospitality businesses bring together three things:</p>
<div class="mt-6 flex max-w-4xl flex-col gap-1">
{chr(10).join(phil_row(p) for p in PHIL)}
</div>
<div class="mt-8 flex max-w-4xl flex-col gap-5">
<p class="{P}">When these elements work together, good concepts become great businesses.</p>
<p class="{P}">That is what The Feelgood Company is here to help create.</p>
</div>
</div>
</section>
</main>
''' + footer("home")
(ROOT / "index.html").write_text(index, encoding="utf-8")

# ------------------------------------------------------------------ about


def person(p, big):
    name, role, paras = p
    if big:
        grid, tile, mono, nm = "md:grid-cols-[240px_1fr] md:gap-14", "w-[200px] md:w-[240px]", "text-[56px]", "text-[22px]"
    else:
        grid, tile, mono, nm = "sm:grid-cols-[168px_1fr] sm:gap-10", "w-[152px] sm:w-[168px]", "text-[40px]", H3
    ps = "\n".join(f'<p class="{SMALL}">{e(t)}</p>' for t in paras)
    return f'''<div class="reveal grid grid-cols-1 items-center gap-6 {grid}">
<div role="img" aria-label="Portrait of {e(name)} to follow" class="relative flex aspect-square {tile} items-center justify-center rounded-[2rem] bg-cream-deep {mono} font-black tracking-[.02em]">{initials(name)}</div>
<div class="flex max-w-2xl flex-col gap-2">
<h4 class="{nm} font-bold leading-snug">{e(name)}</h4>
<p class="{LABEL}">{e(role)}</p>
<div class="mt-2 flex flex-col gap-2">{ps}</div>
</div>
</div>'''


about = head("About | The Feelgood Co.", "Meet the Feelgood team: founders, specialists, how we work and who we work with.") + header("about") + f'''
<main id="main">
<section aria-labelledby="about-title" class="relative overflow-hidden bg-sage">
<span aria-hidden="true" class="pointer-events-none absolute -left-24 -top-28 size-80 rounded-full bg-cream/25"></span>
<span aria-hidden="true" class="pointer-events-none absolute -bottom-40 -right-16 size-[420px] rounded-full bg-cream/20"></span>
<span aria-hidden="true" class="pointer-events-none absolute right-[16%] top-12 size-6 rounded-full bg-sunny"></span>
<div class="{WRAP} max-w-6xl relative py-24 text-center md:py-32">
<h1 id="about-title" class="reveal text-[34px] font-black uppercase leading-[1.1] tracking-[.06em] md:text-[52px]">Meet the Feelgood team</h1>
</div>
</section>

<section class="bg-cream {SECTION}">
<div class="{WRAP}  max-w-4xl">
{heading("Our team")}
<h3 class="reveal mt-12 {LABEL}">Founders</h3>
<div class="mt-8 flex flex-col gap-14">
{chr(10).join(person(p, True) for p in FOUNDERS)}
</div>
<h3 class="reveal mt-20 {LABEL}">Specialist team</h3>
<div class="mt-8 flex flex-col gap-12">
{chr(10).join(person(p, False) for p in SPECIALISTS)}
</div>
</div>
</section>

<section class="bg-cream-deep {SECTION}">
<div class="{WRAP} max-w-4xl">
{heading("How we work")}
<div class="mt-8 flex max-w-4xl flex-col gap-5">
<p class="{P}">Every hospitality business has different needs, challenges and ambitions.</p>
<p class="{P}">Some clients come to us with an idea that needs to be developed. Others have an established operation that needs improvement, a menu that needs rethinking or a new opportunity they want to explore.</p>
<p class="{P}">We begin by understanding the business, its objectives and the people it serves. From there, we develop a practical scope of work, bring together the relevant expertise and remain involved through the stages required to deliver the intended outcome.</p>
<p class="{P}">Our approach is built around four principles:</p>
</div>
<ul class="mt-10 max-w-4xl divide-y divide-sage">
{chr(10).join(numbered_row(i, t, f'<p class="{BODY}">{e(d)}</p>') for i, (t, d) in enumerate(PRINCIPLES))}
</ul>
</div>
</section>

<section class="relative overflow-hidden bg-cream {SECTION}">
{bubble(8, 84, "butter", 2, phone=True)}
{bubble(52, 50, "sage", 5, 11, 40)}
{bubble(88, 96, "sunny", 1, 17, 70)}
<div class="{WRAP} max-w-4xl relative z-10">
{heading("Who we work with")}
<div class="mt-8 flex max-w-4xl flex-col gap-5">
<p class="{P}">The Feelgood Company works with businesses and individuals across the hospitality ecosystem.</p>
<p class="{P}">These may include:</p>
</div>
<div class="mx-auto mt-10 max-w-2xl">{bullet_list(WORKWITH)}</div>
<div class="mt-10 flex max-w-4xl flex-col gap-5">
<p class="{P}">We can support a complete development journey or provide specialist expertise for a specific challenge.</p>
<p class="{P}">Our involvement is shaped by the needs of each project.</p>
</div>
</div>
</section>
</main>
''' + footer("about")
(ROOT / "about.html").write_text(about, encoding="utf-8")
print("ok")
