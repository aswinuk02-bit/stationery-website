/* SHOWPIECE 3 — Interactive desk category explorer.
   Behaviour only. Every .desk-item[data-category] in the scene is matched to the
   .desk-panel[data-category-panel] with the same value. Add an item + a panel in HTML
   and it works — no category names live in this file.
   Desktop: hover/focus previews, click follows the link. Touch: first tap previews. */
(function () {
  'use strict';
  document.querySelectorAll('.desk').forEach(function (desk) {
    var items = Array.prototype.slice.call(desk.querySelectorAll('.desk-item'));
    var panels = Array.prototype.slice.call(desk.querySelectorAll('.desk-panel'));
    if (!items.length || !panels.length) return;
    var touch = window.matchMedia('(hover: none)').matches;

    function show(key) {
      items.forEach(function (i) { i.classList.toggle('is-active', i.dataset.category === key); });
      panels.forEach(function (p) { p.hidden = p.dataset.categoryPanel !== key; });
    }

    items.forEach(function (item) {
      item.addEventListener('mouseenter', function () { show(item.dataset.category); });
      item.addEventListener('focus', function () { show(item.dataset.category); });
      item.addEventListener('click', function (e) {
        if (touch && !item.classList.contains('is-active')) { e.preventDefault(); show(item.dataset.category); }
      });
    });
    show(items[0].dataset.category);
  });
})();
