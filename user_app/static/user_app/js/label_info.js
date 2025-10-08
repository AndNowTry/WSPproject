document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('input');

  inputs.forEach(input => {
    input.addEventListener('blur', () => {
      if (input.value.trim() !== '') {
        input.classList.add('filled');
      } else {
        input.classList.remove('filled');
      }
    });
  });
});
