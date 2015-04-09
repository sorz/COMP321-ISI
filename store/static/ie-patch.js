$(document).ready(function () {
  // Current IE do not support buttons with form attribut.
  $('button[form]').click(function (event) {
    event.preventDefault();
    var form = $(this).attr('form');
    $('form#' + form).submit();
  });
});

