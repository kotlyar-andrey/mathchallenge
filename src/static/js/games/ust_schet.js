$(function () {
    var mode;
    var true_answer = 0, false_answer = 0;
    $('#game').click(function () {
        $('.game_start').hide();
        $('.schet_place').show();
        game_init();
    });
    $('#training').click(function () {
        $('.game_start').hide();
        $('.schet_place').show();
        training_init({});
    });

    function game_init() {
        mode = 'game';
        var game_option = {
            'point': 0,
            'lvl': 1,
            get points() {return this.point},
            set points(value) {this.point += value}
        };
        var ans_to_lvl = 0;
        var time = 60;
        var game_answer = problem({'lvl': game_option.lvl});
        var game_timeout = window.setTimeout(game_over, time*1000);
        var game_timer = window.setInterval(timer, 1000);
        $('.number-').click(answer_check);
        $('#info').html($('#game_info')[0].innerHTML);

        function timer() {
            time = time - 1;
            var mm = Math.floor(time/60);
            var ss = time - mm*60;
            if ((""+mm).length<2) {mm = "0"+mm}
            if ((""+ss).length<2) {ss = "0"+ss}
            $('#time').html(mm + ' : ' + ss);
        }

        function answer_check () {
            if ($('input#ans').val() == game_answer) {
                ans_to_lvl += 1;
                game_option.points = game_option.lvl*10;
                $('#points').html(game_option.points);
                $('.level-complit')[0].style.width = ans_to_lvl*15 + 'px';
                $('#smile').removeClass('fa-stop red-color').addClass('fa-smile-o green-color');
            } else {
                $('#smile').removeClass('fa-smile-o green-color').addClass('fa-stop red-color');
            }
            if (game_option.points >= summa(game_option.lvl)*100) {
                game_option.lvl += 1;
                ans_to_lvl = 0;
                $('.level-complit')[0].style.width = 0;
                time = 60;
                window.clearTimeout(game_timeout);
                game_timeout = window.setTimeout(game_over, time*1000);
                $('#level').html(game_option.lvl);
            }
            game_answer = problem({'lvl': game_option.lvl});
        }

        function game_over() {
            window.clearInterval(game_timer);
            $('input#ans').hide();
            $('#time').html('00 : 00');
            $('div[class^="number"]').attr("disabled", "disabled");
            $('.d, .numb').html('');
            $('#n1').html('Время вышло')[0].style.color = 'red';
            $('#smile').hide();
            $.get(
                '/game/game_over/',
                {'points': game_option.points, 'game_pk': 1} //pk прописано жестко!
            )
        }

        $('input#ans').keypress(function(event) {
            switch (event.which) {
                case 13: answer_check();
                    break;
                default:
                    break;
            }
        });
    }

    function training_init() {
        mode = 'training';
        var options = {'lvl': 1, 'dd': ['+', '-', '*', '/']};
        $('.number-').click(answer_check);
        $('#game_info').hide();
        $('#training_info').show();
        var game_answer = problem(options);

        function answer_check () {
            if ($('input#ans').val() == game_answer) {
                true_answer += 1;
                $('#ta').html(true_answer);
            } else {
                false_answer += 1;
                $('#fa').html(false_answer);
            }
            game_answer = problem(options);
        }

        $('input[type="checkbox"], #lvl').change(function () {
            $('#training_start').show();
        });

        $('#training_start').click(function () {
            var du = ['+'], i = 0;
            $('input[type="checkbox"]:checked').each(function () {
                du[i] = $(this).val();
                i++;
            });
            if (!du) {du = ['+']}
            options = {'lvl': Number($('#lvl').val()), 'dd': du};
            true_answer = 0;  $('#ta').html(true_answer);
            false_answer = 0; $('#fa').html(false_answer);
            game_answer = problem(options);
            $('input#ans').select();
            $('#training_start').hide();
        });

        $('input#ans').keypress(function(event) {
            switch (event.which) {
                case 13: answer_check();
                    break;
                default:
                    break;
            }
        });
    }

    function problem(obj_options) {
        var level = obj_options.lvl || 1;
        var dd = obj_options.dd || ['+', '-', '*', '/'];
        var n1, n2, d, tmp;
        if (!dd) {
            switch (Math.floor(Math.random()*4+1)) {
                case 2:
                    d = '-';
                    break;
                case 3:
                    d = '*';
                    break;
                case 4:
                    d = '/';
                    break;
                default:
                    d = '+';
                    break;
            }
        } else {
            d = dd[Math.floor(Math.random()*dd.length)]
        }
        switch (d) {
            case '+':
                switch (level) {
                    case 1:
                        n1 = Math.floor(Math.random()*10+1);
                        n2 = Math.floor(Math.random()*10+1);
                        break;
                    case 2:
                        n1 = Math.floor(Math.random()*20+9);
                        n2 = Math.floor(Math.random()*10+5);
                        break;
                    case 3:
                        n1 = Math.floor(Math.random()*20+30);
                        n2 = Math.floor(Math.random()*40+30);
                        break;
                    case 4:
                        n1 = Math.floor(Math.random()*50+50);
                        n2 = Math.floor(Math.random()*100+50);
                        break;
                    case 5:
                        n1 = Math.floor(Math.random()*500+100);
                        n2 = Math.floor(Math.random()*500+100);
                        break;
                    case 6:
                        n1 = Math.floor(Math.random()*5000+500);
                        n2 = Math.floor(Math.random()*5000+500);
                        break;
                    case 7:
                        n1 = Math.floor(Math.random()*90000+10000);
                        n2 = Math.floor(Math.random()*90000+10000);
                        break;
                    default:
                        n1 = Math.floor(Math.random()*900000+100000);
                        n2 = Math.floor(Math.random()*900000+100000);
                        break;
                }
                break;
            case '-':
                switch (level) {
                    case 1:
                        n2 = Math.floor(Math.random()*9+1);
                        n1 = n2 + Math.floor(Math.random()*10+1);
                        break;
                    case 2:
                        n2 = Math.floor(Math.random()*10+5);
                        n1 = n2 + Math.floor(Math.random()*10+5);
                        break;
                    case 3:
                        n2 = Math.floor(Math.random()*20+11);
                        n1 = n2 + Math.floor(Math.random()*20+10);
                        break;
                    case 4:
                        n2 = Math.floor(Math.random()*100+100);
                        n1 = n2 + Math.floor(Math.random()*50+25);
                        break;
                    case 5:
                        n2 = Math.floor(Math.random()*400+100);
                        n1 = n2 + Math.floor(Math.random()*200+100);
                        break;
                    case 6:
                        n2 = Math.floor(Math.random()*1000+500);
                        n1 = n2 + Math.floor(Math.random()*1000+500);
                        break;
                    case 7:
                        n2 = Math.floor(Math.random()*9000+1000);
                        n1 = n2 + Math.floor(Math.random()*5000+1000);
                        break;
                    default:
                        n2 = Math.floor(Math.random()*90000+10000);
                        n1 = n2 + Math.floor(Math.random()*90000+10000);
                        break;
                }
                break;
            case '*':
                switch (level) {
                    case 1:
                        n1 = Math.floor(Math.random()*9+1);
                        n2 = Math.floor(Math.random()*9+1);
                        break;
                    case 2:
                        n1 = Math.floor(Math.random()*9+5);
                        n2 = Math.floor(Math.random()*9+5);
                        break;
                    case 3:
                        n1 = Math.floor(Math.random()*5+5);
                        n2 = Math.floor(Math.random()*10+10);
                        break;
                    case 4:
                        n1 = Math.floor(Math.random()*100+100);
                        n2 = Math.floor(Math.random()*4+3);
                        break;
                    case 5:
                        n1 = Math.floor(Math.random()*20+10);
                        n2 = Math.floor(Math.random()*20+10);
                        break;
                    case 6:
                        n1 = Math.floor(Math.random()*50+20);
                        n2 = Math.floor(Math.random()*50+20);
                        break;
                    case 7:
                        n1 = Math.floor(Math.random()*100+50);
                        n2 = Math.floor(Math.random()*500+50);
                        break;
                    default:
                        n1 = Math.floor(Math.random()*900+100);
                        n2 = Math.floor(Math.random()*900+100);
                        break;
                }
                break;
            case '/':
                switch (level) {
                    case 1:
                        n2 = Math.floor(Math.random()*9+1);
                        tmp = Math.floor(Math.random()*8+1);
                        n1 = n2 * tmp;
                        break;
                    case 2:
                        n2 = Math.floor(Math.random()*9+5);
                        tmp = Math.floor(Math.random()*5+1);
                        n1 = n2 * tmp;
                        break;
                    case 3:
                        n2 = Math.floor(Math.random()*10+8);
                        tmp = Math.floor(Math.random()*5+5);
                        n1 = n2 * tmp;
                        break;
                    case 4:
                        n2 = Math.floor(Math.random()*40+10);
                        tmp = Math.floor(Math.random()*6+3);
                        n1 = n2 * tmp;
                        break;
                    case 5:
                        n2 = Math.floor(Math.random()*30+10);
                        tmp = Math.floor(Math.random()*10+11);
                        n1 = n2 * tmp;
                        break;
                    case 6:
                        n2 = Math.floor(Math.random()*85+15);
                        tmp = Math.floor(Math.random()*15+15);
                        n1 = n2 * tmp;
                        break;
                    case 7:
                        n2 = Math.floor(Math.random()*800+101);
                        tmp = Math.floor(Math.random()*40+20);
                        n1 = n2 * tmp;
                        break;
                    default:
                        n1 = Math.floor(Math.random()*9000+1000);
                        n2 = Math.floor(Math.random()*900+100);
                        break;
                }
                break;
            default:
                switch (level) {
                    case 1:
                        n1 = Math.floor(Math.random()*10+1);
                        n2 = Math.floor(Math.random()*10+1);
                        break;
                    case 2:
                        n1 = Math.floor(Math.random()*20+9);
                        n2 = Math.floor(Math.random()*10+5);
                        break;
                    case 3:
                        n1 = Math.floor(Math.random()*20+30);
                        n2 = Math.floor(Math.random()*40+30);
                        break;
                    case 4:
                        n1 = Math.floor(Math.random()*100+50);
                        n2 = Math.floor(Math.random()*100+50);
                        break;
                    case 5:
                        n1 = Math.floor(Math.random()*500+100);
                        n2 = Math.floor(Math.random()*500+100);
                        break;
                    case 6:
                        n1 = Math.floor(Math.random()*5000+500);
                        n2 = Math.floor(Math.random()*5000+500);
                        break;
                    case 7:
                        n1 = Math.floor(Math.random()*90000+10000);
                        n2 = Math.floor(Math.random()*90000+10000);
                        break;
                    default:
                        n1 = Math.floor(Math.random()*900000+100000);
                        n2 = Math.floor(Math.random()*900000+100000);
                        break;
                }
                break;
        }
        $('input#ans').val('');
        $('#n1').html(n1);
        $('#n2').html(n2);
        $('#d').html(d);
        switch (d) {
            case '+':
                return n1+n2;
            case '-':
                return n1-n2;
            case '*':
                return n1*n2;
            case '/':
                return n1/n2;
        }
    }

    $('div[class^="number"]').click(function() {
        var ch = $(this).attr("data-n");
        var inp = $('input#ans');
        switch (ch) {
            case "0": inp.val(inp.val()+ch);
                 break;
            case "1": inp.val(inp.val()+ch);
                 break;
            case "2": inp.val(inp.val()+ch);
                 break;
            case "3": inp.val(inp.val()+ch);
                break;
            case "4": inp.val(inp.val()+ch);
                break;
            case "5": inp.val(inp.val()+ch);
                break;
            case "6": inp.val(inp.val()+ch);
                break;
            case "7": inp.val(inp.val()+ch);
                break;
            case "8": inp.val(inp.val()+ch);
                break;
            case "9": inp.val(inp.val()+ch);
                break;
            case "sep": inp.val(inp.val()+',');
                break;
            case "bs": inp.val(inp.val().slice(0,inp.val().length-1));
                break;
            default:
                break;
        }
        inp.focus();
    });
    $('#reload').click(function () {
        location.reload();
    })
});

function summa (n) {
    var s = 0;
    for (var i=1;i<=n;i++) {
        s += i;
    }
    return s;
}