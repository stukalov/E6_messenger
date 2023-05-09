(function() {
    'use strict'

    const chatRoom = document.querySelector('.chat-room');
    const roomUrl = chatRoom.getAttribute('data-url');
    const chat = chatRoom.querySelector('.chat');
    const input = chatRoom.querySelector('.message-input');
    const submit = chatRoom.querySelector('.message-submit');

    connect();

    function message(message, user) {
        const element = document.createElement("div");
        if (user === undefined) {
            element.style.color = "red";
            element.innerHTML = message;
        }
        else {
            element.innerHTML = `<a href="${user.url}">${user.name}:</a> ${message}`;
        }
        if (chat.innerHTML == '&nbsp;') {
            chat.innerHTML = '';
        }
        chat.insertAdjacentElement("beforeend", element);
        chat.scrollTop = chat.scrollHeight;
    }

    function connect(start_message) {
        const socket = new WebSocket('ws://' + window.location.host + roomUrl);
        socket.onopen = function () {
            input.focus();
            input.addEventListener('keyup', keyup);
            submit.addEventListener('click', click);
            if (start_message) {
                message(start_message);
            }
        }
        socket.onclose = function(event) {
            input.removeEventListener('keyup', keyup);
            submit.removeEventListener('click', click);
            console.error('Chat socket closed unexpectedly');
            message('Попытка восстановить соединение через 5 секунд')
            setTimeout(connect, 5000, 'Соединение восстановлено');
        };
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            message(data.message, data.user);
        };

        function keyup(event) {
            if (event.keyCode === 13) {
                submit.click();
            }
        }
        function click() {
            const message = input.value;
            if (message) {
                socket.send(JSON.stringify({'message': message}));
                input.value = '';
            }
        }
    }

})()