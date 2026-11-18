(function () {
  var b = document.querySelector('.burger'), m = document.getElementById('menu');
  function setMenu(open) { m.classList.toggle('open', open); b.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  if (b && m) {
    b.addEventListener('click', function () { setMenu(!m.classList.contains('open')); });
    // Esc closes the mobile menu and returns focus to the button that opened it.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && m.classList.contains('open')) { setMenu(false); b.focus(); }
    });
  }
  // SMIL orbit dot ignores CSS media queries, so honour reduced motion here.
  try {
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)
      document.querySelectorAll('animateMotion').forEach(function (n) { n.remove(); });
  } catch (e) {}
  // The status legend on /research/ is folded on narrow screens; a link to #legend opens it.
  var lg = document.querySelector('.legend-box');
  function openLegend() { if (lg && location.hash === '#legend') lg.open = true; }
  openLegend(); window.addEventListener('hashchange', openLegend);
})();

// Loading intro (reference GIF recreated in SVG/CSS): about 2.4 s, skippable (button, click/tap, Esc/Enter/Space),
// once per device. The head script in build.py (INTRO_HEAD) decides whether html.intro-on is set.
(function () {
  var el = document.getElementById('intro'); if (!el) return;
  var root = document.documentElement;
  var hidden = false;
  try { hidden = getComputedStyle(el).display === 'none'; } catch (e) {}
  // Not shown (no intro-on, or hidden by prefers-reduced-motion even with ?intro): drop it and block nothing.
  if (!root.classList.contains('intro-on') || hidden) { root.classList.remove('intro-on'); el.parentNode.removeChild(el); return; }
  try { localStorage.setItem('aev_intro', '1'); } catch (e) { try { sessionStorage.setItem('aev_intro', '1'); } catch (e2) {} }
  var done = false, now = function () { return window.performance && performance.now ? performance.now() : Date.now(); }, t0 = now();
  var behind = document.querySelectorAll('header.nav, main, footer.foot, .skip');
  behind.forEach(function (n) { n.setAttribute('inert', ''); });
  var skip = el.querySelector('.in-skip');
  if (skip) try { skip.focus({ preventScroll: true }); } catch (e) { skip.focus(); }
  function close() {
    if (done) return; done = true;
    var hadFocus = el.contains(document.activeElement);
    behind.forEach(function (n) { n.removeAttribute('inert'); });
    el.classList.add('out'); root.classList.remove('intro-on');
    if (hadFocus) {
      var main = document.getElementById('main');
      if (main) try { main.focus({ preventScroll: true }); } catch (e) { main.focus(); }
    }
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 500);
  }
  el.addEventListener('click', close);  // anywhere on the overlay, the skip button included
  document.addEventListener('keydown', function (e) {
    if (!done && (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); close(); }
    else if (!done && e.key === 'Tab' && skip) { e.preventDefault(); skip.focus(); }  // keep focus on the overlay while it is shown
  });
  // Auto-close is timed from the moment the intro's CSS animations actually start, not from script start: on a cold
  // cache they can start more than a second late, and the tagline (last to appear, ~2.2 s in) must be seen.
  var SHOW = 2500, CAP = 4000, timer = null;
  function startedAt(a0) {
    if (timer !== null || done) return;
    timer = setTimeout(close, Math.max(0, Math.min(a0 + SHOW, t0 + CAP) - now()));
  }
  try {  // already running when this deferred script runs? (startTime is on the same clock as performance.now)
    var a = el.querySelector('.in-sky').getAnimations()[0];
    if (a && a.startTime !== null && typeof performance !== 'undefined') startedAt(a.startTime);
  } catch (e) {}
  el.addEventListener('animationstart', function () { startedAt(now()); });
  setTimeout(close, CAP); // never block the page longer than this
})();
