document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('input');
  const textarea = document.querySelectorAll('textarea');

  textarea.forEach(textarea => {
    textarea.addEventListener('blur', () => {
      if (textarea.value.trim() !== '') {
        textarea.classList.add('filled');
      } else {
        textarea.classList.remove('filled');
      }
    });
  });

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
