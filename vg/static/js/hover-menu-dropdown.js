$('ul.nav li.dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(30).fadeIn(100);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(30).fadeOut(150);
});