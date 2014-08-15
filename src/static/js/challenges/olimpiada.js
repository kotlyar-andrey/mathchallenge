$(function () {
    var time = 300;
    function timer() {
        time = time - 1;
        hh = Math.floor(time/3600);
        mm = Math.floor(time/60) - hh*60;
        ss = time - mm*60 - hh*3600;
        if ((""+mm).length<2) {mm = "0"+mm}
        if ((""+ss).length<2) {ss = "0"+ss}
        $('#timer').html(hh+ ' : ' +mm + ' : ' + ss);
    }

    function check(){
        $.ajax({
            type: 'GET',
            url: '/challenge/olimpiada_check/',
            data: $('#answer_form').serialize(),
            success: function (req) {
                $('#target').html(req);
            },
            error: function () {
                $('#target').html('Ошибка.');
            }
        });
        $('#timer').hide();
        $('#button_res').html('');
        $('.olimpiada-answer-form').html('');
        $('form hr').hide();
    }
    window.setInterval(timer, 1000);
    window.setTimeout(check, time*1000);
    $('#answerButton').click(check);
})