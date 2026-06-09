/**
 * Atualiza data-max dos contadores da home com base na média desde 1991.
 * Roda antes do numscroller para cada visita refletir o momento atual.
 */
(function () {
  var grid = document.querySelector('[data-metrics-live]');
  if (!grid) return;

  var start = Number(grid.dataset.metricsStart);
  var rates = {
    clientes: Number(grid.dataset.rateClientes),
    amostras: Number(grid.dataset.rateAmostras),
    analises: Number(grid.dataset.rateAnalises),
  };

  if (!start || !rates.clientes) return;

  function elapsedSec() {
    return Math.max(0, (Date.now() - start) / 1000);
  }

  function compute() {
    var sec = elapsedSec();
    return {
      clientes: Math.floor(rates.clientes * sec),
      amostras: Math.floor(rates.amostras * sec),
      analises: Math.floor(rates.analises * sec),
    };
  }

  function scrollerCfg(max, targetMs) {
    var steps = 100;
    var increment = Math.max(1, Math.floor(max / steps));
    var ms = targetMs || 2500;
    var delay = Math.max(1, Math.ceil((ms * increment) / 1000));
    return { increment: increment, delay: delay };
  }

  function apply() {
    var values = compute();
    grid.querySelectorAll('[data-metric]').forEach(function (el) {
      var key = el.getAttribute('data-metric');
      var val = values[key];
      if (val == null) return;
      var targetMs = Number(el.getAttribute('data-scroll-ms')) || 2500;
      var cfg = scrollerCfg(val, targetMs);
      el.setAttribute('data-max', String(val));
      el.setAttribute('data-increment', String(cfg.increment));
      el.setAttribute('data-delay', String(cfg.delay));
      if (!el.classList.contains('isShown')) {
        el.textContent = val.toLocaleString('pt-BR');
      }
    });
  }

  apply();

  var ticking = false;
  window.addEventListener(
    'scroll',
    function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        apply();
        ticking = false;
      });
    },
    { passive: true }
  );

  setInterval(apply, 60_000);
})();
