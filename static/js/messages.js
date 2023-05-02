(function() {
    'use strict'
    const url = document.querySelector('.messaging').getAttribute('data-url');
    const messages = document.querySelector('.messaging .messages');
    const textarea = document.querySelector('.messaging textarea');

    messages.scrollTo(0, messages.scrollHeight);
    if (textarea) {
        textarea.addEventListener('input', function () {
            textarea.style.height = `${textarea.scrollHeight+2}px`;
        });

        setInterval(checkMessages, 1000);
    }

    function checkMessages() {
        const unread = messages.querySelectorAll('.sender[data-unread]');
        const unread_ids = [];
        unread.forEach(element => unread_ids.push(element.getAttribute('data-id')))

        let full_url = `${url}?`;
        const last = messages.querySelector('.message:last-child');
        if (last) {
            full_url = `${full_url}id=${last.getAttribute('data-id')}&`;
        }
        if (unread_ids.length) {
            full_url = `${full_url}unread=${unread_ids.join(',')}&`;
        }
        fetch(full_url)
        .then(response => {
            return response.text()
        })
        .then(html => {
            const DOM = new DOMParser().parseFromString(html, "text/html");
            const new_messages = DOM.querySelectorAll('.message');
            new_messages.forEach(element => {
                const old_element = document.getElementById(element.id)
                if (old_element) {
                    old_element.replaceWith(element)
                }
                else {
                    messages.insertAdjacentElement('beforeend', element)
                    messages.scrollTo(0, messages.scrollHeight);
                }
            })
        })
    }

})()