(function () {
  const wrapper = document.querySelector('.image-slider-slider');
  if (!wrapper) return;

  const inner = wrapper.querySelector('.image-slider-inner');
  const hoverLine = wrapper.querySelector('.hover-line');
  const sliderImages = wrapper.querySelectorAll('.slider-image');
  const mainImg = document.querySelector('.image-slider-main img');
  if (!inner || !hoverLine || !sliderImages.length || !mainImg) return;

  let activeEl = sliderImages[0];
  let hoverTimer = null;

  setActive(activeEl);

  inner.addEventListener('pointerenter', onPointerEnter, true);
  inner.addEventListener('pointermove', onPointerMove, true);
  inner.addEventListener('pointerleave', onPointerLeave, true);

  sliderImages.forEach(img => {
    img.addEventListener('click', () => switchTo(img));

    img.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimer);
      const el = img;
      hoverTimer = setTimeout(() => {
        switchTo(el);
      }, 150);
    });

    img.addEventListener('mouseleave', () => clearTimeout(hoverTimer));
  });

  function switchTo(img) {
    activeEl = img;
    const src = img.querySelector('img').getAttribute('src');
    mainImg.src = src;
    setActive(img);
  }

  function getRelativeRect(child, ancestor) {
    const childRect = child.getBoundingClientRect();
    const ancRect = ancestor.getBoundingClientRect();
    return {
      top: childRect.top - ancRect.top,
      height: childRect.height
    };
  }

  function showLineFor(target) {
    const rect = getRelativeRect(target, wrapper);
    hoverLine.style.top = rect.top + 'px';
    hoverLine.style.height = rect.height + 'px';
    hoverLine.style.opacity = '1';
  }

  function setActive(el) {
    showLineFor(el);
  }

  function onPointerEnter(e) {
    const t = e.target.closest('.slider-image');
    if (t && inner.contains(t)) showLineFor(t);
  }

  function onPointerMove(e) {
    const t = e.target.closest('.slider-image');
    if (t && inner.contains(t)) showLineFor(t);
  }

  function onPointerLeave(e) {
    clearTimeout(hoverTimer);
    if (!inner.contains(e.relatedTarget)) setActive(activeEl);
  }

  inner.addEventListener('scroll', () => setActive(activeEl), { passive: true });
})();

(function () {
  const mainImgEl = document.querySelector('.image-slider-main img');
  const modal = document.getElementById('imageModal');
  if (!modal || !mainImgEl) return;

  const modalMain = modal.querySelector('.image-modal-main');
  const modalThumbs = modal.querySelector('.image-modal-thumbs');
  const modalClose = modal.querySelector('.image-modal-close');
  const modalBackdrop = modal.querySelector('.image-modal-backdrop');
  const btnPrev = document.getElementById('modalPrevBtn');
  const btnNext = document.getElementById('modalNextBtn');
  const thumbImages = [...document.querySelectorAll('.slider-image img')];

  let modalActiveIndex = 0;

  function openModal(index) {
    modalActiveIndex = index;
    modal.classList.add('show');
    renderModal();
  }

  function closeModal() {
    modal.classList.remove('show');
  }

  function renderModal() {
    modalMain.src = thumbImages[modalActiveIndex].src;
    renderModalThumbs();
    updateThumbsActive();
    centerActiveThumb();
    mainImgEl.src = thumbImages[modalActiveIndex].src;
  }

  function renderModalThumbs() {
    modalThumbs.innerHTML = "";
    thumbImages.forEach((img, i) => {
      const el = document.createElement('img');
      el.src = img.src;
      el.className = 'image-modal-thumb';
      if (i === modalActiveIndex) el.classList.add('active');

      el.addEventListener('click', () => {
        modalActiveIndex = i;
        modalMain.src = img.src;
        mainImgEl.src = img.src;
        updateThumbsActive();
        centerActiveThumb();
      });

      modalThumbs.appendChild(el);
    });
  }

  function updateThumbsActive() {
    Array.from(modalThumbs.children).forEach((thumb, idx) => {
      thumb.classList.toggle('active', idx === modalActiveIndex);
    });
  }

  function centerActiveThumb() {
    const active = modalThumbs.querySelector('.active');
    if (!active) return;
    const container = modalThumbs;
    const offset = active.offsetLeft - (container.clientWidth / 2) + (active.clientWidth / 2);
    container.scrollTo({ left: offset, behavior: 'smooth' });
  }

  function next() {
    modalActiveIndex = (modalActiveIndex + 1) % thumbImages.length;
    renderModal();
  }

  function prev() {
    modalActiveIndex = (modalActiveIndex - 1 + thumbImages.length) % thumbImages.length;
    renderModal();
  }

  mainImgEl.addEventListener('click', () => {
    const index = thumbImages.findIndex(i => i.src === mainImgEl.src);
    openModal(index >= 0 ? index : 0);
  });

  thumbImages.forEach((img, i) => {
    img.addEventListener('click', () => openModal(i));
  });

  btnNext.addEventListener('click', next);
  btnPrev.addEventListener('click', prev);
  modalClose.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', closeModal);

  document.addEventListener('keydown', e => {
    if (!modal.classList.contains('show')) return;
    if (e.key === 'ArrowRight') next();
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'Escape') closeModal();
  });
})();

(function() {
  const scroller = document.querySelector('.image-slider-inner');
  if (!scroller) return;

  let isDown = false;
  let startY;
  let scrollTop;

  scroller.addEventListener('pointerdown', (e) => {
    isDown = true;
    scroller.setPointerCapture(e.pointerId);
    startY = e.pageY - scroller.offsetTop;
    scrollTop = scroller.scrollTop;
    scroller.style.cursor = 'grabbing';
  });

  scroller.addEventListener('pointermove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const y = e.pageY - scroller.offsetTop;
    const walk = (y - startY) * 1.2;
    scroller.scrollTop = scrollTop - walk;
  });

  scroller.addEventListener('pointerup', (e) => {
    isDown = false;
    scroller.releasePointerCapture(e.pointerId);
    scroller.style.cursor = '';
  });

  scroller.addEventListener('pointerleave', () => {
    isDown = false;
    scroller.style.cursor = '';
  });
})();