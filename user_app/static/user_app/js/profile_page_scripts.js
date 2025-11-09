document.addEventListener('DOMContentLoaded', function()
{
    const dialog_button_open = document.getElementById('dialog_button_open')
    const dialog_button_close = document.getElementById('dialog_button_close')
    const dialog_window = document.getElementById('dialog_window')

    dialog_button_open.addEventListener("click", function () {
      dialog_window.showModal()
    })

    dialog_button_close.addEventListener("click", function () {
      dialog_window.close()
    })
});