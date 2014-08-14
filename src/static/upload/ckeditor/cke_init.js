window.onload = function()
{
    CKEDITOR.replace('material', {
        toolbar: 'Full'
    });
    textareas = $('textarea[name|=task_set],textarea[name|=remember_set]');
    for (var i=0; i<textareas.length; i++) {
        CKEDITOR.replace(textareas[i], {
            toolbar: 'Full'
        });
    }
};