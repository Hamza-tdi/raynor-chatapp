document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Retrieve username
    const username = document.querySelector('#get-username').innerHTML;
    const rooms = document.getElementsByClassName('select-room')

    // Set default room
    let room = rooms[0].textContent
    joinRoom(room);

    // send files
    const fileInput = document.querySelector('#formFileSm');
    fileInput.addEventListener('change', (e) => {
        console.log(document.querySelector('#formFileSm').value)
        socket.emit('incoming-msg', {'msg': document.querySelector('#formFileSm').value.replace(' ', '_'),
               'username': username, 'room': room, 'message_type': 'FILE'}); 
    });

    // Send messages
    document.querySelector('#send_message').onclick = () => {
        if (document.querySelector('#user_message').value != ''){
            socket.emit('incoming-msg', {'msg': document.querySelector('#user_message').value,
                'username': username, 'room': room, 'message_type': 'TEXT'});

            document.querySelector('#user_message').value = '';
        }
    };

    // Display all incoming messages
    socket.on('message', data => {

        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Display user's own message
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");

                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    //Append
                    document.querySelector('#display-message-section').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display-message-section').append(p);
            }
            // Display system message
            else {
                printSysMsg(data.msg);
            }


        }
        scrollDownChatWindow();
    });

    // Select a room
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML
            // Check if user already in the room
            if (newRoom === room) {
                msg = `You are already in ${room} room.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });

    // Logout from chat
    document.querySelector("#logout-btn").onclick = () => {
        leaveRoom(room);
    };

    // Trigger 'leave' event if user was previously on a room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        document.querySelectorAll('.select-room').forEach(p => {
            p.style.color = "black";
        });
    }

    // socket event join room
    socket.on('join_room', data => {
        for (const elm of data.data) {
            const a = document.createElement('a')
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            const chatWindow = document.querySelector("#display-message-section");
            if (elm.message_sender == data.user) {
                p.setAttribute("class", "my-msg");

                // Username
                span_username.setAttribute("class", "my-username");
                span_username.innerText = elm.message_sender;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = elm.message_time;

                // HTML to append
                if (elm.message_type == 'FILE'){
                    a.innerText = elm.message_text
                    a.setAttribute("href", '/get-file/'+elm.message_text)
                    a.setAttribute("target", "_blank")
                    p.innerHTML += span_username.outerHTML + br.outerHTML + a.outerHTML + br.outerHTML + span_timestamp.outerHTML
                }
                else {
                    p.innerHTML += span_username.outerHTML + br.outerHTML + elm.message_text + br.outerHTML + span_timestamp.outerHTML
                }
                //Append
                document.querySelector('#display-message-section').append(p);
            }
            else {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = elm.message_sender;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = elm.message_time;

                // HTML to append
                if (elm.message_type == 'FILE'){
                    a.innerText = elm.message_text
                    a.setAttribute("href", '/get-file/'+elm.message_text)
                    a.setAttribute("target", "_blank")
                    p.innerHTML += span_username.outerHTML + br.outerHTML + a.outerHTML + br.outerHTML + span_timestamp.outerHTML
                }
                else {
                    p.innerHTML += span_username.outerHTML + br.outerHTML + elm.message_text + br.outerHTML + span_timestamp.outerHTML
                }

                //Append
                document.querySelector('#display-message-section').append(p);
            }
        }
    })

    // Trigger 'join' event
    function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});

        // Highlight selected room
        document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
        document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});
