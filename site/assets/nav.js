/* Honorbrook header menu: click/tap dropdowns on desktop, hamburger + accordion on mobile. */
(function () {
  'use strict';
  var header = document.querySelector('header');
  var menu = document.getElementById('site-menu');
  if (!header || !menu) return;
  var toggle = header.querySelector('.nav-toggle');
  var items = menu.querySelectorAll('.has-dd');

  function setOpen(item, open) {
    item.classList.toggle('open', open);
    item.querySelector('.dd-t').setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function closeAll(except) {
    for (var i = 0; i < items.length; i++) if (items[i] !== except) setOpen(items[i], false);
  }
  function setMenu(open) {
    header.classList.toggle('nav-open', open);
    if (toggle) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    if (!open) closeAll();
  }

  for (var i = 0; i < items.length; i++) {
    items[i].querySelector('.dd-t').addEventListener('click', function (e) {
      var item = e.currentTarget.parentNode, open = !item.classList.contains('open');
      closeAll(item);
      setOpen(item, open);
    });
    items[i].addEventListener('mouseenter', function (e) {
      if (!header.classList.contains('nav-open')) closeAll(e.currentTarget);
    });
  }
  if (toggle) toggle.addEventListener('click', function () { setMenu(!header.classList.contains('nav-open')); });

  document.addEventListener('click', function (e) {
    if (!header.contains(e.target)) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var open = menu.querySelector('.has-dd.open .dd-t');
      setMenu(false);
      if (open) open.focus();
    }
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.dd a')) setMenu(false);
  });
})();
