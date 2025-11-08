document.addEventListener('DOMContentLoaded', function() {
    const reviewAddBtn = document.querySelector('.product-reviews-add');
    const reviewModal = document.getElementById('reviewsModal');
    const reviewModalClose = document.querySelector('.review-modal-close');
    const reviewsModalBackdrop = document.querySelector('.reviews-modal-backdrop');

    reviewAddBtn.addEventListener('click', function() {
        reviewModal.classList.add('show');
    });
    reviewModalClose.addEventListener('click', function() {
        reviewModal.classList.remove('show');
    });
    reviewsModalBackdrop.addEventListener('click', function() {
        reviewModal.classList.remove('show');
    });
});