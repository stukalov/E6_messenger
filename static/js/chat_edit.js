(function() {
    'use strict'

    const chatEdit = document.querySelector('.chat-edit');
    const title = chatEdit.querySelector('.chat-title');
    const descr = chatEdit.querySelector('.chat-descr');
    const submit = chatEdit.querySelector('button');
    const link = chatEdit.querySelector('a');
    const header = document.getElementsByTagName('h1')[0];
    const csrf = chatEdit.querySelector('input[name="csrfmiddlewaretoken"]');

    submit.addEventListener('click', ajax.bind(null, 'POST'));

    ajax('GET');

    function getAjaxUrl() {
        if (chatEdit.dataset.id) {
            return `${chatEdit.dataset.url}/${chatEdit.dataset.id}`;
        }
        else {
            return chatEdit.dataset.url
        }
    }

    function setData(data) {
        if (data.id) {
            chatEdit.dataset.id = data.id;
            title.value = data.title,
            descr.value = data.description

            header.innerHTML = `Чат ${data.title}`
            document.title = `Чат ${data.title} | Messenger`
            link.setAttribute('href', data.room_url)
        }
        else {
            header.innerHTML = '<i>Новый чат</i>';
            document.title = 'Новый чат | Messenger'
        }
    }

    function ajax(method) {
        let body;
        const headers = {
          'Accept': 'application/json',
        }
        if (method == 'POST') {
            body = JSON.stringify({
                title: title.value,
                description: descr.value,
            })
            headers['Content-Type'] = 'application/json';
            headers['X-CSRFToken'] = csrf.value;
        }
        fetch(getAjaxUrl(), {
            method: method,
            headers: headers,
            body: body,
        })
        .then(response => {
            return response.text();
        })
        .then(json => {
            return JSON.parse(json);
        })
        .then(data => {
            setData(data);
        })
        .catch(() => {
            console.log('error');
        });
    }

})()