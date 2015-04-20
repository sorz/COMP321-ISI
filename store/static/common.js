// Patch jQuery Ajax to send CSRF token.
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function initializeNavbar() {

  // Active current (selected) item.

  var PATH_REGEX_TO_NAME = {
    '^/account/register/': 'register',
    '^/account/login/': 'login',
    '^/account/': 'user',
    '^/category/': 'category',
    '^/order/': 'purchase',
    '^/cart/': 'cart',
    '^/about/': 'about',
    '^/$': 'home',
    '^/admin/order/pending/': 'order-pending',
    '^/admin/order/on-delivery/': 'order-on-delivery',
    '^/admin/order/fulfilled/': 'order-fulfilled',
    '^/admin/order/cancelled/': 'order-cancelled',
    '^/admin/order/best/': 'order-best',
    '^/admin/category/new/': 'category-new',
    '^/admin/category/': 'management',
    '^/admin/product/new/': 'product-new',
    '^/admin/product/': 'management',
    '^/admin/$': 'overview'
  };

  var path = window.location.pathname;
  for (var pathRegex in PATH_REGEX_TO_NAME) {
    if (path.match(pathRegex)) {
      $('li.nav-' + PATH_REGEX_TO_NAME[pathRegex]).addClass('active');
      break;
    }
  }
}


function addMessage(level, message) {
  // A JavaScript version of django.contrib.messages.add_messages().
  // Show a message on the top of web page,
  // and auto hide in several seconds.
  var $local = $('#local-messages');
  var $msg = $local.children('div').first().clone();
  $msg.addClass('alert-' + level)
    .removeClass('template')
    .append(document.createTextNode(message))
    .appendTo($local);

  setTimeout(function () {
    $msg.slideUp(function () {
      $msg.remove();
    });
  }, 2000);
}


$(document).ready(function () {
  initializeNavbar();

  // Auto hide messages.
  setTimeout(function () {
    $('#remote-messages').slideUp(function () {
      $(this).empty();
    });
  }, 5000);
  
  // Add-to-shopping-cart button.
  $('button.buy').click(function () {
    $.post($(this).data('link'), function () {
      addMessage('success', 'Product added into shopping cart.');
    });
  });

});

