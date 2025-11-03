document.addEventListener('DOMContentLoaded', function () {
  const stars = document.querySelectorAll('.modal-rating-stars svg');
  const ratingInput = document.getElementById('ratingInput');

  stars.forEach((star, index) => {
    star.addEventListener('click', function () {
      const rating = index + 1;
      ratingInput.value = rating;

      stars.forEach((s, i) => {
        const path = s.querySelector('path');
        if (i < rating) {
          path.classList.add('selected');
        } else {
          path.classList.remove('selected');
        }
      });
    });

    star.addEventListener('mouseover', function () {
      const hoverValue = index + 1;
      stars.forEach((s, i) => {
        const path = s.querySelector('path');
        if (i < hoverValue) {
          path.classList.add('selected');
        } else {
          path.classList.remove('selected');
        }
      });
    });
  });

  document.querySelector('.rating-stars').addEventListener('mouseleave', function () {
    const savedRating = Number(ratingInput.value);
    stars.forEach((s, i) => {
      const path = s.querySelector('path');
      if (i < savedRating) path.classList.add('selected');
      else path.classList.remove('selected');
    });
  });
});
