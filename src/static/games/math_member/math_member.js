$(function () {
    var game_option = {'lvl': 1, 'dd': ['+', '-', '*', '/']};
    $('#start').click(game_init);

    function game_init () {
        var cart_count = 4 + game_option.lvl*2;
        var karts = [];
        for (var i= 0;i < cart_count;i++) {
            karts[i] = problem(game_option);
            $('#templates .karta').show().clone(true).appendTo('.place').attr(karts[i]);
        }
        $('#templates .karta').hide();

        $('.karta').click(function () {
            console.log($(this).attr())
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
                        n1 = Math.floor(Math.random()*10);
                        n2 = Math.floor(Math.random()*10);
                        break;
                    case 2:
                        n1 = Math.floor(Math.random()*10+5);
                        n2 = Math.floor(Math.random()*10+5);
                        break;
                    case 3:
                        n1 = Math.floor(Math.random()*20+5);
                        n2 = Math.floor(Math.random()*20+5);
                        break;
                    case 4:
                        n1 = Math.floor(Math.random()*30+1);
                        n2 = Math.floor(Math.random()*30+1);
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
        switch (d) {
            case '+':
                return {'problem': n1+' + '+n2+' =', 'answer': n1+n2};
            case '-':
                return {'problem': n1+' - '+n2+' =', 'answer': n1-n2};
            case '*':
                return {'problem': n1+' * '+n2+' =', 'answer': n1*n2};
            case '/':
                return {'problem': n1+' / '+n2+' =', 'answer': n1/n2};
        }
    }
});