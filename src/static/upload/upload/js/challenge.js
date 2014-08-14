$(function () {
    $('<h4 class="text-center italic">Задачи, оцениваемые в 3 балла</h4>').insertBefore('#pr1');
    $('<h4 class="text-center italic">Задачи, оцениваемые в 4 балла</h4>').insertAfter('#pr10');
    $('<h4 class="text-center italic">Задачи, оцениваемые в 5 баллов</h4>').insertAfter('#pr20');

    var time = 4500;
    function timer() {
        time = time - 1;
        hh = Math.floor(time/3600);
        mm = Math.floor(time/60) - hh*60;
        ss = time - mm*60 - hh*3600;
        if ((""+mm).length<2) {mm = "0"+mm};
        if ((""+ss).length<2) {ss = "0"+ss};
        $('#timer').html(hh+ ' : ' +mm + ' : ' + ss);
    }

    function check(){
        $.ajax({
            type: 'POST',
            url: '/challenge/kenguru_check/',
            data: $('#answer_form').serialize(),
            success: function (req) {
                $('#target').html(req);
                $('#timer').hide();
                $('#button_res').html('');
                $('.kenguru-answer-form').hide();
                $('.challenge_problem hr').hide();
            },
            error: function () {
                $('#target').html('Ошибка.');
            }
        });
    }
    window.setInterval(timer, 1000);
    window.setTimeout(check, 4500000);
    $('#answerButton').click(check);
})