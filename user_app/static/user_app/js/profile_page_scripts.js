document.addEventListener('DOMContentLoaded', function()
{
    const fileInput = document.getElementById('id_avatar');
    const form = document.getElementById('profile-form');

    if (fileInput)
    {
        console.log(2);
        fileInput.addEventListener('change', function()
        {
            console.log(1);
            form.submit();
        });
    }
});