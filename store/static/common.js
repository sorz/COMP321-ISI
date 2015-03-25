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


function initialize_navbar() {

  // Active current (selected) item.

  var PATH_REGEX_TO_NAME = {
    '^/account/register/': 'register',
    '^/account/login/': 'login',
    '^/account/': 'user',
    '^/category/': 'category',
    '^/order/': 'purchase',
    '^/cart/': 'cart',
    '^/$': 'home',
    '^/admin/order/pending': 'order-pending',
    '^/admin/order/on-delivery': 'order-on-delivery',
    '^/admin/category/new/': 'category-new',
    '^/admin/category/': 'management',
    '^/admin/product/new/': 'product-new',
    '^/admin/product/': 'management',
    '^/admin/': 'overview'
  };

  var path = window.location.pathname;
  for (var pathRegex in PATH_REGEX_TO_NAME) {
    if (path.match(pathRegex)) {
      $('li.nav-' + PATH_REGEX_TO_NAME[pathRegex]).addClass('active');
      break;
    }
  }
}


$(document).ready(function () {
  initialize_navbar();

  // Auto hide messages.
  setTimeout(function () {
    $('#alert-messages').slideUp(function () {
      $(this).empty();
    });
  }, 5000);
  
  // Add-to-shopping-cart button.
  $('button.buy').click(function () {
    $.post($(this).data('link'), function () {
      alert('Added.');
    });
  });

});

