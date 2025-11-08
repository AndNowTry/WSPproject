document.addEventListener('DOMContentLoaded', function() {
  $('a[href^="#"]').on('click', function(e) {
    e.preventDefault();

    var target = $(this.hash);
    if (!target.length) return;

    var offset = $('.header').outerHeight() || 100;

    $('html, body').stop().animate({
      scrollTop: target.offset().top - offset
    }, 900, 'swing');

    history.pushState(null, null, this.hash);
  });
});
