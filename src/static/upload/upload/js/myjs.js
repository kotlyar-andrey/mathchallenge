function achievments_check () {
        $.ajax({
            type: 'GET',
            url: '/achievments_check/',
            success: function (html) {
                $('#fmodals').html(html);
                show_modals();
            }
        });
}

function show_modals() {
    $('.modal').modal({'backdrop': false});
}