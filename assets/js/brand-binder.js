/* SHOWPIECE 2 — "Brand your binder" scroll sequence.
   Motion/behaviour only. Steps are .brand-step elements in the markup. Each step declares
   what the binder should look like using data attributes:
       data-binder-color="#123456"   -> sets --binder-color on .brand-binder
       data-logo="on|off"            -> copied to .brand-binder[data-logo]
       data-finish="none|foil"       -> copied to .brand-binder[data-finish]
   Add a step in HTML (with its own data attributes) and it is picked up automatically:
   scroll length, progress and active state are all derived from the number of steps. */
(function () {
  'use strict';
  var section = document.querySelector('.brand');
  if (!section) return;
  var scroller = section.querySelector('.brand-scroll');
  var binder = section.querySelector('.brand-binder');
  var steps = Array.prototype.slice.call(section.querySelectorAll('.brand-step'));
  var swatches = Array.prototype.slice.call(section.querySelectorAll('.brand-swatch'));
  if (!scroller || !binder || !steps.length) return;

  section.style.setProperty('--steps', steps.length);
  var current = -1;

  function apply(idx) {
    if (idx === current) return;
    current = idx;
    steps.forEach(function (s, n) { s.classList.toggle('is-active', n === idx); });
    var s = steps[idx];
    var d = s.dataset;
    if (d.binderColor) binder.style.setProperty('--binder-color', d.binderColor);
    ['logo', 'finish'].forEach(function (k) { if (d[k] !== undefined) binder.dataset[k] = d[k]; });
    swatches.forEach(function (sw) { sw.classList.toggle('is-active', !!d.binderColor && sw.dataset.color === d.binderColor); });
  }

  function onScroll() {
    var r = scroller.getBoundingClientRect();
    var total = r.height - window.innerHeight;
    var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    apply(Math.min(steps.length - 1, Math.floor(p * steps.length)));
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  steps.forEach(function (s, n) {
    s.addEventListener('click', function () {
      var r = scroller.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var target = window.scrollY + r.top + total * ((n + 0.5) / steps.length);
      window.scrollTo({ top: target, behavior: 'smooth' });
    });
  });
  onScroll();
  if (current === -1) apply(0);
})();
