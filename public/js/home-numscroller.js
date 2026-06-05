/**
 * Contadores animados da homepage (plugin scrollzip / numscroller do site original).
 * Requer jQuery.
 */
(function ($) {
  if (!$ || !$('.numscroller').length) return;

  function numberRoller(slno) {
    var min = $('.roller-title-number-' + slno).attr('data-min'),
      max = $('.roller-title-number-' + slno).attr('data-max'),
      delay = $('.roller-title-number-' + slno).attr('data-delay');
    numberRoll(
      slno,
      min,
      max,
      $('.roller-title-number-' + slno).attr('data-increment'),
      (1000 * delay) / (max - min)
    );
  }

  function numberRoll(slno, min, max, increment, timeout) {
    min = parseInt(min, 10);
    max = parseInt(max, 10);
    increment = parseInt(increment, 10);
    if (min <= max) {
      $('.roller-title-number-' + slno).html(formatNumber(min));
      min += increment;
      setTimeout(function () {
        numberRoll(slno, min, max, increment, timeout);
      }, timeout);
    } else {
      $('.roller-title-number-' + slno).html(formatNumber(max));
    }
  }

  function formatNumber(number) {
    return parseInt(number, 10).toLocaleString('pt-BR');
  }

  $(window).on('load', function () {
    $(document).scrollzipInit();
    $(document).rollerInit();
  });

  $(window).on('load scroll resize', function () {
    $('.numscroller').scrollzip({
      showFunction: function () {
        numberRoller($(this).attr('data-slno'));
      },
      wholeVisible: false,
    });
  });

  $.fn.scrollzipInit = function () {
    $('body').prepend(
      "<div style='position:fixed;top:0px;left:0px;width:0;height:0;' id='scrollzipPoint'></div>"
    );
  };

  $.fn.rollerInit = function () {
    var t = 0;
    $('.numscroller').each(function () {
      t++;
      $(this).attr('data-slno', t);
      $(this).addClass('roller-title-number-' + t);
    });
  };

  $.fn.scrollzip = function (opts) {
    var settings = $.extend(
      {
        showFunction: null,
        hideFunction: null,
        showShift: 0,
        wholeVisible: false,
        hideShift: 0,
      },
      opts
    );
    return this.each(function () {
      $(this).addClass('scrollzip');
      if (
        $.isFunction(settings.showFunction) &&
        !$(this).hasClass('isShown') &&
        $(window).outerHeight() + $('#scrollzipPoint').offset().top - settings.showShift >
          $(this).offset().top + (settings.wholeVisible ? $(this).outerHeight() : 0) &&
        $('#scrollzipPoint').offset().top + (settings.wholeVisible ? $(this).outerHeight() : 0) <
          $(this).outerHeight() + $(this).offset().top - settings.showShift
      ) {
        $(this).addClass('isShown');
        settings.showFunction.call(this);
      }
      if (
        $.isFunction(settings.hideFunction) &&
        $(this).hasClass('isShown') &&
        ($(window).outerHeight() + $('#scrollzipPoint').offset().top - settings.hideShift <
          $(this).offset().top + (settings.wholeVisible ? $(this).outerHeight() : 0) ||
          $('#scrollzipPoint').offset().top + (settings.wholeVisible ? $(this).outerHeight() : 0) >
            $(this).outerHeight() + $(this).offset().top - settings.hideShift)
      ) {
        $(this).removeClass('isShown');
        settings.hideFunction.call(this);
      }
      return this;
    });
  };
})(window.jQuery);
