(function () {
  'use strict';

  function formatPhone(input) {
    var value = input.value.replace(/\D/g, '');
    var formatted = '';
    var len = value.length;
    if (len > 0) {
      formatted += '(' + value.substring(0, 2);
      if (len > 2) {
        formatted += ') ';
        if (len >= 7) {
          formatted += value.substring(2, len - 4) + '-' + value.substring(len - 4);
        } else {
          formatted += value.substring(2);
        }
      }
    }
    input.value = formatted;
  }

  function setStatus(el, type, text) {
    if (!el) return;
    el.hidden = false;
    el.className = 'contato-form-status contato-form-status--' + type;
    el.textContent = text;
    el.setAttribute('role', 'alert');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('contato-form');
    if (!form) return;

    var accessKey = form.getAttribute('data-web3forms-key') || '';
    var statusEl = document.getElementById('contato-form-status');
    var submitBtn = form.querySelector('[type="submit"]');
    var phoneInput = form.querySelector('#telefone');

    if (phoneInput) {
      phoneInput.setAttribute('maxlength', '15');
      phoneInput.addEventListener('input', function () {
        formatPhone(phoneInput);
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      if (!accessKey) {
        setStatus(
          statusEl,
          'error',
          'Formulário indisponível no momento. Entre em contato por telefone ou e-mail.'
        );
        return;
      }

      var honeypot = form.querySelector('[name="botcheck"]');
      if (honeypot && honeypot.checked) return;

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.setAttribute('aria-busy', 'true');
      }
      if (statusEl) statusEl.hidden = true;

      var formData = new FormData(form);
      var estado = formData.get('estado_servico') || '';
      formData.append('access_key', accessKey);
      formData.append(
        'subject',
        estado ? 'Contato pelo site – Limnos (' + estado + ')' : 'Contato pelo site – Limnos'
      );
      formData.append('from_name', formData.get('name') || 'Visitante do site');
      formData.append('replyto', formData.get('email') || '');

      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: formData,
      })
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (data.success) {
            window.location.href = form.getAttribute('action') || '/obrigado';
            return;
          } else {
            setStatus(
              statusEl,
              'error',
              data.message || 'Não foi possível enviar. Tente novamente ou use nossos contatos ao lado.'
            );
          }
        })
        .catch(function () {
          setStatus(
            statusEl,
            'error',
            'Erro de conexão. Verifique sua internet ou fale conosco por telefone e e-mail.'
          );
        })
        .finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.removeAttribute('aria-busy');
          }
        });
    });
  });
})();
