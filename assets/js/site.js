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
