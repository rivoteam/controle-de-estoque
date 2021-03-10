// Delete Confirm Dialog
$(".btn-delete").click(function(event) {
  event.preventDefault();
  let r = confirm($( this ).attr('data-msg'));
  if (r === true) {
    window.location.href = $( this ).attr('href');
  }
});

// Select2
$(document).ready(function() {
    $('.form-select2').select2();
});
