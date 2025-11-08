document.addEventListener('DOMContentLoaded', function () {
  const scoreElements = document.querySelectorAll('.rating-score-value');

  scoreElements.forEach(scoreEl => {
    const rating = Math.round(parseFloat(scoreEl.textContent.trim()));
    if (isNaN(rating)) return;

    const starContainer = scoreEl.parentElement.querySelector('.rating-stars');
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll('svg path');

    stars.forEach((path, index) => {
      path.classList.toggle('selected', index < rating);
    });
  });
});
