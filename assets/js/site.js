/* Site behaviour (menu, forms, gallery, reveal). No content lives in this file:
   everything reads from markup via data-* attributes, so it survives the move to Elementor. */
(function () {
  'use strict';
  var doc = document;
  var body = doc.body;

  /* ---------- mobile drawer ---------- */
  var toggle = doc.querySelector('.nav-toggle');
  var drawer = doc.querySelector('.mobile-drawer');
  var scrim = doc.querySelector('.drawer-scrim');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    if (scrim) scrim.classList.toggle('is-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
    body.style.overflow = open ? 'hidden' : '';
    if (open) { var first = drawer.querySelector('a, summary, button'); if (first) first.focus(); }
    else if (toggle) toggle.focus();
  }
  if (toggle && drawer) {
    toggle.addEventListener('click', function () { setDrawer(!drawer.classList.contains('is-open')); });
    doc.querySelectorAll('[data-drawer-close]').forEach(function (el) { el.addEventListener('click', function () { setDrawer(false); }); });
    drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setDrawer(false); }); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && drawer.classList.contains('is-open')) setDrawer(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1060 && drawer.classList.contains('is-open')) setDrawer(false); });
  }

  /* ---------- mega menu (click for touch / keyboard, hover handled in CSS) ---------- */
  doc.querySelectorAll('.nav-item--mega > .nav-link').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  doc.addEventListener('click', function (e) {
    doc.querySelectorAll('.nav-item--mega.is-open').forEach(function (item) {
      if (!item.contains(e.target)) { item.classList.remove('is-open'); item.firstElementChild.setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------- scroll reveal ---------- */
  var reveals = doc.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('is-in'); }); }

  /* ---------- prefill forms from ?product=...&qty=... ---------- */
  var params = new URLSearchParams(window.location.search);
  doc.querySelectorAll('[data-prefill]').forEach(function (field) {
    var v = params.get(field.getAttribute('data-prefill'));
    if (v) field.value = v;
  });

  /* ---------- mailto forms: any <form data-mailto="addr"> ---------- */
  doc.querySelectorAll('form[data-mailto]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.type === 'submit' || el.type === 'button') return;
        if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
        var label = el.getAttribute('data-label') || (el.labels && el.labels[0] ? el.labels[0].textContent.replace('*', '').trim() : el.name);
        var val = (el.type === 'checkbox') ? 'Yes' : el.value;
        if (String(val).trim() !== '') lines.push(label + ': ' + val);
      });
      var subject = form.getAttribute('data-subject') || 'Website enquiry';
      var href = 'mailto:' + form.getAttribute('data-mailto') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      var status = form.querySelector('.form-status');
      if (status) status.textContent = 'Opening your email app with the details filled in… just press Send.';
      window.location.href = href;
    });
  });

  /* ---------- product gallery: .gallery [data-gallery-thumb] swaps .gallery-main img ---------- */
  doc.querySelectorAll('.gallery').forEach(function (g) {
    var main = g.querySelector('.gallery-main img');
    g.querySelectorAll('[data-gallery-thumb]').forEach(function (t) {
      t.addEventListener('click', function () {
        var src = t.getAttribute('data-gallery-thumb');
        main.src = src; main.alt = t.getAttribute('data-alt') || main.alt;
        g.querySelectorAll('.gallery-thumb').forEach(function (x) { x.classList.remove('is-active'); });
        t.classList.add('is-active');
      });
    });
  });

  /* ---------- product options -> quote + whatsapp links ---------- */
  var product = doc.querySelector('[data-product]');
  if (product) {
    var name = product.getAttribute('data-product');
    var chosen = {};
    var quote = doc.querySelectorAll('[data-quote-link]');
    var wa = doc.querySelectorAll('[data-wa-link]');
    var update = function () {
      var bits = Object.keys(chosen).map(function (k) { return k + ': ' + chosen[k]; });
      quote.forEach(function (a) {
        var u = new URL(a.getAttribute('data-quote-link'), window.location.href);
        u.searchParams.set('product', name);
        if (bits.length) u.searchParams.set('details', bits.join(', '));
        a.href = u.pathname.split('/').pop() + u.search + '#quote';
      });
      wa.forEach(function (a) {
        var base = a.getAttribute('data-wa-link');
        a.href = base + encodeURIComponent('Hi, I would like a quote for: ' + name + (bits.length ? ' (' + bits.join(', ') + ')' : '') + '.');
      });
    };
    product.querySelectorAll('.option-group').forEach(function (group) {
      var key = group.getAttribute('data-option');
      var valueLabel = group.querySelector('.option-label span');
      var setActive = function (btn) {
        group.querySelectorAll('.option').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        chosen[key] = btn.getAttribute('data-value');
        if (valueLabel) valueLabel.textContent = chosen[key];
        update();
      };
      group.querySelectorAll('.option').forEach(function (btn) { btn.addEventListener('click', function () { setActive(btn); }); });
      var pre = group.querySelector('.option[aria-pressed="true"]');
      if (pre) setActive(pre);
    });
    update();
  }

  /* ---------- footer year ---------- */
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
