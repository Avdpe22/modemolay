/* ============================================================
   Missouri DeMolay — shared behaviour for interior pages:
   mobile menu, sticky-nav shadow, and the "Show content gaps"
   review toggle. The homepage has its own inline script.
   ============================================================ */
(function(){
  // ---- content-gap review mode ----
  var gt = document.getElementById('gapToggle');
  if (gt) {
    gt.addEventListener('click', function(){
      var on = document.body.classList.toggle('show-gaps');
      gt.setAttribute('aria-pressed', on);
      gt.textContent = on ? 'Hide content gaps' : 'Show content gaps';
    });
  }

  // ---- sticky-nav shadow once the page has scrolled ----
  var nav = document.querySelector('nav.main'), ticking = false;
  function onScroll(){
    if (ticking) return; ticking = true;
    requestAnimationFrame(function(){
      if (nav) nav.classList.toggle('scrolled', window.pageYOffset > 40);
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();

  // ---- mobile slide-down menu ----
  var toggle = document.getElementById('navToggle'),
      panel  = document.getElementById('mobilenav'),
      reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      mqDesktop = window.matchMedia('(min-width:961px)'),
      closeTimer;

  if (toggle && panel) {
    var firstLink = panel.querySelector('a');
    function openMenu(){
      clearTimeout(closeTimer);
      panel.hidden = false;
      void panel.offsetHeight;
      panel.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      document.body.style.overflow = 'hidden';
      if (firstLink) try { firstLink.focus({ preventScroll:true }); } catch(e){ firstLink.focus(); }
    }
    function closeMenu(returnFocus){
      panel.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.body.style.overflow = '';
      closeTimer = setTimeout(function(){ if (!panel.classList.contains('open')) panel.hidden = true; }, reduce ? 0 : 320);
      if (returnFocus && toggle) toggle.focus();
    }
    toggle.addEventListener('click', function(){
      panel.classList.contains('open') ? closeMenu(true) : openMenu();
    });
    panel.addEventListener('click', function(e){ if (e.target.closest('a')) closeMenu(false); });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && panel.classList.contains('open')) closeMenu(true);
    });
    document.addEventListener('click', function(e){
      if (panel.classList.contains('open') && !panel.contains(e.target) && !toggle.contains(e.target)) closeMenu(false);
    });
    mqDesktop.addEventListener('change', function(e){
      if (e.matches && panel.classList.contains('open')) closeMenu(false);
    });
  }
})();
