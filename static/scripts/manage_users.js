document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    // promote user to admin
    const btns = document.querySelectorAll('.promote');
    for (const btn of btns) {
        btn.addEventListener('click', function() {
            socket.emit('promote_user', {'user': btn.getAttribute('data-set')})
            if (btn.innerText == 'promote'){
                btn.innerText = 'demote'
                btn.setAttribute('data-set', btn.getAttribute('data-set').replace('user', 'admin'))
            }
            else{
                btn.innerText = 'promote'
                btn.setAttribute('data-set', btn.getAttribute('data-set').replace('admin', 'user'))
            }
        });
    }

    // delete user or admin
    const delete_btns = document.querySelectorAll('.delete');
    for (const btn of delete_btns) {
        btn.addEventListener('click', function() {
            socket.emit('disable_user', {'user': btn.getAttribute('data-set')})
            if (btn.innerText == 'enable'){
                btn.innerText = 'disable'
            }
            else{
                btn.innerText = 'enable'
            }
        });
    }


    var properties = [
        'id',
        'username',
        'role',
    ];

    $.each( properties, function( i, val ) {

        var orderClass = '';

        $("#" + val).click(function(e){
            e.preventDefault();
            $('.filter__link.filter__link--active').not(this).removeClass('filter__link--active');
            $(this).toggleClass('filter__link--active');
            $('.filter__link').removeClass('asc desc');

            if(orderClass == 'desc' || orderClass == '') {
                    $(this).addClass('asc');
                    orderClass = 'asc';
            } else {
                $(this).addClass('desc');
                orderClass = 'desc';
            }

            var parent = $(this).closest('.header__item');
                var index = $(".header__item").index(parent);
            var $table = $('.table-content');
            var rows = $table.find('.table-row').get();
            var isSelected = $(this).hasClass('filter__link--active');
            var isNumber = $(this).hasClass('filter__link--number');

            rows.sort(function(a, b){

                var x = $(a).find('.table-data').eq(index).text();
                    var y = $(b).find('.table-data').eq(index).text();

                if(isNumber == true) {

                    if(isSelected) {
                        return x - y;
                    } else {
                        return y - x;
                    }

                } else {

                    if(isSelected) {
                        if(x < y) return -1;
                        if(x > y) return 1;
                        return 0;
                    } else {
                        if(x > y) return -1;
                        if(x < y) return 1;
                        return 0;
                    }
                }
                });

            $.each(rows, function(index,row) {
                $table.append(row);
            });

            return false;
        });

    });
});