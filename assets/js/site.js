(function () {
  var b = document.querySelector('.burger'), m = document.getElementById('menu');
  if (b && m) b.addEventListener('click', function () {
    var o = m.classList.toggle('open'); b.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  // SMIL orbit dot ignores CSS media queries, so honour reduced motion here.
  try {
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)
      document.querySelectorAll('animateMotion').forEach(function (n) { n.remove(); });
  } catch (e) {}
})();

// Loading intro (reference GIF recreated in SVG/CSS): ~5.6 s, skippable, once per session.
(function () {
  var el = document.getElementById('intro'); if (!el) return;
  var done = false, t0 = Date.now();
  try { sessionStorage.setItem('aev_intro', '1'); } catch (e) {}
  function close() {
    if (done) return; done = true;
    el.classList.add('out'); document.documentElement.classList.remove('intro-on');
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 1000);
  }
  var skip = el.querySelector('.in-skip'); if (skip) skip.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') close(); });
  function go() { setTimeout(close, Math.max(0, 5600 - (Date.now() - t0))); }
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
  setTimeout(close, 9000); // never block the page longer than this
})();
