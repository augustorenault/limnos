/**
 * Lightbox leve e sem dependencias.
 * Intercepta cliques na galeria de imagens (.mpi-gallery) e exibe a imagem
 * ampliada em um overlay, com navegacao por grupo (data-fancybox), teclado
 * e fechar ao clicar fora. Links de paginas relacionadas sao ignorados.
 */
(function () {
  'use strict';

  function init() {
    var links = Array.prototype.slice.call(
      document.querySelectorAll('.mpi-gallery a.lightbox, .mpi-gallery a[data-fancybox]')
    );
    if (!links.length) return;

    var overlay = document.createElement('div');
    overlay.className = 'lb-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML =
      '<button class="lb-close" type="button" aria-label="Fechar">\u00d7</button>' +
      '<button class="lb-prev" type="button" aria-label="Imagem anterior">\u2039</button>' +
      '<figure class="lb-figure">' +
        '<img class="lb-image" alt="">' +
        '<figcaption class="lb-caption"></figcaption>' +
      '</figure>' +
      '<button class="lb-next" type="button" aria-label="Pr\u00f3xima imagem">\u203a</button>';
    document.body.appendChild(overlay);

    var imgEl = overlay.querySelector('.lb-image');
    var capEl = overlay.querySelector('.lb-caption');
    var group = [];
    var index = 0;

    function show(i) {
      if (!group.length) return;
      index = (i + group.length) % group.length;
      var a = group[index];
      imgEl.src = a.getAttribute('href');
      var caption =
        a.getAttribute('data-caption') || a.getAttribute('title') || '';
      imgEl.alt = caption;
      capEl.textContent = caption;
      capEl.style.display = caption ? '' : 'none';
    }

    function open(a) {
      var name = a.getAttribute('data-fancybox');
      group = name
        ? links.filter(function (l) {
            return l.getAttribute('data-fancybox') === name;
          })
        : [a];
      overlay.classList.toggle('is-single', group.length < 2);
      show(group.indexOf(a));
      overlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      overlay.classList.remove('is-open');
      document.body.style.overflow = '';
      imgEl.src = '';
    }

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        open(a);
      });
    });

    overlay.querySelector('.lb-close').addEventListener('click', close);
    overlay.querySelector('.lb-prev').addEventListener('click', function (e) {
      e.stopPropagation();
      show(index - 1);
    });
    overlay.querySelector('.lb-next').addEventListener('click', function (e) {
      e.stopPropagation();
      show(index + 1);
    });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.classList.contains('lb-figure')) {
        close();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (!overlay.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(index - 1);
      else if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
