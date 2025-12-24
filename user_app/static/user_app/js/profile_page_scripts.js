document.addEventListener('DOMContentLoaded', () => {
    const openBtn = document.getElementById('dialog_button_open');
    const closeBtn = document.getElementById('dialog_button_close');
    const dialog = document.getElementById('dialog_window');

    if (!openBtn || !closeBtn || !dialog) return;

    openBtn.addEventListener('click', () => {
        dialog.showModal();
        dialog.classList.add('dialog-open');
    });

    closeBtn.addEventListener('click', () => {
        closeDialog();
    });

    dialog.addEventListener('click', (e) => {
        if (e.target === dialog) {
            closeDialog();
        }
    });

    function closeDialog() {
        dialog.classList.remove('dialog-open');
        dialog.classList.add('dialog-close');

        setTimeout(() => {
            dialog.close();
            dialog.classList.remove('dialog-close');
        }, 200);
    }
});
