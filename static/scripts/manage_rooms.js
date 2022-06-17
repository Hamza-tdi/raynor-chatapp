document.addEventListener('DOMContentLoaded', () => {
        // Connect to websocket
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        const btns = document.querySelectorAll('.disable');
        for (const btn of btns) {
            btn.addEventListener('click', function() {
                socket.emit('disable_room', {'room': btn.getAttribute('data-set')})
                if (btn.innerText == 'enable'){
                    btn.innerText = 'Disable'
                    btn.setAttribute('data-set', btn.getAttribute('data-set').replace('is_active', 'is_inactive'))
                }
                else{
                    btn.innerText = 'Enable'
                    btn.setAttribute('data-set', btn.getAttribute('data-set').replace('is_inactive', 'is_active'))
                }
            });
        }
});