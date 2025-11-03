document.addEventListener('DOMContentLoaded', function () {
  const ratingBlocks = document.querySelectorAll('.rating-stars');

  ratingBlocks.forEach(block => {
    const input = block.querySelector('input[name="review-rating-count"]');
    if (!input) return;

    const rating = Math.round(parseFloat(input.value));
    const stars = block.querySelectorAll('svg path');

    stars.forEach((path, index) => {
      if (index < rating) {
        path.classList.add('selected');
      } else {
        path.classList.remove('selected');
      }
    });
  });
});
