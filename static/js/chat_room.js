(function() {
    'use strict'

    const chatRoom = document.querySelector('.chat-room');
    const roomUrl = chatRoom.getAttribute('data-url');
    const chat = chatRoom.querySelector('.chat');
    const input = chatRoom.querySelector('.message-input');
    const submit = chatRoom.querySelector('.message-submit');

    connect();

    function display_message(html) {
        const element = document.createElement("div");
        element.innerHTML = html;
        if (chat.innerHTML == '&nbsp;') {
            chat.innerHTML = '';
        }
        chat.insertAdjacentElement("beforeend", element);
        chat.scrollTop = chat.scrollHeight;
    }

    function send_message(message, socket) {
        if (message) {
            display_message(`<span style="font_weight: bold; color: green;">Вы отправили:</span>  ${message}`);
            socket.send(JSON.stringify({'message': message}));
        }
    }

    function received_message(message, user) {
        display_message(`<a href="${user.url}">${user.name}:</a> ${message}`);
    }

    function info_message(message) {
        display_message(`<span style="color: red;">${message}</span>`);
    }

    function connect(start_message) {
        const socket = new WebSocket('ws://' + window.location.host + roomUrl);
        socket.onopen = function () {
            input.focus();
            input.addEventListener('keyup', keyup);
            submit.addEventListener('click', click);
            if (start_message) {
                info_message(start_message);
            }
        }
        socket.onclose = function(event) {
            input.removeEventListener('keyup', keyup);
            submit.removeEventListener('click', click);
            console.error('Chat socket closed unexpectedly');
            info_message('Попытка восстановить соединение через 5 секунд')
            setTimeout(connect, 5000, 'Соединение восстановлено');
        };
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            received_message(data.message, data.user);
        };

        function keyup(event) {
            if (event.keyCode === 13) {
                submit.click();
            }
        }

        function click() {
            send_message(input.value, socket);
            input.value = '';
        }
    }

})()