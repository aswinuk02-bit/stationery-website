/* SHOWPIECE 1 — Hero "pen writes the headline".
   Motion only. The words come from whatever is inside .hero-headline; the pen is the
   .hero-pen element in the markup; cards are .hero-card; fade-ins are .hero-fade.
   Change the headline text or add cards in HTML and this just works. */
(function () {
  'use strict';
  var wrap = document.querySelector('.hero-headline-wrap');
  if (!wrap) return;
  var headline = wrap.querySelector('.hero-headline');
  var pen = wrap.querySelector('.hero-pen');
  var fades = document.querySelectorAll('.hero-fade');
  var cards = document.querySelectorAll('.hero-card');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function showAll() {
    document.documentElement.classList.remove('js-hero');
    headline.querySelectorAll('.w-in').forEach(function (w) { w.style.clipPath = 'none'; });
    headline.querySelectorAll('.hl-mark').forEach(function (m) { m.style.backgroundSize = '100% 100%'; });
    fades.forEach(function (f) { f.style.opacity = 1; f.style.transform = 'none'; });
  }
  if (reduce || !headline.animate) { showAll(); return; }

  /* split text nodes into words, keeping any inline elements (e.g. .hl-mark) intact */
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (child) {
      if (child.nodeType === 3) {
        var parts = child.textContent.split(/(\s+)/);
        var frag = document.createDocumentFragment();
        parts.forEach(function (p) {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
          var w = document.createElement('span'); w.className = 'w';
          var i = document.createElement('span'); i.className = 'w-in'; i.textContent = p;
          w.appendChild(i); frag.appendChild(w);
        });
        node.replaceChild(frag, child);
      } else if (child.nodeType === 1 && !child.classList.contains('w')) { splitWords(child); }
    });
  }
  headline.setAttribute('aria-label', headline.textContent.replace(/\s+/g, ' ').trim());
  splitWords(headline);
  var words = Array.prototype.slice.call(headline.querySelectorAll('.w-in'));
  words.forEach(function (w) { w.setAttribute('aria-hidden', 'true'); w.style.clipPath = 'inset(0 100% 0 0)'; });

  var marks = Array.prototype.slice.call(headline.querySelectorAll('.hl-mark'));
  var i = 0;
  var wrapBox;

  function penTo(x, y, tilt) {
    if (!pen) return;
    pen.style.opacity = 1;
    pen.style.transform = 'translate(' + (x - 6) + 'px,' + (y - 40) + 'px) rotate(' + tilt + 'deg)';
  }

  function writeWord() {
    if (i >= words.length) { finish(); return; }
    var w = words[i++];
    wrapBox = wrap.getBoundingClientRect();
    var box = w.getBoundingClientRect();
    var x0 = box.left - wrapBox.left, y = box.top - wrapBox.top + box.height * 0.78, width = box.width;
    var dur = Math.max(220, Math.min(620, width * 2.4));
    var start = performance.now();
    var anim = w.animate([{ clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)' }], { duration: dur, easing: 'cubic-bezier(.45,.05,.4,1)', fill: 'forwards' });
    (function track(now) {
      var p = Math.min(1, (now - start) / dur);
      var wobble = Math.sin(p * 18) * 2.2;
      penTo(x0 + width * p, y + wobble, -14 + Math.sin(p * 9) * 5);
      if (p < 1) requestAnimationFrame(track);
    })(start);
    anim.onfinish = function () {
      w.style.clipPath = 'none';
      var mark = w.closest('.hl-mark');
      if (mark && marks.indexOf(mark) > -1) {
        var all = mark.querySelectorAll('.w-in');
        if (all[all.length - 1] === w) mark.animate([{ backgroundSize: '0% 100%' }, { backgroundSize: '100% 100%' }], { duration: 450, easing: 'ease-out', fill: 'forwards' });
      }
      setTimeout(writeWord, 40);
    };
  }

  function finish() {
    if (pen) pen.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 500, delay: 250, fill: 'forwards' });
    fades.forEach(function (f, n) {
      f.animate([{ opacity: 0, transform: 'translateY(14px)' }, { opacity: 1, transform: 'none' }], { duration: 600, delay: n * 110, easing: 'ease-out', fill: 'forwards' });
    });
  }

  /* cards "assemble" onto the desk, then follow the pointer with a light parallax */
  cards.forEach(function (c, n) {
    var end = getComputedStyle(c).transform;
    c.animate([{ opacity: 0, transform: 'translateY(-60px) scale(1.15) rotate(0deg)' }, { opacity: 1, transform: end === 'none' ? 'none' : end }], { duration: 750, delay: 250 + n * 220, easing: 'cubic-bezier(.3,1.4,.5,1)', fill: 'backwards' });
  });
  var stack = document.querySelector('.hero-stack');
  if (stack && cards.length && window.matchMedia('(hover: hover)').matches) {
    stack.addEventListener('mousemove', function (e) {
      var r = stack.getBoundingClientRect();
      var dx = (e.clientX - r.left) / r.width - 0.5, dy = (e.clientY - r.top) / r.height - 0.5;
      cards.forEach(function (c, n) { var d = (n + 1) * 7; c.style.translate = (dx * d) + 'px ' + (dy * d) + 'px'; });
    });
  }

  function begin() { setTimeout(writeWord, 350); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(begin); else begin();
})();
