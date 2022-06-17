document.addEventListener('DOMContentLoaded', () => {
        // Connect to websocket
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        const btns = document.querySelectorAll('.disable');
        for (const btn of btns) {
            btn.addEventListener('click', function() {
                socket.emit('disable_room', {'room': btn.getAttribute('data-set')})
                if (btn.innerText == 'Enable'){
                    btn.innerText = 'Disable'
                    btn.setAttribute('data-set', btn.getAttribute('data-set').replace('YES', 'NO'))
                }
                else{
                    btn.innerText = 'Enable'
                    btn.setAttribute('data-set', btn.getAttribute('data-set').replace('NO', 'YES'))
                }
            });
        }
});