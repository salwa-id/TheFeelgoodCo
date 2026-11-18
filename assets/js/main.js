(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- More / Read more toggles ---------- */
  document.querySelectorAll("[data-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.getElementById(btn.getAttribute("data-toggle"));
      if (!target) return;
      var open = target.classList.toggle("hidden") === false;
      var disp = btn.getAttribute("data-display");
      if (disp) target.classList.toggle(disp, open);
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? btn.getAttribute("data-less") : btn.getAttribute("data-more");
    });
  });

  /* ---------- Expandable panels (services, principles, "Read more"): one open per group ---------- */
  var setAcc = function (btn, open) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    if (!panel) return;
    btn.setAttribute("aria-expanded", String(open));
    panel.classList.toggle("grid-rows-[1fr]", open);
    panel.classList.toggle("grid-rows-[0fr]", !open);
    if (open) panel.removeAttribute("inert"); else panel.setAttribute("inert", "");
    var label = btn.querySelector("[data-label]");
    if (label && btn.dataset.more) label.textContent = open ? btn.dataset.less : btn.dataset.more;
  };
  document.querySelectorAll("[data-acc]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      var group = btn.dataset.accGroup;
      document.querySelectorAll('[data-acc][aria-expanded="true"]').forEach(function (o) {
        if (o !== btn && o.dataset.accGroup === group) setAcc(o, false);
      });
      setAcc(btn, !open);
    });
  });

  /* ---------- Nav: "Services" lights up while the services section is on screen ---------- */
  var navLinks = document.querySelectorAll("[data-nav]");
  var servicesEl = document.getElementById("services");
  if (servicesEl && navLinks.length && "IntersectionObserver" in window) {
    var setActive = function (key) {
      navLinks.forEach(function (a) {
        if (a.getAttribute("data-nav") === key) a.setAttribute("data-active", ""); else a.removeAttribute("data-active");
      });
    };
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { setActive(en.isIntersecting ? "services" : "home"); });
    }, { rootMargin: "-40% 0px -55% 0px" }).observe(servicesEl);
  }

  /* ---------- Fade-up on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal, .reveal-bar, .reveal-img, .reveal-dot");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      var visible = entries.filter(function (en) { return en.isIntersecting; });
      visible.forEach(function (en, i) {
        if (en.target.__img) { en.target.__img.classList.add("is-in"); io.unobserve(en.target); return; }
        en.target.style.transitionDelay = ((i % 5) * 60) + "ms";
        en.target.classList.add("is-in");
        io.unobserve(en.target);
        (function (el) { setTimeout(function () { el.style.transitionDelay = ""; }, 1200); })(en.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) {
      if (el.classList.contains("reveal-img") && el.parentElement) { el.parentElement.__img = el; io.observe(el.parentElement); }
      else io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Lifecycle timeline: line draws as you scroll ---------- */
  var tl = document.getElementById("tl");
  var fill = document.getElementById("tl-fill");
  if (tl && fill) {
    var rows = Array.prototype.slice.call(tl.querySelectorAll(".tl-row"));
    var ticking = false;
    var update = function () {
      ticking = false;
      var r = tl.getBoundingClientRect();
      var tip = window.innerHeight * 0.62;
      var p = Math.min(Math.max((tip - r.top) / r.height, 0), 1);
      if (reduceMotion) p = 1;
      fill.style.transform = "scaleY(" + p + ")";
      var tipY = r.top + p * r.height;
      rows.forEach(function (row) {
        var d = row.querySelector(".tl-dot").getBoundingClientRect();
        var cy = d.top + d.height / 2;
        if (reduceMotion || cy <= tipY) row.classList.add("is-on"); // stays once revealed
      });
    };
    var onScroll = function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  }

  /* ---------- Hero: three scenes on a virtual scroll ---------- */
  var heroEl = document.getElementById("hero");
  var headerEl = document.querySelector("body > header");
  var setHeaderH = function () {
    if (headerEl) document.documentElement.style.setProperty("--header-h", headerEl.offsetHeight + "px");
  };
  setHeaderH();
  window.addEventListener("resize", setHeaderH);

  var scenes = ["scene-logo", "scene-intro", "scene-philosophy"].map(function (id) { return document.getElementById(id); });
  if (heroEl && scenes.every(Boolean) && !reduceMotion) {
    var TRAVEL = 1800; // virtual scroll distance for the whole sequence
    var clamp = function (x, a, b) { return Math.max(a, Math.min(b, x)); };
    var smooth = function (x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
    var target = 0, current = 0, rafId = 0, lastY = 0;

    var sceneOpacity = function (i, p) {
      var introIn = smooth((p - 0.07) / 0.31);
      var philIn = smooth((p - 0.49) / 0.34);
      if (i === 0) return 1 - introIn;
      if (i === 1) return introIn * (1 - philIn);
      return philIn;
    };
    var renderScenes = function (p) {
      scenes.forEach(function (el, i) {
        var a = sceneOpacity(i, p);
        el.style.opacity = a;
        el.style.transform = "translateY(" + ((1 - a) * 8).toFixed(2) + "px)";
        el.style.visibility = a < 0.01 ? "hidden" : "visible";
        el.setAttribute("aria-hidden", a < 0.01 ? "true" : "false");
      });
    };
    var heroTick = function () {
      current += (target - current) * 0.12;
      if (Math.abs(target - current) < 0.0005) current = target;
      renderScenes(current);
      rafId = current !== target ? requestAnimationFrame(heroTick) : 0;
    };
    // only take over while the page is at the very top; at either end the event passes through
    var scrub = function (delta, e) {
            if (document.documentElement.classList.contains("is-loading")) { e.preventDefault(); return; }
      if (window.scrollY > 1) return;
      var next = clamp(target + delta / TRAVEL, 0, 1);
      if (next === target) return;
      e.preventDefault();
      target = next;
      if (!rafId) rafId = requestAnimationFrame(heroTick);
    };
    window.addEventListener("wheel", function (e) { if (!e.ctrlKey) scrub(e.deltaY, e); }, { passive: false });
    window.addEventListener("touchstart", function (e) { lastY = e.touches[0].clientY; }, { passive: true });
    window.addEventListener("touchmove", function (e) {
      var y = e.touches[0].clientY;
      scrub((lastY - y) * 1.6, e);
      lastY = y;
    }, { passive: false });
    window.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "PageDown" || (e.key === " " && !e.shiftKey)) scrub(220, e);
      else if (e.key === "ArrowUp" || e.key === "PageUp" || (e.key === " " && e.shiftKey)) scrub(-220, e);
    });
    var cue = document.getElementById("cue");
    if (cue) {
      cue.addEventListener("click", function (e) {
        e.preventDefault();
        target = current = 1;
        renderScenes(1);
        document.getElementById("who").scrollIntoView({ behavior: "smooth" });
      });
    }
    renderScenes(0);
  }

    /* ---------- Bubbles: Charcoal circles fall slowly from the top once, sway a little, fade out in the lower third ---------- */
  var canvas = document.getElementById("confetti");
  if (canvas) {
    var ctx = canvas.getContext("2d");
    var COLOUR = "#57534E";   // Charcoal
    var AMOUNT = 35;          // bubbles released in total
    var SIZE = 20;            // largest bubble, in px (smallest is about a third of this)
    var SPEED = 7;            // 1 = very slow ... 10 = fast
    var RELEASE_MS = 2500;    // bubbles are released over this long
    var W = 0, H = 0, bubbles = [], raf = 0, last = 0, releaseEnd = 0, released = 0;
    var rand = function (a, b) { return a + Math.random() * (b - a); };

    var resize = function () {
      var box = canvas.parentElement.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = box.width; H = box.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    var makeBubble = function () {
      var maxR = SIZE / 2, r = rand(maxR * 0.35, maxR);
      return {
        x: rand(0, W), y: -r - rand(0, 40), r: r,
        vy: SPEED * 0.18 * rand(0.7, 1.3) * (0.6 + (r / maxR) * 0.5),  // bigger ones fall a touch faster
        sway: rand(8, 22), phase: rand(0, 6.28), freq: rand(0.0006, 0.0012),
        alpha: rand(0.55, 0.9), age: 0
      };
    };

    var frame = function (t) {
      var ms = Math.min(t - last, 50), dt = ms / 16.67;
      last = t;
      if (t < releaseEnd) {
        var due = Math.round(AMOUNT * (1 - (releaseEnd - t) / RELEASE_MS));
        while (released < due) { bubbles.push(makeBubble()); released++; }
      }
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = COLOUR;
      for (var i = bubbles.length - 1; i >= 0; i--) {
        var b = bubbles[i];
        b.age += ms;
        b.y += b.vy * dt;
        var fadeIn = Math.min(1, b.age / 600);
        var fadeOut = Math.max(0, Math.min(1, (H * 0.92 - b.y) / (H * 0.35)));
        if (fadeOut <= 0) { bubbles.splice(i, 1); continue; }
        ctx.globalAlpha = b.alpha * fadeIn * fadeOut;
        ctx.beginPath();
        ctx.arc(b.x + Math.sin(b.phase + b.age * b.freq) * b.sway, b.y, b.r, 0, 6.2832);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      if (bubbles.length || t < releaseEnd) raf = requestAnimationFrame(frame);
      else { raf = 0; ctx.clearRect(0, 0, W, H); }
    };

    var fire = function () {
      resize();
      bubbles = []; released = 0;
      releaseEnd = performance.now() + RELEASE_MS;
      if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
    };

    window.addEventListener("resize", resize);
    document.addEventListener("fg:ready", function () { if (!reduceMotion) fire(); }, { once: true });

    var replay = document.getElementById("replay");
    if (replay) {
      replay.addEventListener("click", function () { if (!reduceMotion) fire(); });
    }
  }
  
  /* ---------- Intro screen: shows once per visit (not on Home), then the bubbles fall ---------- */
  (function () {
    var root = document.documentElement;
    var loader = document.getElementById("loader");
    var ready = function () { document.dispatchEvent(new Event("fg:ready")); };
    var seen = function () { try { sessionStorage.setItem("fg-intro", "1"); } catch (e) {} };
    if (!loader || getComputedStyle(loader).display === "none") { seen(); ready(); return; }
    root.classList.add("is-loading");
    var MIN = 400, MAX = 3500, start = performance.now(), finished = false;
    var finish = function () {
      if (finished) return;
      finished = true;
      seen();
      loader.setAttribute("data-done", "");
      setTimeout(function () { root.classList.remove("is-loading"); ready(); }, 450);
      setTimeout(function () { loader.remove(); }, 950);
    };
    var whenLoaded = function () { setTimeout(finish, Math.max(0, MIN - (performance.now() - start))); };
    if (document.readyState === "complete") whenLoaded(); else window.addEventListener("load", whenLoaded, { once: true });
    setTimeout(finish, MAX);
  })();
})();
